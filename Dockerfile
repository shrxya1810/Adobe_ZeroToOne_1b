FROM --platform=linux/amd64 python:3.9.13-slim
WORKDIR /app

# Install git-lfs for model downloading
RUN apt-get update && apt-get install -y git git-lfs && \
    git lfs install && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install -U sentence-transformers

# Download the model during build
RUN mkdir -p models && \
    git clone https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2 models/all-MiniLM-L6-v2

COPY . .
CMD ["python", "main.py"]
