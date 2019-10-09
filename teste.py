import socket
import time
import threading

online = {}
HOST_SERVIDOR = '127.0.0.1'     # Endereco IP do Servidor
PORT_SERVIDOR = 5000           # Porta que o Servidor esta
udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
udp.bind((HOST_SERVIDOR, PORT_SERVIDOR))

def conexao():
    global mutex
    while (True):
        msg, cliente = udp.recvfrom(1024)
        comando = str(msg).split(" ")
        comando[0] = comando[0][2:]
        comando[-1] = comando[-1][:-1]
        print(comando)
        if (comando[0] == "USER"):
            aux = comando[1].replace("_", "")
            if(aux.isalnum()):
                mutex.acquire()
                if(cliente[0] in online.keys() and online[cliente[0]][2][1] != cliente[1]):
                    udp.sendto(b"USER NOK", online[cliente[0]][2])
                nome_lista = comando[1] + ":" + cliente[0] + ":" + comando[2]
                online[cliente[0]] = (nome_lista, time.time(), cliente)    
                mutex.release()
                udp.sendto(b"USER OK", cliente)
            else:
                udp.sendto(b"USER NOK", cliente)

        elif(comando[0] == "LIST"):
            mutex.acquire()
            res = 'LIST '+str(len(online))
            for i in online.values():
                res = res+' '+i[0]
            mutex.release()
            udp.sendto(bytes(res, encoding='utf8'), cliente)
        elif(comando[0] == "EXIT"):
            mutex.acquire()
            online.pop(cliente[0])
            mutex.release()

def remove():
    global mutex
    while(True):
        mutex.acquire()
        for i in online.items():
            if(time.time() - i[1][1] >= 60):
                online.pop(i[0])
        mutex.release()
        time.sleep(10)
        

mutex  = threading.Semaphore(1)

t1 = threading.Thread(target=remove, args=())
t1.daemon = True
t1.start()


t2 = threading.Thread(target=conexao, args=())
t2.daemon = True
t2.start()

t2.join()

udp.close()