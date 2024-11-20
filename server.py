import socket
import threading
import sqlite3

# Funzione per gestire ogni richiesta del client
def handle_client(client_socket):
    # Crea una connessione separata al database per questo thread
    conn = sqlite3.connect('file.db')

    try:
        while True:
            # Ricevi la richiesta dal client
            request = client_socket.recv(1024).decode('utf-8')
            if not request:
                break
            
            # Interpreta la richiesta
            parts = request.split()
            command = parts[0]
            
            if command == "FILE_EXIST":
                filename = parts[1]
                result = file_exists(conn, filename)
                client_socket.send(result.encode())
            
            elif command == "FILE_FRAGMENTS":
                filename = parts[1]
                result = file_fragments(conn, filename)
                client_socket.send(result.encode())
            
            elif command == "FRAGMENT_IP":
                filename = parts[1]
                fragment_number = int(parts[2])
                result = fragment_ip(conn, filename, fragment_number)
                client_socket.send(result.encode())
            
            elif command == "ALL_FRAGMENTS_IP":
                filename = parts[1]
                result = all_fragments_ip(conn, filename)
                client_socket.send(result.encode())
            else: 
                result = "Errore! Hai scritto un comando non presente"
                client_socket.send(result.encode())
            
    finally:
        client_socket.close()
        #conn.close()  # Chiudi la connessione al DB dopo che il client ha terminato
        
# Funzione per verificare se il file esiste
def file_exists(conn, filename):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM files WHERE nome=?", (filename,))
    row = cursor.fetchone()
    return "OK" if row else "NOT_FOUND"

# Funzione per ottenere il numero di frammenti di un file
def file_fragments(conn, filename):
    cursor = conn.cursor()
    cursor.execute("SELECT tot_frammenti FROM files WHERE nome=?", (filename,))
    row = cursor.fetchone()
    return str(row[0]) if row else "NOT_FOUND"

# Funzione per ottenere l'IP di un frammento
def fragment_ip(conn, filename, fragment_number):
    cursor = conn.cursor()
    cursor.execute("""
        SELECT f.host 
        FROM frammenti AS f
        INNER JOIN files AS fi ON fi.id_file = f.id_file
        WHERE fi.nome=? AND f.n_frammento=?
    """, (filename, fragment_number))
    row = cursor.fetchone()
    return row[0] if row else "NOT_FOUND"

# Funzione per ottenere tutti gli IP dei frammenti
def all_fragments_ip(conn, filename):
    cursor = conn.cursor()
    cursor.execute("""
        SELECT f.host 
        FROM frammenti AS f
        INNER JOIN files AS fi ON fi.id_file = f.id_file
        WHERE fi.nome=?
    """, (filename,))
    rows = cursor.fetchall()
    return ', '.join([row[0] for row in rows]) if rows else "NOT_FOUND"

# Funzione per avviare il server
def start_server():
    # Crea il socket del server
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('0.0.0.0', 9999))
    server.listen(5)
    print("Server in ascolto sulla porta 9999...")

    # Gestisce le connessioni dei client
    while True:
        client_socket, addr = server.accept()
        print(f"Connessione stabilita con {addr}")
        client_handler = threading.Thread(target=handle_client, args=(client_socket,))
        client_handler.start()

if __name__ == "__main__":
    start_server()
    
