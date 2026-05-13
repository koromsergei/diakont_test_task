import socket
from common.M.config import HOST, PORT


def receive_all(conn, length):
    data = b""
    while len(data) < length:
        chunk = conn.recv(length - len(data))
        if not chunk:
            raise ConnectionError("Connection closed")
        data += chunk
    return data


def make_packet(packet_type, packet_number, message):
    data = bytes([packet_type]) + packet_number + message
    header = bytes([len(data)])
    return header + data


def run_server(on_respond=None, on_pack_id=None, on_closed=None, send_respond=None):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((HOST, PORT))
    server.listen(1)

    print(f"Server listening on {HOST}:{PORT}")

    while True:
        conn = None
        try:
            conn, addr = server.accept()

            if on_respond is not None:
                on_respond(True)

            if on_pack_id is not None:
                on_pack_id(0)

            print(f"Connected: {addr}")

            while True:
                header = conn.recv(1)
                if not header:
                    raise ConnectionError("Client disconnected")

                data_length = header[0]
                data = receive_all(conn, data_length)

                if len(data) < 3:
                    continue
                data_number = data[1:3]
                data_message = data[3:]

                if data_message == b'\x00\x00':
                    if on_pack_id is not None:
                        pack_id = int.from_bytes(data_number, byteorder='big')
                        on_pack_id(pack_id)

                if data_message == b'\xFF\xFF':
                    if on_closed is not None:
                        on_closed(True)
                    break

                if send_respond is not None and send_respond():
                    response_packet = make_packet(
                        packet_type=0x11,
                        packet_number=data_number,
                        message=data_message
                    )
                    conn.sendall(response_packet)

        except Exception as e:
            print(f"Error occurs: {e}")

        finally:
            if conn:
                conn.close()

            if on_respond is not None:
                on_respond(False)


if __name__ == "__main__":
    run_server()