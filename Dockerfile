FROM python:3.10-slim

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends 
    ffmpeg 
    libsndfile1 
    libgl1 
    libglib2.0-0 
    git 
    && rm -rf /var/lib/apt/lists/*

RUN git clone --depth 1 https://github.com/OpenTalker/SadTalker.git .

RUN pip install --no-cache-dir torch==2.1.0 torchvision==0.16.0 torchaudio==2.1.0 --index-url https://download.pytorch.org/whl/cpu

RUN pip install --no-cache-dir 
    gradio==3.44.0 
    numpy==1.24.0 
    scipy==1.11.0 
    librosa==0.10.0 
    opencv-python-headless==4.8.0 
    Pillow==10.0.0 
    tqdm==4.66.0 
    gfpgan==1.3.8 
    basicsr==1.4.2 
    facexlib==0.3.0 
    transformers==4.35.0 
    huggingface_hub==0.20.0 
    TTS==0.21.0 
    numba==0.58.0 
    scikit-image==0.21.0 
    imageio==2.31.0 
    imageio-ffmpeg==0.4.9 
    soundfile==0.12.1 
    pydub==0.25.1

ENV COQUI_TOS_AGREED=1
ENV PYTHONPATH=/app

EXPOSE 7860

CMD ["python", "app_sadtalker.py"]