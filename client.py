import socket

def send_request(request):
    # Connessione al server
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(('localhost', 9999))
    
    # Invia la richiesta al server
    client.send(request.encode())
    
    # Ricevi la risposta dal server
    response = client.recv(1024).decode('utf-8')
    
    # Stampa la risposta
    print(f"Risposta server: {response}")
    
    # Chiudi la connessione
    client.close()

if __name__ == "__main__":
    while True:
        # Chiedi all'utente di inserire una richiesta
        request = input("Inserisci la tua richiesta (oppure 'exit' per uscire): ")
        if request.lower() == "exit":
            break
        send_request(request)
    

# Messaggi Client->Server:

# Verifica se il file esiste:
# Formato: "FILE_EXIST nome_file"
# Descrizione: Chiede al server se il file con il nome specificato è presente nel database.
# RISPOSTA"
# Descrizione: Il server risponde con "OK" se il file esiste, altrimenti con "NOT_FOUND".

# Recupera il numero di frammenti di un file:
# Formato: "FILE_FRAGMENTS nome_file"
# Descrizione: Chiede al server il numero totale di frammenti in cui è suddiviso un file.
# RISPOSTA"
# Descrizione: Il server risponde con il numero di frammenti o con "NOT_FOUND" se il file non esiste.

# Recupera l'IP del frammento:
# Formato: "FRAGMENT_IP nome_file numero_frammento"
# Descrizione: Chiede al server l'indirizzo IP dell'host che ospita un determinato frammento di un file.
# RISPOSTA"
# Descrizione: Il server risponde con l'IP dell'host che ospita il frammento o con "NOT_FOUND" se il frammento non esiste.

# Recupera tutti gli IP degli host che ospitano i frammenti di un file:
# Formato: "ALL_FRAGMENTS_IP nome_file"
# Descrizione: Chiede al server tutti gli indirizzi IP degli host che ospitano i frammenti di un determinato file.
# RISPOSTA"
# Descrizione: Il server risponde con una lista di indirizzi IP separati da virgola o con "NOT_FOUND" se non esistono frammenti per quel file.


