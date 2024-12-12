# Użycie obrazu Pythona 3.9
FROM python:3.9-slim

# Instalacja zależności systemowych (cron i wget)
RUN apt-get update && apt-get install -y cron wget && rm -rf /var/lib/apt/lists/*

# Ustawienie katalogu roboczego w kontenerze
WORKDIR /app

# Skopiowanie pliku requirements.txt i zainstalowanie zależności
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Skopiowanie skryptu Python do kontenera
COPY database_update.py /app/

# Skopiowanie pliku crontab do folderu cron.d
COPY cronjob /etc/cron.d/cronjob

# Ustawienie odpowiednich uprawnienien do pliku cronjob
RUN chmod 0644 /etc/cron.d/cronjob && crontab /etc/cron.d/cronjob

# Uruchomienie cron oraz logowanie
CMD cron && tail -f /var/log/cron.log
