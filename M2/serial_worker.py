import serial
import threading
import time
from diakont_test_task.common.config import HOST, PORT, ATTEMPTS_TO_RECONNECT, \
    TIME_TO_CONNECT, TIME_TO_RECONNECT, COM_SPEED, COM_TIMEOUT, TIME_TO_RECEIVE_FROM_M1
import socket
from shared_state import stop_sending_event


def receive_all_com(conn, length):
    data = b""
    while len(data) < length:
        chunk = conn.read(length - len(data))
        if not chunk:
            raise ConnectionError("Connection closed")
        data += chunk

    return data


def send_defauilt(sock):
    sock.sendall(b'0xffff')


def connect_to_serial(on_pack_id=None, is_connected=None):
    attempt = 0
    while attempt < ATTEMPTS_TO_RECONNECT:
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.settimeout(TIME_TO_CONNECT)
                sock.connect((HOST, PORT))
                print("M2 connected to server.")

                with serial.Serial(
                                    "COM3", 
                                    COM_SPEED, 
                                    bytesize=8,
                                    parity=serial.PARITY_NONE,
                                    stopbits=serial.STOPBITS_ONE,
                                    timeout=COM_TIMEOUT 
                ) as ser:
                    while True:
                        all_packets = b""


                        header = ser.read(1)
                        if not header:
                            continue
                        data_length = header[0]  
                        is_connected(True)
                        data = receive_all_com(ser, data_length)
                        data_type = data[1]
                        data_number = data[1:3]
                        data_message = data[3:]

                        if on_pack_id is not None and data_message == b'\x00\x00':
                            on_pack_id(data_number)

                        sock.settimeout(TIME_TO_RECEIVE_FROM_M1)
                        sock.sendall(data_message)
                        response = sock.recv(1024)
                        
        except socket.timeout:
            print(f"Сервер M1 не ответил за {TIME_TO_RECEIVE_FROM_M1} секунд")
            stop_sending_event.set()
            send_defauilt(sock)
        
        except Exception as e:
            attempt += 1
            print(f"Connection failed, attempts left {ATTEMPTS_TO_RECONNECT - attempt}:", e)
            time.sleep(TIME_TO_RECONNECT) 
        
        finally:
            is_connected(False)

if __name__ == "__main__":
    connect_to_serial()