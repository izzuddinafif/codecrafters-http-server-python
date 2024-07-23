# Uncomment this to pass the first stage
import socket
import threading


def handle_client(client):
    try:
        data = client.recv(1024).decode()
        if not data:
            client.close()
            return

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
                    user_agent = header[len("User-Agent: "):]
                    ua_length = len(user_agent)
                    client.sendall(f"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: {ua_length}\r\n\r\n{user_agent}".encode())    
        else:
            client.sendall(b"HTTP/1.1 404 Not Found\r\nContent-Type: text/plain\r\nContent-Length: 0\r\n\r\n")

    except Exception as e:
        print(f"Error: {e}")
        client.sendall(b"HTTP/1.1 500 Internal Server Error\r\nContent-Type: text/plain\r\nContent-Length: 0\r\n\r\n")
    
    finally:   
        client.close()

def main():
    # You can use print statements as follows for debugging, they'll be visible when running tests.
    print("Logs from your program will appear here!")
    
    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)
    
    while True:
        client, address = server_socket.accept()
        client_thread = threading.Thread(target=handle_client, args=[client])
        client_thread.start()


if __name__ == "__main__":
    main()
