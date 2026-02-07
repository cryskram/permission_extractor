FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y \
    openjdk-17-jdk \
    apktool \
    python3 \
    python3-pip \
    unzip \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY analyze.py .

ENTRYPOINT [ "python3", "analyze.py" ]