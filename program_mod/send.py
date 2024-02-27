import socket
import ssl
import threading
import os

def receive_file(ssl_socket, address):
    from program_mod.secure_drop_shell import Global_SecureDropShell
    Global_SecureDropShell.pause()

    try:
        request = ssl_socket.recv(1024).decode()
        if request == "FILE_REQUEST":
            print(f"Contact is sending a file. Accept (y/n)?", end="", flush=True)
            user_input = input().lower()
            if user_input == "y":
                ## ACCEPT FILE REQUEST ##
                ssl_socket.sendall(b"ACCEPT")
            
                file_extension = ssl_socket.recv(1024).decode()

                file_data = b""
                while True:
                    data = ssl_socket.recv(1024)
                    if not data:
                        break
                    file_data += data

                with open(f"received_file_{address[0]}_{address[1]}{file_extension}", "wb") as file:
                    file.write(file_data)

                print(f"File received from {address}")
            else:
                ssl_socket.sendall(b"DECLINE")
            ssl_socket.close()
        else:
            print(f"Invalid request. Aborting")
            ssl_socket.close()
    except ssl.SSLError as e:
        print(f"SSL Error: {e}")
    finally:
        Global_SecureDropShell.resume()
def start_listener():
    host = '0.0.0.0'  # Listen on all available interfaces
    port = 9999

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(5)

    ssl_context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    ssl_context.load_cert_chain(certfile='server.crt', keyfile='server.key')


    while True:
        peer_socket, peer_address = server_socket.accept()

        ssl_socket = ssl_context.wrap_socket(peer_socket, server_side=True)

        peer_handler = threading.Thread(target=receive_file, args=(ssl_socket, peer_address))
        peer_handler.daemon = True
        peer_handler.start()
    return ssl_context.wrap_socket(tcp_socket, server_hostname='client')

#TODO: Make it so that is is not peer_ip, but peer_email and then we can convert in this function   
def send_file(file_path, peer_ip):
    port = 9999

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((peer_ip, port))
    

    ssl_context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    ssl_context.load_cert_chain(certfile='client.crt', keyfile='client.key')
    ssl_socket = ssl.wrap_socket(client_socket, server_side=False)
    
    try:
        ssl_socket.sendall(b"FILE_REQUEST")
        ack = ssl_socket.recv(1024).decode()
        if ack == "ACCEPT":

            #GET FILE NAME, AND EXTENSION, send extension to reciever so they can open right file type
            file_name, file_extension = os.path.splitext(file_path)
            ssl_socket.sendall(file_extension.encode())

            print(f"Contact has accepted the transfer request.")
            with open(file_path, "rb") as file:
                file_data = file.read()

            ssl_socket.sendall(file_data)

            print(f"File sent successfully to {peer_ip}:{port}")
        elif ack == "DECLINE":
            print(f"Reciever declined file transfer. Abort")
        else:
            print(f"invalid response. abort")
    except ssl.SSLError as e:
        print(f"SSL Error: {e}")
    finally:
        ssl_socket.close()

