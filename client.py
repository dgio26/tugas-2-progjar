import socket

class TimeClient:
    def __init__(self, host='172.16.16.101', port=45000):
        self.host = host
        self.port = port
        self.client_socket = None
    
    def connect_to_server(self):
        """Membuat koneksi ke server"""
        try:
            self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client_socket.connect((self.host, self.port))
            print(f"Terhubung ke server {self.host}:{self.port}")
            return True
        except Exception as e:
            print(f"Error koneksi ke server: {e}")
            return False
    
    def send_request(self, request):
        """Mengirim request ke server"""
        try:
            formatted_request = request + "\r\n"
            self.client_socket.send(formatted_request.encode('utf-8'))
            response = self.client_socket.recv(1024)
            return response.decode('utf-8').strip()
        except Exception as e:
            print(f"Error mengirim request: {e}")
            return None
    
    def get_time(self):
        """Meminta waktu dari server"""
        response = self.send_request("TIME")
        if response:
            print(f"Response dari server: {response}")
        return response
    
    def quit_connection(self):
        """Mengirim QUIT dan menutup koneksi"""
        self.send_request("QUIT")
        if self.client_socket:
            self.client_socket.close()
        print("Koneksi ditutup")

def main():
    client = TimeClient()
    
    if not client.connect_to_server():
        return
    
    try:
        while True:
            command = input("\nMasukkan perintah (TIME/QUIT): ").strip()
            
            if command.upper() == 'QUIT':
                client.quit_connection()
                break
            elif command.upper() == 'TIME':
                client.get_time()
            else:
                print("Perintah tidak valid. Gunakan TIME atau QUIT")
                
    except KeyboardInterrupt:
        print("\nProgram dihentikan")
        client.quit_connection()

if __name__ == "__main__":
    main()
