# Image de base volontairement ancienne pour que Trivy détecte des CVE (étape 1 du TP).
# Correction à faire plus tard : passer à python:3.12-slim (voir GUIDE.md, section 4.4)
FROM python:3.11-buster

WORKDIR /app
COPY app/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app/ .
EXPOSE 5000
CMD ["python", "app.py"]
