import time
import socket
import serial

from common.M.config import (
    HOST,
    PORT,
    ATTEMPTS_TO_RECONNECT,
    TIME_TO_CONNECT,
    TIME_TO_RECONNECT,
    COM_SPEED,
    COM_TIMEOUT,
    TIME_TO_RECEIVE_FROM_M1,
    M2_PORT,
)

from M2.shared_state import stop_sending_event


def receive_all_com(conn, length):
    data = b""
    while len(data) < length:
        chunk = conn.read(length - len(data))
        if not chunk:
            raise ConnectionError("Connection closed")
        data += chunk
    return data


def make_packet(packet_type, packet_number, message):
    data = bytes([packet_type]) + packet_number + message
    header = bytes([len(data)])
    return header + data


def send_default(ser):
    ser.write(b"\xFF\xFF")


def connect_to_serial(on_pack_id=None, is_connected=None):
    attempt = 0

    while attempt < ATTEMPTS_TO_RECONNECT:
        try:
            stop_sending_event.clear()

            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.settimeout(TIME_TO_CONNECT)
                sock.connect((HOST, PORT))
                print("M2 connected to server.")

                with serial.Serial(
                    M2_PORT,
                    COM_SPEED,
                    bytesize=8,
                    parity=serial.PARITY_NONE,
                    stopbits=serial.STOPBITS_ONE,
                    timeout=COM_TIMEOUT,
                ) as ser:

                    if is_connected:
                        is_connected(True)

                    while True:
                        if stop_sending_event.is_set():
                            if is_connected:
                                is_connected(False)
                            return

                        header = ser.read(1)
                        if not header:
                            continue

                        data_length = header[0]
                        data = receive_all_com(ser, data_length)

                        data_type = data[0]
                        data_number = data[1:3]
                        data_message = data[3:]

                        if on_pack_id is not None and data_message == b"\x00\x00":
                            on_pack_id(data_number)

                        request_packet = make_packet(
                            packet_type=0x11,
                            packet_number=data_number,
                            message=data_message,
                        )

                        sock.settimeout(TIME_TO_RECEIVE_FROM_M1)
                        sock.sendall(request_packet)

                        try:
                            response = sock.recv(1024)
                            if not response:
                                raise ConnectionError("M1 disconnected")

                            ser.write(response)

                        except socket.timeout:
                            print("Timeout waiting response from M1")
                            stop_sending_event.set()
                            send_default(ser)
                            raise ConnectionError("M1 timeout")

        except Exception as e:
            attempt += 1
            print(
                f"M2 connection failed, attempts left {ATTEMPTS_TO_RECONNECT - attempt}: {e}"
            )
            if is_connected:
                is_connected(False)
            time.sleep(TIME_TO_RECONNECT)

    if is_connected:
        is_connected(False)


if __name__ == "__main__":
    connect_to_serial()