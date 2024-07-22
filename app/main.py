# Uncomment this to pass the first stage
import socket


def main():
    # You can use print statements as follows for debugging, they'll be visible when running tests.
    print("Logs from your program will appear here!")
    
    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)
    
    client, address = server_socket.accept()
    
    data = client.recv(1024).decode()
    
    lines = data.split("\r\n")
    
    req = lines[0]
    headers = lines[1:]
    
    method, path, version = req.split(' ')
    
    if path == '/':
        client.sendall(b"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: 0\r\n\r\n")
    
    elif path.startswith("/echo/"):
        echo_string = path[len("/echo/"):] # extract string after /echo/ (path[6:])
        content_length = len(echo_string)
        client.sendall(f"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: {content_length}\r\n\r\n{echo_string}".encode())
    
    elif path == "/user-agent":
        for header in headers:
            if header.startswith("User-Agent: "):
                user_agent = header.strip("User-Agent: ")
                ua_length = len(user_agent)
                client.sendall(f"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: {ua_length}\r\n\r\n{user_agent}".encode())    
    else:
        client.sendall(b"HTTP/1.1 404 Not Found\r\nContent-Type: text/plain\r\nContent-Length: 0\r\n\r\n")
    
    client.close()
    server_socket.close()

if __name__ == "__main__":
    main()
