### Questo script ha la funzione di monitorare il Server A (Quello principale) e spostare l'IP Failover in caso esso dovesse andare giù.

import requests
from requests.auth import HTTPBasicAuth

# --- CONFIG SEMPLICE (metti i tuoi valori qui) ---
ROBOT_USER = "MAIL HETZNER" 
ROBOT_PASS = "PASSWORD HETZNER" 

FAILOVER_IP = "FAILOVER IP"       #Failover IP  
SERVER_A_IP = "IP SERVER A"     #IP principale Server A 
SERVER_B_IP = "IP SERVER B"      #IP principale Server B 

HEALTH_URL_A = "http://IP SERVER A/"   
TIMEOUT_S = 5
ALLOW_FAILBACK = True              #se True, quando A torna ON, rimetti il failover su A

BASE = "https://robot-ws.your-server.de"
auth = HTTPBasicAuth(ROBOT_USER, ROBOT_PASS)

### FUNZIONE PER CONTROLLARE SE IL SERVER PRINCIPALE E' ATTIVO:
def a_is_healthy():
    try:
        #Manda una richiesta get, all'url dichiarato all'inizio e se la risposta è compresa tra 200 e 400 allora ritorna true
        r = requests.get(HEALTH_URL_A, timeout=TIMEOUT_S)
        return 200 <= r.status_code < 400
        #Altrimenti false
    except Exception:
        return False

### FUNZIONE PER VEDERE IN CHE SERVER E' ATTIVO E' IL FAILOVER:
def get_active():
    #Chiama Endpoint dell'API per vedere dov'è attivo il Failover
    r = requests.get(f"{BASE}/failover/{FAILOVER_IP}", auth=auth, timeout=10)
    #Uso un metodo di Request, se lo status HTTP è 4xx o 5xx, solleva requests.exceptions.HTTPError
    r.raise_for_status()
    #Ritorna il json con il server che hai il failover attivo
    return r.json()["failover"]["active_server_ip"]  

### FUNZIONE PER ATTIVARE IL FILEOVER SU UN SERVER SPECIFICO:
def set_active(target_ip):
    #Chiama l'Endpoint dell'API per attivare il Failover sul il Server inserito
    r = requests.post(f"{BASE}/failover/{FAILOVER_IP}",
                      auth=auth,
                      data={"active_server_ip": target_ip},
                      timeout=10)
    #Uso un metodo di Request, se lo status HTTP è 4xx o 5xx, solleva requests.exceptions.HTTPError
    r.raise_for_status()

def main():
    try:
        #Guarda in quale server è attivo il Failover
        active = get_active()
    except Exception as e:
        print(f"[ERRORE] Lettura stato API: {e}")
        return

    print(f"[INFO] Failover attivo su: {active}")

    #Checka se il Server A è attivo o meno
    healthy = a_is_healthy()
    print(f"[INFO] Server A health: {'OK' if healthy else 'KO'}")

    #Se A è KO e non è già attivo B >>> sposta su B
    if not healthy and active != SERVER_B_IP:
        try:
            set_active(SERVER_B_IP)
            print(f"[ACTION] Switch su B: {SERVER_B_IP}")
        except Exception as e:
            print(f"[ERRORE] Switch su B fallito: {e}")
        return

    #Se A è OK e vogliamo failback su A
    if healthy and ALLOW_FAILBACK and active != SERVER_A_IP:
        try:
            set_active(SERVER_A_IP)
            print(f"[ACTION] Failback su A: {SERVER_A_IP}")
        except Exception as e:
            print(f"[ERRORE] Failback su A fallito: {e}")
        return

    print("[INFO] Nessuna azione necessaria.")

if __name__ == "__main__":
    main()