FROM python:3.12-slim
RUN apt-get update && apt-get install -y --no-install-recommends dnsutils \
    && rm -rf /var/lib/apt/lists/* \
    && pip install --no-cache-dir flask==3.0.3
RUN echo "CTF{c0mmand_1njection_pwn3d}" > /flag.txt
WORKDIR /app
COPY . .
EXPOSE 5000
CMD ["python", "app.py"]
