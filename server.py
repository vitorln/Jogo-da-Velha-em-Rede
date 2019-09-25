import socket
import time
import threading

conectados = {}
HOST = '127.0.0.1'     # Endereco IP do Servidor
PORT = 5000           # Porta que o Servidor esta
udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
udp.bind((HOST, PORT))


def remove():
    while(True):
        for i in conectados.items():
            if(time.time() - i[1][1] >= 60):
                conectados.pop(i[0])
        time.sleep(10)


t1 = threading.Thread(target=remove, args=())
t1.daemon = True
t1.start()
while (True):
    msg, cliente = udp.recvfrom(1024)
    comando = str(msg).split(" ")
    comando[0] = comando[0][2:]
    comando[-1] = comando[-1][:-1]
    if (comando[0] == "USER"):
        aux = comando[1].replace("_", "")
        if(aux.isalnum()):
            pessoa = comando[1] + ":" + cliente[0] + ":" + comando[2]
            conectados[cliente[0]] = (pessoa, time.time())
            udp.sendto(b"USER OK", cliente)
        else:
            udp.sendto(b"USER NOK", cliente)
    elif(comando[0] == "LIST"):
        print("lista")
    elif(comando[0] == "EXIT"):
        conectados.pop(cliente[0])

udp.close()