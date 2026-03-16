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
    && echo "0165ee4a2db012cc657381001e593e981f42aa5707acdd50658326790c9d0dc3  helm-v3.20.1-linux-amd64.tar.gz" | sha256sum --check \
    && tar xvzf helm-v3.20.1-linux-amd64.tar.gz \
    && mv linux-amd64/helm /usr/local/bin \
    && chmod +x /usr/local/bin/helm \
    && rm -rv linux-amd64 helm-v3.20.1-linux-amd64.tar.gz \
    && curl -fsSL https://dl.k8s.io/v1.35.1/bin/linux/amd64/kubectl -o kubectl \
    && echo "36e2f4ac66259232341dd7866952d64a958846470f6a9a6a813b9117bd965207  kubectl" | sha256sum --check \
    && mv kubectl /usr/local/bin/kubectl \
    && chmod +x /usr/local/bin/kubectl \
    && curl -fsSL https://kind.sigs.k8s.io/dl/v0.31.0/kind-linux-amd64 -o kind-linux-amd64 \
    && echo "eb244cbafcc157dff60cf68693c14c9a75c4e6e6fedaf9cd71c58117cb93e3fa  kind-linux-amd64" | sha256sum --check \
    && mv kind-linux-amd64 /usr/local/bin/kind \
    && chmod +x /usr/local/bin/kind

WORKDIR /app

COPY helm-charts-editor/ /app/

RUN git init >/dev/null 2>&1 \
    && git config user.email task@example.com \
    && git config user.name "Task Seed" \
    && git add . \
    && git commit -m "seed task workspace" >/dev/null 2>&1 || true

CMD ["/bin/bash"]
