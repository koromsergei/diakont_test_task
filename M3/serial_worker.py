import serial
import time

from common.M.config import ATTEMPTS_TO_RECONNECT, TIME_TO_RECONNECT, COM_SPEED, COM_TIMEOUT

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


def connect_to_serial(on_pack_id=None, is_connected=None):
    attempt = 0
    pack_number = 1
    request_data = b"\x00\x00"

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

                if is_connected:
                    is_connected(True)

                current_pack = pack_number.to_bytes(2, byteorder="big")
                if on_pack_id:
                    on_pack_id(str(pack_number))

                ser.write(make_packet(0x01, current_pack, request_data))

                while True:
                    if stop_sending_event.is_set():
                        return

                    resp_header = ser.read(1)
                    if not resp_header:
                        raise ConnectionError("No response from M2")

                    resp_length = resp_header[0]
                    response = receive_all_com(ser, resp_length)

                    if len(response) < 3:
                        continue

                    data_type = response[0]
                    data_number = response[1:3]
                    data_message = response[3:]

                    pack_number = int.from_bytes(data_number, byteorder="big") + 1
                    current_pack = pack_number.to_bytes(2, byteorder="big")

                    if on_pack_id:
                        on_pack_id(str(pack_number))

                    ser.write(make_packet(0x01, current_pack, request_data))

        except Exception as e:
            attempt += 1
            print(f"Connection failed, attempts left {ATTEMPTS_TO_RECONNECT - attempt}: {e}")
            time.sleep(TIME_TO_RECONNECT)

        finally:
            if is_connected:
                is_connected(False)


if __name__ == "__main__":
    connect_to_serial()