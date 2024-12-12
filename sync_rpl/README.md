#TAKIEGO POLECENIA UżYJCIE DLA ZBUDOWANIA OBRAZU
docker build -t my-python-cron-image . 

#uruchomienie kontenera zbudowanego z obrazu
docker run -it --name my-python-cron-container my-python-cron-image bash

#sprawdzenie czy cron jest uruchomiony
ps aux | grep cron

#włączenie usługi cron w systemie
service cron start

#wyświetlenie aktualnie zaplanowanych zadań cron
crontab -l 
