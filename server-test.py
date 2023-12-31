import socket
import time
import subprocess

client_process = None

def start_server():
    host = 'localhost'  # Server address
    port = 12345        # Server port

    server_socket = socket.socket()
    server_socket.bind((host, port))

    server_socket.listen(1)
    print("Server listening...")
    script_path = '/home/pi/openAI-rpi-11labs-test/test-neopixel.py' 
    global client_process
    client_process = subprocess.Popen(['sudo', 'python3', script_path])

    try:
        # Wait for the client to connect
        conn, addr = server_socket.accept()
        print(f"Connection from: {addr}")

        # Server's main loop
        while True:
            # Send different messages
            for message in ["sht", "ask", "spk", "done"]:
                conn.send(message.encode())
                
                time.sleep(5)  # Wait for 2 seconds before sending the next message
    
    except KeyboardInterrupt:
        print("Keyboard interrupt received, shutting down.")
        try:
            print("wtfffffff")
            conn.send('shtd'.encode())  # Send shutdown command to client
        finally:
            time.sleep(1)
            conn.close()
            server_socket.close()
            print("did u do this??")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == '__main__':
    start_server()


