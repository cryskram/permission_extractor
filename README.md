# Android APK Permission Extractor

Extracts declared permissions from an Android APK using a Dockerized static analysis pipeline



## Installation & Usage

Build the Docker image:

```bash
docker build -t apk-analyzer .
```

Place your apk in the current directory(or use the one present here for dummy) and run:

```bash
docker run --rm -v $(pwd):/data apk-analyzer /data/app-release.apk
```

