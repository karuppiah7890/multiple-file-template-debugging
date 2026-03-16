from __future__ import annotations

import json
import os
import subprocess
from pathlib import Path

import yaml


WORKSPACE = Path("/app/helm-charts-editor")
CHART_DIR = WORKSPACE / "charts" / "mlflow"
TARGET_FILES = [
    CHART_DIR / "values.yaml",
    CHART_DIR / "values.schema.json",
    CHART_DIR / "templates" / "pvc.yaml",
    CHART_DIR / "templates" / "deployment.yaml",
]
STALE_PATTERN = "{{ .Release.Name }}-data-pvc"


def run(cmd: list[str], *, timeout: int = 180) -> subprocess.CompletedProcess[str]:
    result = subprocess.run(
        cmd,
        cwd=WORKSPACE,
        text=True,
        capture_output=True,
        env=os.environ.copy(),
        timeout=timeout,
    )
    if result.returncode != 0:
        raise SystemExit(
            f"Command failed: {' '.join(cmd)}\nSTDOUT:\n{result.stdout}\nSTDERR:\n{result.stderr}"
        )
    return result


def require_files() -> None:
    required = [
        WORKSPACE / ".gitignore",
        WORKSPACE / "charts" / "mlflow" / "Chart.yaml",
        WORKSPACE / "charts" / "mlflow" / "values.yaml",
        WORKSPACE / "charts" / "mlflow" / "values.schema.json",
        WORKSPACE / "charts" / "mlflow" / "templates" / "_helpers.tpl",
        WORKSPACE / "charts" / "mlflow" / "templates" / "pvc.yaml",
        WORKSPACE / "charts" / "mlflow" / "templates" / "deployment.yaml",
    ]
    missing = [str(path) for path in required if not path.exists()]
    if missing:
        raise SystemExit("Missing required files:\n" + "\n".join(missing))


def require_schema_shape() -> None:
    text = (CHART_DIR / "values.schema.json").read_text(encoding="utf-8")
    persistence_occurrences = text.count('"persistence"')
    if persistence_occurrences < 4:
        raise SystemExit(
            f"Expected duplicate persistence blocks in values.schema.json, found {persistence_occurrences}."
        )

    schema = json.loads(text)
    root_persistence = schema["properties"]["persistence"]
    required_fields = {"enabled", "size", "storageClass", "mountPath"}
    if set(root_persistence["properties"]) != required_fields:
        raise SystemExit("Root persistence schema drifted away from the seeded shape.")


def require_no_stale_release_only_rule() -> None:
    offenders: list[str] = []
    for path in TARGET_FILES:
        text = path.read_text(encoding="utf-8")
        if STALE_PATTERN in text:
            offenders.append(str(path))
    if offenders:
        raise SystemExit(
            "Release-name-only PVC naming is still present in:\n" + "\n".join(offenders)
        )


def render(release: str, namespace: str) -> list[dict]:
    result = run(
        ["helm", "template", release, str(CHART_DIR), "--namespace", namespace],
        timeout=180,
    )
    docs = [doc for doc in yaml.safe_load_all(result.stdout) if doc]
    if not docs:
        raise SystemExit("Helm template produced no YAML documents.")
    return docs


def lint_chart() -> None:
    run(["helm", "lint", str(CHART_DIR)], timeout=180)


def check_render(release: str, namespace: str, expected_pvc_name: str) -> None:
    docs = render(release, namespace)
    pvc_docs = [doc for doc in docs if doc.get("kind") == "PersistentVolumeClaim"]
    if len(pvc_docs) != 1:
        raise SystemExit(f"Expected exactly one PVC for release {release}, found {len(pvc_docs)}.")

    pvc = pvc_docs[0]
    actual_name = pvc.get("metadata", {}).get("name")
    actual_namespace = pvc.get("metadata", {}).get("namespace")
    if actual_name != expected_pvc_name:
        raise SystemExit(f"PVC name mismatch: expected {expected_pvc_name}, got {actual_name}.")
    if actual_namespace != namespace:
        raise SystemExit(
            f"PVC namespace mismatch: expected {namespace}, got {actual_namespace!r}."
        )

    workloads = [
        doc
        for doc in docs
        if doc.get("kind") in {"Deployment", "StatefulSet"}
    ]
    if len(workloads) != 1:
        raise SystemExit(f"Expected one workload, found {len(workloads)}.")

    workload = workloads[0]
    pod_spec = workload["spec"]["template"]["spec"]
    volumes = pod_spec.get("volumes", [])
    pvc_volumes = [
        volume for volume in volumes if "persistentVolumeClaim" in volume
    ]
    if len(pvc_volumes) != 1:
        raise SystemExit(f"Expected one PVC-backed volume, found {len(pvc_volumes)}.")

    claim_name = pvc_volumes[0]["persistentVolumeClaim"].get("claimName")
    if claim_name != expected_pvc_name:
        raise SystemExit(
            f"Workload claimName mismatch: expected {expected_pvc_name}, got {claim_name}."
        )

    values = yaml.safe_load((CHART_DIR / "values.yaml").read_text(encoding="utf-8"))
    expected_mount_path = values["persistence"]["mountPath"]
    container_mounts = []
    for container in pod_spec.get("containers", []):
        for mount in container.get("volumeMounts", []):
            if mount.get("name") == pvc_volumes[0]["name"]:
                container_mounts.append(mount)
    if len(container_mounts) != 1:
        raise SystemExit(
            f"Expected one PVC-backed volume mount, found {len(container_mounts)}."
        )
    mount_path = container_mounts[0].get("mountPath")
    if mount_path != expected_mount_path:
        raise SystemExit(
            f"Volume mount path mismatch: expected {expected_mount_path}, got {mount_path}."
        )


def main() -> None:
    require_files()
    require_schema_shape()
    require_no_stale_release_only_rule()
    lint_chart()
    check_render("mlflow-test", "mlflow-test2", "mlflow-test-data-pvc")
    check_render("prod-check", "prod-space", "prod-check-mlflow-data-pvc")
    print("Verification passed.")

if __name__ == "__main__":
    main()
