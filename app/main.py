# Uncomment this to pass the first stage
import socket


def main():
    # You can use print statements as follows for debugging, they'll be visible when running tests.
    print("Logs from your program will appear here!")

    # Uncomment this to pass the first stage
    
    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)
    client, address = server_socket.accept()
    data = client.recv(1024).decode()
    req = data.split("\r\n")[0]
    method, path, version = req.split(' ')
    if(path == "/"):
        client.sendall(b"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: 0\r\n\r\n")
    elif path.startswith("/echo/"):
        echo_string = path[len("/echo/"):] # extract string after /echo/ (path[6:])
        content_length = len(echo_string)
        print(f"{echo_string} {content_length}")
        client.sendall(f"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: {content_length}\r\n\r\n{echo_string}".encode())
    else:
        client.sendall(b"HTTP/1.1 404 Not Found\r\nContent-Type: text/plain\r\nContent-Length: 0\r\n\r\n")
    client.close()
    server_socket.close()

if __name__ == "__main__":
    main()
