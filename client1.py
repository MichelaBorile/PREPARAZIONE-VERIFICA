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
