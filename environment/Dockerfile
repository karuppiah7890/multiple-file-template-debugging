FROM debian:trixie

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y --no-install-recommends \
    bash \
    ca-certificates \
    curl \
    git \
    jq \
    python3 \
    python3-yaml \
    tar \
    gzip \
    && rm -rf /var/lib/apt/lists/*

RUN curl -fsSL https://get.helm.sh/helm-v3.20.1-linux-amd64.tar.gz -o helm-v3.20.1-linux-amd64.tar.gz \
    && curl -fsSL https://get.helm.sh/helm-v3.20.1-linux-amd64.tar.gz.sha256sum -o helm-v3.20.1-linux-amd64.tar.gz.sha256sum
    && sha256sum -c helm-v3.20.1-linux-amd64.tar.gz.sha256sum
    && rm -fv helm-v3.20.1-linux-amd64.tar.gz.sha256sum
    && mv linux-amd64/helm /usr/local/bin
    && chmod +x /usr/local/bin/helm
    && rm -rfv linux-amd64 helm-v3.20.1-linux-amd64.tar.gz helm-v3.20.1-linux-amd64.tar.gz.sha256sum
    && curl -fsSL https://dl.k8s.io/v1.35.1/bin/linux/amd64/kubectl.sha256 -o kubectl.sha256 \
    && sha256sum -c kubectl.sha256
    && mv kubectl /usr/local/bin/kubectl
    && chmod +x /usr/local/bin/kubectl \
    && curl -fsSL https://kind.sigs.k8s.io/dl/v0.31.0/kind-linux-amd64 -o /usr/local/bin/kind \
    && chmod +x /usr/local/bin/kind

WORKDIR /app/helm-charts-editor

COPY helm-charts-editor/ /app/helm-charts-editor/

RUN git init >/dev/null 2>&1 \
    && git config user.email task@example.com \
    && git config user.name "Task Seed" \
    && git add . \
    && git commit -m "seed task workspace" >/dev/null 2>&1 || true

CMD ["/bin/bash"]
