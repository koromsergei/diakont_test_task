import serial
import time
from common.M.config import HOST, PORT, ATTEMPTS_TO_RECONNECT, \
    TIME_TO_CONNECT, TIME_TO_RECONNECT, COM_SPEED, COM_TIMEOUT
import socket
from M2.shared_state import stop_sending_event

def receive_all_sock(conn, length):
    data = b""
    while len(data) < length:
        chunk = conn.recv(length - len(data))
        if not chunk:
            raise ConnectionError("Connection closed")
        data += chunk

    return data




def connect_to_socket(is_connected=None):
    attempt = 0
    while attempt < ATTEMPTS_TO_RECONNECT:
        try:
            with serial.Serial(
                                "COM3", 
                                COM_SPEED, 
                                bytesize=8,
                                parity=serial.PARITY_NONE,
                                stopbits=serial.STOPBITS_ONE,
                                timeout=COM_TIMEOUT 
            ) as ser:

                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                    sock.settimeout(TIME_TO_CONNECT)
                    sock.connect((HOST, PORT))
                    print(f"M2 connected to M1 {HOST}:{PORT}")
                    if is_connected:
                        is_connected(True)

                    while True:
                        if stop_sending_event.is_set():
                            return
                       
                        header = sock.recv(1)
                        if not header:
                            raise ConnectionError("M1 disconnected")
                        data_length = header[0]
                 
                        data = receive_all_sock(sock, data_length)
                        data_type = data[0]
                        data_number = data[1:3]
                        data_message = data[3:]
                        
                        if not data_message:
                            continue
                        ser.write(data_message)
                        ser.flush()
                        

        except Exception as e:
            attempt += 1
            print(f"Connection failed, attempts left {ATTEMPTS_TO_RECONNECT - attempt}:", e)
            time.sleep(TIME_TO_RECONNECT) 
        finally:
            if is_connected:
                is_connected(False)

if __name__ == "__main__":
    connect_to_socket()