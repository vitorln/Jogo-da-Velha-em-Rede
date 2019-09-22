import socket

HOST = '127.0.0.1'     # Endereco IP do Servidor
PORT = 5000            # Porta que o Servidor esta
udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
udp.bind((HOST, PORT))
while (True):
    msg, cliente = udp.recvfrom(1024)
    comando = str(msg).split(" ")
    comando[0] = comando[0][2:]
    comando[-1] = comando[-1][0:-1]
    print(comando)
udp.close()