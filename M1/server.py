import socket


def recive_all(conn, length):
    data = b""
    while len(data) < length:
        chunk = conn.recv(length - len(data))
        if not chunk:
            raise ConnectionError("Connection closed")
        data += chunk

    return data


def run_server(on_respond=None, on_pack_id=None, on_closed=None):
    # TODO: добавить задание порта и адреса в файл
    HOST = "127.0.0.1"
    PORT = 5000

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen(1)

    print(f"Server listening on {HOST}:{PORT}")
    while True:
        conn = ''
        try:
            conn, addr = server.accept()
            if on_respond is not None:
                on_respond(True)
                on_pack_id(0)
            print(f"Connected: {addr}")

            data_length = conn.recv(1)[0]
            data = recive_all(conn, data_length)
            data_type = data[1]
            data_number = data[2:4]
            data_message = data[3:]


            if data_message and on_pack_id is not None:
                if data_message == b'0x0000':
                    on_pack_id(data_number)
                    conn.sendall(recive_all)
                if data_message == b'0xFFFF':
                    on_closed(True)

        except Exception as e:
            print(f"Error occurs: {e}")
            continue
        finally:
            if conn:
                if on_respond is not None:
                    on_respond(False)
                conn.close()




if __name__ == "__main__":
    run_server()