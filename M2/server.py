import serial
import time
from diakont_test_task.common.config import HOST, PORT, ATTEMPTS_TO_RECONNECT, \
    TIME_TO_CONNECT, TIME_TO_RECONNECT, COM_SPEED, COM_TIMEOUT
import socket


def receive_all(conn, length):
    data = b""
    while len(data) < length:
        chunk = conn.read(length - len(data))
        if not chunk:
            raise ConnectionError("Connection closed")
        data += chunk

    return data


def connect_to_server(on_pack_id=None):
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

                        data_length = ser.read(1)
                        data = receive_all(ser, data_length)
                        data_type = data[1]
                        data_number = data[2:4]
                        data_message = data[3:]

                        if on_pack_id is not None and data_message == b'0x0000':
                            on_pack_id(data_number)

                        line = ser.readline()
                        if not line:
                            continue
                        sock.sendall(line)

        except Exception as e:
            attempt += 1
            print(f"Connection failed, attempts left {ATTEMPTS_TO_RECONNECT - attempt}:", e)
            time.sleep(TIME_TO_RECONNECT) 


if __name__ == "__main__":
    connect_to_server()