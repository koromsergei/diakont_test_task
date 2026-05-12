import serial
import time
from diakont_test_task.common.config import HOST, PORT, ATTEMPTS_TO_RECONNECT, \
    TIME_TO_CONNECT, TIME_TO_RECONNECT, COM_SPEED, COM_TIMEOUT
import socket
from shared_state import stop_sending_event

def receive_all_sock(conn, length):
    data = b""
    while len(data) < length:
        chunk = conn.recv(length - len(data))
        if not chunk:
            raise ConnectionError("Connection closed")
        data += chunk

    return data




def connect_to_socket(on_pack_id=None, is_connected=None):
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
                    sock.bind((HOST, PORT))
                    sock.listen(1)

                    while True:
                        conn = None
                        conn, addr = sock.accept()
                        print(f"M2 connected to server {addr}.")
                        data_length = conn.recv(1)[0]
                        is_connected(True)
                        data = receive_all_sock(conn, data_length)
                        data_type = data[1]
                        data_number = data[1:3]
                        data_message = data[3:]
                        
                        if not data_message:
                            continue
                        if not stop_sending_event.is_set():
                            ser.write(data_message)
                        

        except Exception as e:
            attempt += 1
            print(f"Connection failed, attempts left {ATTEMPTS_TO_RECONNECT - attempt}:", e)
            time.sleep(TIME_TO_RECONNECT) 
        
        finally:
            is_connected(False)

if __name__ == "__main__":
    connect_to_socket()