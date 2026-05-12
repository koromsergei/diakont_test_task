import socket
from diakont_test_task.common.config import HOST, PORT

def receive_all(conn, length):
    data = b""
    while len(data) < length:
        chunk = conn.recv(length - len(data))
        if not chunk:
            raise ConnectionError("Connection closed")
        data += chunk

    return data


def run_server(on_respond=None, on_pack_id=None, on_closed=None, send_respond=None):


    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen(1)

    print(f"Server listening on {HOST}:{PORT}")
    while True:
        conn = None
        try:
            conn, addr = server.accept()
            if on_respond is not None:
                on_respond(True)
                on_pack_id(0)
            print(f"Connected: {addr}")

            data_length = conn.recv(1)[0]
            data = receive_all(conn, data_length)
            data_type = data[1]
            data_number = data[1:3]
            data_message = data[3:]


            if data_message and on_pack_id is not None:
                if data_message == b'\x00\x00':
                    on_pack_id(data_number)
                    if send_respond():
                        conn.sendall(receive_all)
                if data_message == b'\xFF\xFF':
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