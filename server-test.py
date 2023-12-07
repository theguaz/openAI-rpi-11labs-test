import socket
import time



def start_server():
    host = 'localhost'  # Server address
    port = 12345        # Server port

    server_socket = socket.socket()
    server_socket.bind((host, port))

    server_socket.listen(1)
    print("Server listening...")

    conn, addr = server_socket.accept()
    print(f"Connection from: {addr}")

    try:
        while True:
            # Send different messages
            for message in ["sht", "ask", "spk", "done"]:
                conn.send(message.encode())
                time.sleep(5)  # Wait for 2 seconds before sending the next message
    except KeyboardInterrupt:
        conn.close()  # Close the connection on interrupt

if __name__ == '__main__':
    start_server()
    
