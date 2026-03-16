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
    && rm -rv /var/lib/apt/lists/*

RUN curl -fsSL https://get.helm.sh/helm-v3.20.1-linux-amd64.tar.gz -o helm-v3.20.1-linux-amd64.tar.gz \
    && curl -fsSL https://get.helm.sh/helm-v3.20.1-linux-amd64.tar.gz.sha256sum -o helm-v3.20.1-linux-amd64.tar.gz.sha256sum \
    && sha256sum --check helm-v3.20.1-linux-amd64.tar.gz.sha256sum \
    && tar xvzf helm-v3.20.1-linux-amd64.tar.gz \
    && mv linux-amd64/helm /usr/local/bin \
    && chmod +x /usr/local/bin/helm \
    && rm -rv linux-amd64 helm-v3.20.1-linux-amd64.tar.gz helm-v3.20.1-linux-amd64.tar.gz.sha256sum \
    && curl -fsSL https://dl.k8s.io/v1.35.1/bin/linux/amd64/kubectl -o kubectl \
    && curl -fsSL https://dl.k8s.io/v1.35.1/bin/linux/amd64/kubectl.sha256 -o kubectl.sha256 \
    && echo "$(cat kubectl.sha256)  kubectl" | sha256sum --check \
    && mv kubectl /usr/local/bin/kubectl \
    && chmod +x /usr/local/bin/kubectl \
    && rm -v kubectl.sha256 \
    && curl -fsSL https://kind.sigs.k8s.io/dl/v0.31.0/kind-linux-amd64 -o kind-linux-amd64 \
    && curl -fsSL https://kind.sigs.k8s.io/dl/v0.31.0/kind-linux-amd64.sha256sum -o kind-linux-amd64.sha256sum \
    && sha256sum --check kind-linux-amd64.sha256sum \
    && mv kind-linux-amd64 /usr/local/bin/kind \
    && chmod +x /usr/local/bin/kind \
    && rm -v kind-linux-amd64.sha256sum

WORKDIR /app/helm-charts-editor

COPY helm-charts-editor/ /app/helm-charts-editor/

RUN git init >/dev/null 2>&1 \
    && git config user.email task@example.com \
    && git config user.name "Task Seed" \
    && git add . \
    && git commit -m "seed task workspace" >/dev/null 2>&1 || true

CMD ["/bin/bash"]
