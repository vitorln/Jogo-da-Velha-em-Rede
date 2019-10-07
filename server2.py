import socket
import time
import threading
class Server:
    def __init__(self, udp):
        self.udp = udp
        self.conectados = {}
        self.t1 = threading.Thread(target=self.remove, args=())
        self.t1.daemon = True
        self.t1.start()


        self.t2 = threading.Thread(target=self.conexao, args=())
        self.t2.daemon = True
        self.t2.start()

        self.t2.join()

        self.udp.close()

    def remove(self):
        while(True):
            for i in self.conectados.items():
                if(time.time() - i[1][1] >= 60):
                    self.conectados.pop(i[0])
                print(i)
            time.sleep(10)
            

    def conexao(self):
        while (True):
            msg, cliente = self.udp.recvfrom(1024)
            print(msg)
            comando = str(msg).split(" ")
            
            comando[0] = comando[0][2:]
            comando[-1] = comando[-1][:-1]
            print(comando)
            if (comando[0] == "USER"):
                aux = comando[1].replace("_", "")
                if(aux.isalnum()):
                    pessoa = comando[1] + ":" + cliente[0] + ":" + comando[2]
                    self.conectados[cliente[0]] = (pessoa, time.time())
                    self.udp.sendto(b"USER OK", cliente)
                else:
                    self.udp.sendto(b"USER NOK", cliente)
            elif(comando[0] == "LIST"):
                for i in self.conectados.items():
                    print("Usuario: "+i[1][0])
                    
            elif(comando[0] == "EXIT"):
                self.conectados.pop(cliente[0])
        





def main(): 
    HOST = '10.81.66.21'     # Endereco IP do Servidor
    PORT = 5000           # Porta que o Servidor esta
    udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp.bind((HOST, PORT))

    server = Server(udp)

    udp.close()

if __name__ == '__main__':
    main()