# Hetzner Failover Monitor

Hetzner Failover Monitor è uno script Python progettato per monitorare lo stato del Server A (primario) e spostare automaticamente l’IP Failover su Server B in caso di malfunzionamento.
Quando il Server A torna operativo, lo script può effettuare automaticamente il failback.

## Funzionamento

Lo script effettua una richiesta HTTP al Server A per verificarne lo stato.
Se il Server A non risponde entro il timeout configurato, l’IP Failover viene spostato su Server B tramite le API Hetzner Robot. Quando il Server A torna online e l’opzione ALLOW_FAILBACK è abilitata, l’IP viene automaticamente riportato al Server A.

## Requisiti

- Python 3.x
- Accesso alle API Hetzner Robot
- Failover IP già configurato tra Server A e Server B
#### Libreria richiesta:

- pip install requests

## Configurazione

Apri il file e imposta i tuoi valori:

- ROBOT_USER = "YOUR_HETZNER_EMAIL"
- ROBOT_PASS = "YOUR_HETZNER_PASSWORD"
- FAILOVER_IP = "XXX.XXX.XXX.XXX"   # IP Failover Hetzner
- SERVER_A_IP = "XXX.XXX.XXX.XXX"   # IP primario
- SERVER_B_IP = "XXX.XXX.XXX.XXX"   # IP di backup
- HEALTH_URL_A = "http://<server-a-ip>/"
- TIMEOUT_S = Xsec
- ALLOW_FAILBACK = True

## Esecuzione

Esegui lo script manualmente:

```
python3 failoverHetzner.py
```
Oppure pianifica l’esecuzione automatica con cron o systemd:
```
*/2 * * * * /usr/bin/python3 /path/failoverHetzner.py >> /var/log/failover.log 2>&1
```
## Endpoint API Hetzner utilizzati
GET	/failover/<FAILOVER_IP>	Ottiene l’IP attualmente attivo

POST	/failover/<FAILOVER_IP>	Imposta un nuovo server attivo

## Documentazione ufficiale:
https://docs.hetzner.com/robot/dedicated-server/ip/failover/

