FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive

# System dependencies ইনস্টল করুন
RUN apt-get update && apt-get install -y \
    python3 python3-pip openjdk-17-jdk git wget unzip \
    build-essential autoconf automake libtool pkg-config zlib1g-dev \
    libssl-dev libffi-dev cmake && \
    apt-get clean

# Non-root user তৈরি করুন
RUN useradd -m -U builder
USER builder
WORKDIR /home/builder

# Buildozer PATH-এ যোগ করুন
ENV PATH="/home/builder/.local/bin:${PATH}"

# Buildozer non-root user হিসেবে ইনস্টল করুন
RUN pip3 install --user buildozer cython==0.29.33

WORKDIR /home/builder/app
