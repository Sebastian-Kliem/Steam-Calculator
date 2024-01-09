FROM python:3.8

# Setzen des Arbeitsverzeichnisses im Container
WORKDIR /app

# Kopieren der requirements.txt und Installation der Abhängigkeiten
COPY app/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Kopieren des app-Verzeichnisses in den Container
COPY app/ /app/

