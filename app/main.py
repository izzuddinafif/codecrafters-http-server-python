from bz2 import compress
from curses import echo
import socket
import threading
import argparse
import os
import gzip
       

def handle_client(client, directory):
    enc_flag = False
    try:
        data = client.recv(1024).decode()
        if not data:
            client.close()
            return

        lines = data.split("\r\n")
        # print(lines)
        body = lines[-1]
        # print(f"data = {body}")
        req = lines[0]
        headers = lines[1:]
        # print(req)
        method, path, _ = req.split(' ')
        # print(method)
        
        for header in headers:
            if header.startswith("Accept-Encoding: "):
                encoding = header.split(':')[1].strip().split(',')
                print(encoding)
                print(type(encoding))
                enc_flag = True
            if header.startswith("User-Agent: "):
                user_agent = header[len("User-Agent: "):]
                ua_length = len(user_agent)
            
        if method == "GET": 
            if path == '/':
                client.sendall(b"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: 0\r\n\r\n")
            
            elif path.startswith("/echo/"):
                echo_string = path[len("/echo/"):].encode() # extract string after /echo/ (path[6:])
                content_length = len(echo_string)
                if enc_flag:
                    print("im in encflag")
                    if "gzip" in encoding:
                        print("im in gzip")
                        compressed_string = gzip.compress(echo_string).decode()
                        content_length = len(compressed_string)
                        client.sendall(f"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Encoding: gzip\r\nContent-Length: {content_length}\r\n\r\n{compressed_string}".encode())
                    else:
                        client.sendall(f"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: {content_length}\r\n\r\n{echo_string}".encode())
                else:
                    client.sendall(f"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: {content_length}\r\n\r\n{echo_string.decode()}".encode())
                                
            elif path == "/user-agent":
                client.sendall(f"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: {ua_length}\r\n\r\n{user_agent}".encode())    
            
            elif path.startswith("/files/"):
                filename = path[len("/files/"):]
                filepath = os.path.join(directory, filename)

                if os.path.isfile(filepath):
                    try:
                        with open(filepath, 'r') as f:
                            content = f.read()
                            content_length = len(content)
                            
                        client.sendall(f"HTTP/1.1 200 OK\r\nContent-Type: application/octet-stream\r\nContent-Length: {content_length}\r\n\r\n{content}".encode())
                            
                    except Exception as e:
                        print(f"Error opening file: {e}")
                        client.sendall(b"HTTP/1.1 500 Internal Server Error\r\nContent-Type: text/plain\r\nContent-Length: 0\r\n\r\n")
                else:
                    client.sendall(b"HTTP/1.1 404 Not Found\r\n\r\n")
                                        
            else:
                client.sendall(b"HTTP/1.1 404 Not Found\r\nContent-Type: text/plain\r\nContent-Length: 0\r\n\r\n")
                
        elif method == "POST":
            if path.startswith("/files/"):
                filename = path[len("/files/"):]
                # print(filename)
                filepath = os.path.join(directory, filename)
                with open(filepath, 'w+') as f:
                    f.write(body)
                # print(filepath)
                client.sendall(b"HTTP/1.1 201 Created\r\n\r\n")                   
                
    except Exception as e:
        print(f"Error: {e}")
        client.sendall(b"HTTP/1.1 500 Internal Server Error\r\nContent-Type: text/plain\r\nContent-Length: 0\r\n\r\n")
    
    finally:   
        client.close()

def main():
    print("This is my own HTTP Server!, it is up and running :D")
    parser = argparse.ArgumentParser(description="A simple HTTP Server") 
    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)
    parser.add_argument('-d', '--directory', type=str, default=os.getcwd(), help="Directory to serve the file from")  
    args = parser.parse_args()

    while True:
        client, address = server_socket.accept()
        client_thread = threading.Thread(target=handle_client, args=[client, args.directory])
        client_thread.start()


if __name__ == "__main__":
    main()
