Word count: 296 words (encouraged range: 300-700)

Raw Output

{
  "encouragedMax": 700,
  "encouragedMin": 300,
  "errorThreshold": 2000,
  "minimumWords": 100,
  "wordCount": 296
}
Prompt uses supported plain-text characters
Description contains only supported plain-text ASCII characters

Raw Output

{
  "field": "description"
}
Verifier uses supported plain-text characters
Verifier contains only supported plain-text ASCII characters

Raw Output

{
  "field": "verifier"
}
Prompt sanity checks (AI, up to 1 min)

Raw Output

{
  "all_issues": "",
  "no_urls_in_description": {
    "explanation": "No web URLs detected in the description; only local paths, commands, and filenames are present.",
    "status": "OK"
  },
  "observable_success_requirements": {
    "explanation": "The prompt defines concrete, verifiable outcomes: helm lint must succeed and helm template must render exactly one PVC with precise names in specified namespaces, with the workload referencing the same claim. These are observable via the provided commands.",
    "status": "OK"
  }
}

Prompt contains only necessary information (AI, up to 2 min)
**Suggestions for improvement** — These are AI-generated suggestions, not hard rules.

- [HIGH] Remove: “You are working on Linux in `/app/helm-charts-editor`.” This environment/path info isn’t needed to implement or verify the fix.
- [HIGH] Remove repo-shape and sibling-directories caveat: “The workspace is a trimmed local snapshot… Please do NOT edit them.” Keep only “The target chart is `charts/mlflow`.” The layout is discoverable; the “do not edit” warning is redundant with requirement 9.
- [HIGH] Remove the entire “Installed tools” list — tool availability is implied and the concrete verification steps are already specified later.
- [MEDIUM] Remove the first “Important scope note” bullet about not requiring a cluster and using helm lint/template — requirements 6–8 already define lint/template as the authoritative checks with exact commands.
- [HIGH] Remove the “Useful commands” block — it duplicates the explicit acceptance criteria in requirements 6–8 (same commands).

*Only high-severity issues are blocking. Medium and low severity suggestions are optional.*

Raw Output

{
  "status_reasoning": "There are 5 suggestions total, including multiple high-priority removals (environment path, repo-shape/sibling dirs note, installed tools list, and duplicate commands). With 3+ suggestions and high-priority items, the correct verdict is request_changes.",
  "suggestions": [
    {
      "priority": "high",
      "quote": "You are working on Linux in `/app/helm-charts-editor`.",
      "suggestion": "Remove entirely — environment path/OS details are unnecessary for solving the task and add noise."
    },
    {
      "priority": "high",
      "quote": "The workspace is a trimmed local snapshot of the original `helm-charts-editor` repo shape. The target chart is `charts/mlflow`. Sibling chart directories are present only to preserve the workspace layout; Please do NOT edit them.",
      "suggestion": "Remove the repo-shape and sibling-directories sentences (keep only “The target chart is `charts/mlflow`. ”). The repo layout is discoverable from the codebase and the “do not edit” warning is redundant with requirement 9."
    },
    {
      "priority": "high",
      "quote": "Installed tools:\n\n- `helm`\n- `kubectl`\n- `kind`\n- `python3`\n- `bash`",
      "suggestion": "Remove the entire installed tools list — availability is implied by the provided commands and environment; not needed in the task description."
    },
    {
      "priority": "medium",
      "quote": "Important scope note\n\n- This bundle keeps the real Helm chart debugging surface but does not require a live running Kubernetes cluster. Use `helm lint` and `helm template` as the authoritative verification path.",
      "suggestion": "Remove this bullet — it’s redundant with requirements 6–8 which already define lint/template as the verification path and show usage with namespaces."
    },
    {
      "priority": "high",
      "quote": "Useful commands:\n\n```bash\nhelm lint charts/mlflow\nhelm template mlflow-test charts/mlflow --namespace mlflow-test2\nhelm template prod-check charts/mlflow --namespace prod-space\n```",
      "suggestion": "Remove this block — these commands are already specified as acceptance criteria in requirements 6–8, so this duplicates information."
    }
  ],
  "summary": "- [HIGH] Remove: “You are working on Linux in `/app/helm-charts-editor`.” This environment/path info isn’t needed to implement or verify the fix.\n- [HIGH] Remove repo-shape and sibling-directories caveat: “The workspace is a trimmed local snapshot… Please do NOT edit them.” Keep only “The target chart is `charts/mlflow`.” The layout is discoverable; the “do not edit” warning is redundant with requirement 9.\n- [HIGH] Remove the entire “Installed tools” list — tool availability is implied and the concrete verification steps are already specified later.\n- [MEDIUM] Remove the first “Important scope note” bullet about not requiring a cluster and using helm lint/template — requirements 6–8 already define lint/template as the authoritative checks with exact commands.\n- [HIGH] Remove the “Useful commands” block — it duplicates the explicit acceptance criteria in requirements 6–8 (same commands).",
  "verdict": "request_changes"
}

---

WORKDIR is set to /app/helm-charts-editor rather than /app. While the workspace is placed under /app and the resulting container will be usable (you can operate inside /app/helm-charts-editor), this deviates from the guideline that the environment SHOULD use /app as the working directory. Because the workspace still lives under /app, this is a warning rather than an error.

The Dockerfile downloads and executes an external install script (curl -fsSL https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3 | bash) and downloads binaries from remote URLs without checksum verification. Downloading-and-piping remote scripts to a shell and fetching binaries without verifying checksums can be risky and reduce build reproducibility and trust. This should be justified or replaced with pinned, verified releases and checksum validation. Also note the build requires network access to fetch those artifacts (which is allowed at build time but makes builds brittle if upstream resources change). No obfuscated payloads or obvious malicious behavior detected.

Note: Internet access is available during `docker build`, but not when running the container. Ensure the Dockerfile installs everything needed for the environment to work offline after build.

Raw Output

{
  "all_issues": "WORKDIR is set to /app/helm-charts-editor rather than /app. While the workspace is placed under /app and the resulting container will be usable (you can operate inside /app/helm-charts-editor), this deviates from the guideline that the environment SHOULD use /app as the working directory. Because the workspace still lives under /app, this is a warning rather than an error.\n\nThe Dockerfile downloads and executes an external install script (curl -fsSL https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3 | bash) and downloads binaries from remote URLs without checksum verification. Downloading-and-piping remote scripts to a shell and fetching binaries without verifying checksums can be risky and reduce build reproducibility and trust. This should be justified or replaced with pinned, verified releases and checksum validation. Also note the build requires network access to fetch those artifacts (which is allowed at build time but makes builds brittle if upstream resources change). No obfuscated payloads or obvious malicious behavior detected.",
  "base_image_compliant": {
    "explanation": "FROM debian:trixie is a reasonable, modern Debian base image. It does not enforce a specific private base image and is compatible with apt-based package installation used later in the Dockerfile.",
    "status": "OK"
  },
  "dependencies_installed": {
    "explanation": "The Dockerfile installs relevant system packages via apt (bash, ca-certificates, curl, git, jq, python3, python3-yaml, tar, gzip) and fetches Helm (via the upstream install script), kubectl v1.35.2, and kind v0.31.0 placing them in /usr/local/bin. These provide common tooling needed for Kubernetes/Helm tasks and the workspace copied into /app/helm-charts-editor will have these tools available at runtime.",
    "status": "OK"
  },
  "environment_setup": {
    "explanation": "WORKDIR is set to /app/helm-charts-editor rather than /app. While the workspace is placed under /app and the resulting container will be usable (you can operate inside /app/helm-charts-editor), this deviates from the guideline that the environment SHOULD use /app as the working directory. Because the workspace still lives under /app, this is a warning rather than an error.",
    "status": "warning"
  },
  "interactive_shell": {
    "explanation": "CMD [\"/bin/bash\"] is provided and WORKDIR is set to /app/helm-charts-editor, so launching the container will place a user in the workspace. The solver can interact with the files under /app. This satisfies the requirement for a usable interactive workspace.",
    "status": "OK"
  },
  "runtime_validation": {
    "explanation": "No heavy tests or hidden verifier files are run during build. The Dockerfile initializes a git repository and commits the copied workspace, which is a lightweight seed step and benign. The build does rely on network fetches to obtain helm, kubectl, and kind, but the resulting image contains those tools and should work offline at runtime.",
    "status": "OK"
  },
  "security_safety": {
    "explanation": "The Dockerfile downloads and executes an external install script (curl -fsSL https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3 | bash) and downloads binaries from remote URLs without checksum verification. Downloading-and-piping remote scripts to a shell and fetching binaries without verifying checksums can be risky and reduce build reproducibility and trust. This should be justified or replaced with pinned, verified releases and checksum validation. Also note the build requires network access to fetch those artifacts (which is allowed at build time but makes builds brittle if upstream resources change). No obfuscated payloads or obvious malicious behavior detected.",
    "status": "warning"
  }
}
