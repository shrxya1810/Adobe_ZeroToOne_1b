
FROM --platform=linux/amd64 python:3.9-slim

WORKDIR /app
COPY . /app

RUN pip install --no-cache-dir torch==2.2.2+cpu --extra-index-url https://download.pytorch.org/whl/cpu

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "main.py"]
