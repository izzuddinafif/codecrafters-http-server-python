# Uncomment this to pass the first stage
import socket


def main():
    # You can use print statements as follows for debugging, they'll be visible when running tests.
    print("Logs from your program will appear here!")

    # Uncomment this to pass the first stage
    
    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)
    # this is a concise way to do it:
    # server_socket.accept()[0].sendall(b"HTTP/1.1 200 OK\r\n\r\n") # take the client socket object (index 0) and use the sendall() on that object
    client, address = server_socket.accept()
    data = client.recv(1024)
    print(type(data))
    print(data)
    request = data.decode()
    print(type(request))
    print(request)
    lines = request.split("\n")
    print(type(lines))
    print(lines)
    req_line = lines[0].split(' ')
    path = req_line[1]
    print(path)
    if(path == "/"):
        client.sendall(b"HTTP/1.1 200 OK\r\n\r\n")
    else:
        client.sendall(b"HTTP/1.1 404 Not Found\r\n\r\n")

if __name__ == "__main__":
    main()
