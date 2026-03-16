- Write down Prompt. Check existing files too, for prompts etc -

codex_env_prompt.txt
codex_events.jsonl
codex_last_message.md
codex_stderr.log
prompt.txt
review.md
scoping_notes.md

---

- Write down Scope-down Design Doc

Mention the following -
- ONLY look at the following files and change them. Following are the files to look at and change and they are present inside the `charts/mlflow` directory: pvc.yaml, deployment.yaml, values.yaml, values.schema.json. DO NOT change any other files or chart directories - basically DO NOT change any other files or directories other than the ones mentioned above.

- No speculative changes or structural changes. Fix ONLY Persistent Volume Claim (PVC) naming consistency. Basically - Speculative changes and structural changes are forbidden — only naming consistency fixes are allowed. 

---

Version 2:

- Use

```Dockerfile
FROM docker:stable-dind
```

Docker In Docker (DIND) and use `kind` or `k3d` - Kubernetes/K3s In Docker

Verify by running the helm chart in the Kubernetes cluster

```bash
helm template mlflow-test charts/mlflow --namespace mlflow-test2

helm install --wait --timeout 10m mlflow-test charts/mlflow --namespace mlflow-test2

helm template prod-check charts/mlflow --namespace prod-space

helm install --wait --timeout 10m prod-check charts/mlflow --namespace prod-space

```

The chart will only run if the following are proper
- No quotes around the port number in the deployment yaml's pod's container's args for command
- Namespace of the PVC is correct. In Helm 3, somehow, it takes release namespace as the namespace for resources when namespace is missing in the resource. In our case, PVC is missing the namespace field in the metadata
- Default Storage Class exists with support for dynamic PVC provisioning
- The PVC name is properly referred in the deployment yaml
