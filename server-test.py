import socket
import time
import subprocess


def start_server():
    host = 'localhost'  # Server address
    port = 12345        # Server port

    server_socket = socket.socket()
    server_socket.bind((host, port))

    server_socket.listen(1)
    print("Server listening...")
    script_path = '/home/pi/openAI-rpi-11labs-test/test-neopixel.py' 
    subprocess.Popen(['sudo', 'python3', script_path])

    conn, addr = server_socket.accept()
    print(f"Connection from: {addr}")

    try:
        while True:
            # Send different messages
            for message in ["sht", "ask", "spk", "done"]:
                conn.send(message.encode())
                print(message)
                time.sleep(5)  # Wait for 2 seconds before sending the next message
    except KeyboardInterrupt:
        conn.close()  # Close the connection on interrupt




if __name__ == '__main__':
    start_server()


