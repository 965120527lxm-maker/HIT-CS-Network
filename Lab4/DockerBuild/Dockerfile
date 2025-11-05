# Dockerfile
FROM debian:stable-slim

# 1) basic tools + python
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        python3 python3-pip \
        iproute2 iputils-ping tcpdump iptables \
        curl vim && \
    rm -rf /var/lib/apt/lists/*

# 2) make "python" point to python3
RUN ln -s /usr/bin/python3 /usr/bin/python

# 3) working dir
WORKDIR /lab

# 4) default: just give me a shell
CMD ["/bin/bash"]
