ARG PG_TAG=15-bullseye

FROM postgres:${PG_TAG}

RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    ca-certificates \
    daemontools \
    lzop \
    pv \
    && rm -rf /var/lib/apt/lists/*

ARG WALG_VERSION=v2.0.1
ARG OS_VERSION=ubuntu-20.04

RUN curl -L "https://github.com/wal-g/wal-g/releases/download/${WALG_VERSION}/wal-g-pg-${OS_VERSION}-amd64.tar.gz" \
    | tar -xz -C /usr/local/bin/ \
    && mv /usr/local/bin/wal-g-pg-${OS_VERSION}-amd64 /usr/local/bin/wal-g

COPY restore-entrypoint.sh /usr/local/bin/restore-entrypoint.sh
RUN chmod +x /usr/local/bin/restore-entrypoint.sh

ENTRYPOINT ["/usr/local/bin/restore-entrypoint.sh"]
CMD ["postgres"]