import socket

# TODO: добавить задание порта и адреса в файл
HOST = "127.0.0.1"
PORT = 5000

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen(1)

print(f"Server listening on {HOST}:{PORT}")


def recive_all(conn, length):
    data = b""
    while len(data) < length:
        chunk = conn.recv(length - len(data))
        if not chunk:
            raise ConnectionError("Connection closed")
        data += chunk

    return data



if __name__ == "__main__":
    while True:
        try:
            conn, addr = server.accept()
            print(f"Connected: {addr}")

            data_length = conn.recv(1)[0]
            data = recive_all(conn, data_length)
            data_type = data[1]
            data_number = data[2:4]
            data_message = data[3:]
            

            if data:
                text = data.decode("utf-8")
                print("Received:", text)
                conn.sendall(f"ACK: {text}".encode("utf-8"))

        except Exception as e:
            print(f"Error occurs: {e}")
            continue
        finally:
            if conn:
                conn.close()