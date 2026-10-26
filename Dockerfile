FROM python:3.10-slim

WORKDIR /app

# 安装系统依赖
RUN apt-get update && apt-get install -y \
    ffmpeg \
    libsndfile1 \
    libgl1-mesa-glx \
    libglib2.0-0 \
    git \
    && rm -rf /var/lib/apt/lists/*

# 克隆SadTalker
RUN git clone https://github.com/OpenTalker/SadTalker.git .

# 安装Python依赖
RUN pip install --no-cache-dir torch==2.1.0 torchvision==0.16.0 torchaudio==2.1.0 --index-url https://download.pytorch.org/whl/cpu

RUN pip install --no-cache-dir \
    gradio==3.44.0 \
    numpy==1.24.0 \
    scipy==1.11.0 \
    librosa==0.10.0 \
    opencv-python==4.8.0 \
    Pillow==10.0.0 \
    tqdm==4.66.0 \
    gfpgan==1.3.8 \
    basicsr==1.4.2 \
    facexlib==0.3.0 \
    transformers==4.35.0 \
    huggingface_hub==0.20.0 \
    TTS==0.21.0 \
    numba==0.58.0 \
    scikit-image==0.21.0 \
    imageio==2.31.0 \
    soundfile==0.12.1 \
    pydub==0.25.1

# 预下载模型（第一次启动自动下载）
ENV COQUI_TOS_AGREED=1

EXPOSE 7860

CMD ["python", "app_sadtalker.py"]
