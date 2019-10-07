import socket
import time
import threading

online = {}
HOST_SERVIDOR = '10.81.66.21'     # Endereco IP do Servidor
PORT_SERVIDOR = 5000           # Porta que o Servidor esta
udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
udp.bind((HOST_SERVIDOR, PORT_SERVIDOR))

def conexao():
    while (True):
        msg, cliente = udp.recvfrom(1024)
        comando = str(msg).split(" ")
        comando[0] = comando[0][2:]
        comando[-1] = comando[-1][:-1]
        if (comando[0] == "USER"):
            aux = comando[1].replace("_", "")
            if(aux.isalnum()):
                if(cliente[0] in online.keys() and online[cliente[0]][2][1] != cliente[1]):
                    udp.sendto(b"USER NOK", online[cliente[0]][2])
                nome_lista = comando[1] + ":" + cliente[0] + ":" + comando[2]
                online[cliente[0]] = (nome_lista, time.time(), cliente)    
                udp.sendto(b"USER OK", cliente)
            else:
                udp.sendto(b"USER NOK", cliente)

        elif(comando[0] == "LIST"):
            res = 'LIST '+str(len(online))
            for i in online.values():
                res = res+' '+i[0]
            udp.sendto(bytes(res, encoding='utf8'), cliente)
        elif(comando[0] == "EXIT"):
            online.pop(cliente[0])

def remove():
    while(True):
        for i in online.items():
            if(time.time() - i[1][1] >= 60):
                online.pop(i[0])
        time.sleep(10)


t1 = threading.Thread(target=remove, args=())
t1.daemon = True
t1.start()


t2 = threading.Thread(target=conexao, args=())
t2.daemon = True
t2.start()

t2.join()

udp.close()