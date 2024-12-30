FROM python:3.8-slim

WORKDIR /

RUN apt-get update && apt-get install -y \
    ffmpeg \
    curl \
    build-essential \
    pkg-config \
    libavformat-dev \
    libavcodec-dev \
    libavdevice-dev \
    libavutil-dev \
    libswscale-dev \
    libswresample-dev \
    libavfilter-dev

# tokenizers (a dependency of faster-whisper) requires Rust to be installed for compilation
RUN curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs |  sh -s -- --default-toolchain 1.83.0 -y \
    && . $HOME/.cargo/env

ENV PATH="/root/.cargo/bin:${PATH}"

RUN pip install --upgrade pip && \
    pip install --no-cache-dir tokenizers==0.13.3 && \
    pip install --no-cache-dir av==11.0.0 && \
    pip install --no-cache-dir numpy && \
    pip install --no-cache-dir pydub && \
    pip install --no-cache-dir faster-whisper && \
    pip install --no-cache-dir moviepy

ENTRYPOINT ["python"]
