FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive

# একবারেই সব dependencies install করুন
RUN apt-get update && apt-get install -y \
    python3 python3-pip git wget unzip \
    openjdk-17-jdk autoconf automake libtool \
    pkg-config zlib1g-dev cmake ninja-build \
    build-essential && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Non-root user setup
RUN useradd -m -u 1001 builder
USER builder
WORKDIR /home/builder

# Buildozer এবং dependencies একসাথে install
RUN pip3 install --user buildozer cython
ENV PATH="/home/builder/.local/bin:${PATH}"

WORKDIR /home/builder/app
