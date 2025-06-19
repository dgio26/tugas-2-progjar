from socket import *
import socket
import threading
import logging
import time
import sys
from datetime import datetime

class ProcessTheClient(threading.Thread):
    def __init__(self, connection, address):
        self.connection = connection
        self.address = address
        threading.Thread.__init__(self)
    
    def run(self):
        logging.warning(f"Handling client {self.address}")
        try:
            while True:
                data = self.connection.recv(1024)
                if not data:
                    break
                
                request = data.decode('utf-8').strip()
                logging.warning(f"Request dari {self.address}: {request}")
                
                if request.upper().startswith('QUIT'):
                    logging.warning(f"Client {self.address} memutuskan koneksi")
                    break
                
                if request.upper().startswith('TIME'):
                    current_time = datetime.now().strftime('%H:%M:%S')

                    response = f"JAM {current_time}\r\n"
                    
                    self.connection.sendall(response.encode('utf-8'))
                    logging.warning(f"Response ke {self.address}: JAM {current_time}")
                else:
                    error_response = "ERROR: Request tidak valid\r\n"
                    self.connection.sendall(error_response.encode('utf-8'))
                    logging.warning(f"Invalid request dari {self.address}: {request}")
                    
        except Exception as e:
            logging.error(f"Error menangani client {self.address}: {e}")
        finally:
            self.connection.close()
            logging.warning(f"Koneksi dengan {self.address} ditutup")

class Server(threading.Thread):
    def __init__(self):
        self.the_clients = []
        self.my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.my_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        threading.Thread.__init__(self)
    
    def run(self):
        self.my_socket.bind(('0.0.0.0', 45000))
        self.my_socket.listen(5)
        
        logging.warning("Time Server berjalan di port 45000")
        logging.warning("Menunggu koneksi client...")
        
        while True:
            try:
                self.connection, self.client_address = self.my_socket.accept()
                logging.warning(f"connection from {self.client_address}")
                
                clt = ProcessTheClient(self.connection, self.client_address)
                clt.start()
                self.the_clients.append(clt)
                
            except Exception as e:
                logging.error(f"Error menerima koneksi: {e}")
                break

def main():
    logging.basicConfig(
        level=logging.WARNING,
        format='%(asctime)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    svr = Server()
    try:
        svr.start()
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        logging.warning("Server dihentikan oleh user")
        sys.exit(0)

if __name__ == "__main__":
    main()
