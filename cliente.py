#-*-confg: utf-8 -*-
import tkinter as Tk
import socket
import time
import threading

class Conexao:
    def __init__(self, master):
        self.arq = open('./Servidor.txt', 'r')
        self.texto = self.arq.read()
        self.salvos = self.texto.split("\n")
        self.arq.close()
        
        self.x1, self.x2 = self.salvos[0].split()
        self.y1, self.y2 = self.salvos[1].split()
        self.ip = Tk.StringVar()
        self.ip.set(self.x1)
        self.porta = Tk.StringVar()
        self.porta.set(self.x2)
        self.nick = Tk.StringVar()
        self.nick.set(self.y1)
        self.porta2 = Tk.StringVar()
        self.porta2.set(self.y2)

        self.master = master
        self.master.wm_title("conexão com servidor")
        self.master.wm_protocol('WM_DELETE_WINDOW', self.master.quit)
        self.container = Tk.Frame(self.master)
        self.container1 = Tk.Frame(self.container)
        self.lbl1 = Tk.Label(self.container1, text="Endereco do servidor: ", anchor = Tk.W, width = 18)
        self.ipText = Tk.Entry(self.container1, width=15, textvariable = self.ip)
        self.container2 = Tk.Frame(self.container)
        self.lbl2 = Tk.Label(self.container2, text="Porta do servidor: ", anchor = Tk.W, width = 18)
        self.portaText = Tk.Entry(self.container2, width=15, textvariable = self.porta)
        self.container3 = Tk.Frame(self.container)
        self.lbl3 = Tk.Label(self.container3, text="Seu usuario: ", anchor = Tk.W, width = 18)
        self.nickText = Tk.Entry(self.container3, width=15, textvariable = self.nick)
        self.container4 = Tk.Frame(self.container)
        self.lbl4 = Tk.Label(self.container4, text="Sua porta: ", anchor = Tk.W, width = 18)
        self.porta2Text = Tk.Entry(self.container4,width=15, textvariable = self.porta2)
        self.b_porta = Tk.Button(self.container, text="conectar", command=self.conecta ,bg="blue", fg="white")

        self.container.pack(side = Tk.TOP, expand = 1, pady = 5, padx = 10)        
        self.container1.pack()
        self.lbl1.pack(side = Tk.LEFT, padx = 8, pady=5)
        self.ipText.pack(side = Tk.RIGHT)
        self.container2.pack()
        self.lbl2.pack(side = Tk.LEFT, padx = 8, pady=5)
        self.portaText.pack(side = Tk.RIGHT)
        self.container3.pack()
        self.lbl3.pack(side = Tk.LEFT, padx = 8, pady=5)
        self.nickText.pack(side = Tk.RIGHT)
        self.container4.pack()
        self.lbl4.pack(side = Tk.LEFT, padx = 8, pady=5)
        self.porta2Text.pack(side = Tk.RIGHT)
        self.b_porta.pack(padx = 8, pady=5)

    def conecta(self):
        host = self.ipText.get()     # Endereco IP do Servidor
        port = int(self.portaText.get())  # Porta que o Servidor esta
        usuario = self.nickText.get()
        minhaPorta = self.porta2Text.get()
        arq = open('./Servidor.txt', 'w')
        texto = host + " " + str(port) + "\n" + usuario + " " + minhaPorta
        arq.write(texto)
        arq.close()
        self.master.withdraw()
        self.newWindow = Tk.Toplevel(self.master)
        self.app = selecao(self.newWindow, self.master, host, port, usuario, minhaPorta)

class selecao:
    def __init__(self, master, conexaoMaster, host, port, usuario, minhaPorta):
        self.udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.dest = (host, port)

        self.master = master
        self.conexaoMaster = conexaoMaster
        self.host = host
        self.port = port
        self.usuario = usuario
        self.minhaPorta = minhaPorta

        self.master.wm_title("conexão com servidor")
        self.master.wm_protocol('WM_DELETE_WINDOW', self.master.quit)
        self.container = Tk.Frame(self.master)
        self.lista = Tk.Listbox(self.container)
        self.container2 = Tk.Frame(self.container)
        self.b_porta = Tk.Button(self.container2, text="partida selecionada" ,bg="blue", fg="white", width=15)
        self.b_porta1 = Tk.Button(self.container2, text="partida aleatoria" ,bg="blue", fg="white", width=15)
        self.b_porta1 = Tk.Button(self.container2, text="partida aleatoria" ,bg="blue", fg="white", width=15)
        self.espaco = Tk.LabelFrame(self.container2, height = 50)
        self.b_porta2 = Tk.Button(self.container2, text="Sair", command=self.close_windows, bg="red", fg="white", width=15)

        self.container.pack(side = Tk.TOP, expand = 1, pady = 5, padx = 10)
        self.lista.pack(side = Tk.LEFT, padx = 8, pady=5)
        self.container2.pack(side = Tk.LEFT)
        self.b_porta.pack(padx = 8, pady=5)
        self.b_porta1.pack(padx = 8, pady=5)
        self.espaco.pack()
        self.b_porta2.pack(side = Tk.BOTTOM, padx = 8, pady = 5)
        
        self.comando = []
        
        self.t1 = threading.Thread(target=self.userLoop, args=())
        self.t1.daemon = True
        self.t1.start()

        self.t2 = threading.Thread(target=self.conversa, args=())
        self.t2.daemon = True
        self.t2.start()

    def conversa(self):                        
        while (True):
            msg, cliente = self.udp.recvfrom(1024)
            self.comando = str(msg).split(" ")
            self.comando[0] = self.comando[0][2:]
            self.comando[-1] = self.comando[-1][0:-1]
            print(self.comando)

            if(self.comando[0] == "USER"):
                if(self.comando[1] == "OK"):
                    self.udp.sendto(b"LIST", self.dest)
                elif(self.comando[1] == "NOK"):
                    print("no")
                    self.conexaoMaster.deiconify()
                    self.master.withdraw()
                    break
            elif(self.comando[0] == "LIST"):
                print("lista")

    def userLoop(self): 
        conexao = "USER " + self.usuario + " " + self.minhaPorta
        print(conexao)
        while (True):
            self.udp.sendto(bytes(conexao, encoding='utf8'), self.dest) 
            time.sleep(10)
            if (self.comando[1] == "NOK"):
                break
        
    def close_windows(self):
        self.udp.close()
        self.udp.sendto(b"EXIT", self.self.udp.close()dest) 
        self.conexaoMaster.destroy()


def main(): 
    root = Tk.Tk()
    app = Conexao(root)
    root.mainloop()

if __name__ == '__main__':
    main()