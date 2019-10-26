#-*-confg: utf-8 -*-
import tkinter as Tk
import socket
import time
import threading

IP_MAQUINA = '192.168.25.30'

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
        self.b_porta = Tk.Button(self.container, text="conectar", command=self.__conecta ,bg="blue", fg="white")

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

    def __conecta(self):
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
        self.b_select = Tk.Button(self.container2, text="partida selecionada" ,command=self.__selecionado, bg="blue", fg="white", width=15)
        self.b_rand = Tk.Button(self.container2, text="partida aleatoria", command=self.__aleatorio,bg="blue", fg="white", width=15)
        self.espaco = Tk.LabelFrame(self.container2, height = 50)
        self.b_sair = Tk.Button(self.container2, text="Sair", command=self.__close_windows, bg="red", fg="white", width=15)

        self.container.pack(side = Tk.TOP, expand = 1, pady = 5, padx = 10)
        self.lista.pack(side = Tk.LEFT, padx = 8, pady=5)
        self.container2.pack(side = Tk.LEFT)
        self.b_select.pack(padx = 8, pady=5)
        self.b_rand.pack(padx = 8, pady=5)
        self.espaco.pack()
        self.b_sair.pack(side = Tk.BOTTOM, padx = 8, pady = 5)
        
        self.comando = []
        
        self.t1 = threading.Thread(target=self.__userLoop, args=())
        self.t1.daemon = True
        self.t1.start()

        self.t2 = threading.Thread(target=self.__conversa, args=())
        self.t2.daemon = True
        self.t2.start()

        self.t3 = threading.Thread(target=self.__convite, args=())
        self.t3.daemon = True
        self.t3.start()

    def __conversa(self):                        
        while (True):
            try:
                msg, cliente = self.udp.recvfrom(1024)
                self.comando = str(msg).split(" ")
                self.comando[0] = self.comando[0][2:]
                self.comando[-1] = self.comando[-1][0:-1]
                print(self.comando)

                if(self.comando[0] == "USER"):
                    if(self.comando[1] == "OK"):
                        self.udp.sendto(b"LIST", self.dest)
                    elif(self.comando[1] == "NOK"):
                        self.conexaoMaster.deiconify()
                        self.master.withdraw()
                        break
                elif(self.comando[0] == "LIST"):
                    self.lista.delete('0','end')
                    tam = int(self.comando[1])
                    for i in range(2, tam + 2):
                        if(self.comando[i] != self.usuario + ":" + IP_MAQUINA + ":" + self.minhaPorta):
                            self.lista.insert(1, self.comando[i])
            except:
                break

    def __userLoop(self): 
        conexao = "USER " + self.usuario + " " + self.minhaPorta
        print(conexao)
        while (True):
            try:
                self.udp.sendto(bytes(conexao, encoding='utf8'), self.dest) 
            except:
                break
            time.sleep(10)
            if (len(self.comando) == 2):
                if (self.comando[1] == "NOK"):
                    break
    
    def __convite(self):
        tcp_listen = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        orig = (IP_MAQUINA, int(self.minhaPorta))
        tcp_listen.bind(orig)

        tcp_listen.listen(1)
        while(True):
            self.con, self.cliente = tcp_listen.accept()
            mensagem  = self.con.recv(1024)
            print (mensagem)
            mensagem = str(mensagem).split(" ")
            mensagem[0] = mensagem[0][2:]
            mensagem[-1] = mensagem[-1][0:-1]
            print (mensagem)
            if (mensagem[0] == "START"):
                self.newWindow = Tk.Toplevel(self.master)
                self.app = convite(self.newWindow, self.conexaoMaster, mensagem[1], self.con, self.udp, self.dest)
            else:
                self.con.close()
                  
    def __close_windows(self):
       
        self.udp.sendto(b"EXIT", self.dest) 
        self.udp.close()
        self.conexaoMaster.destroy()

    def __aleatorio(self):
        print("foi rand")
        self.udp.sendto(b"EXIT", self.dest)
        self.udp.close()
        self.master.withdraw()
        self.newWindow = Tk.Toplevel(self.master)
        self.app = jogo(self.newWindow, self.conexaoMaster, self.tcp_connect)

    def __selecionado(self):
        try:
            tcp_connect = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            select = self.lista.get(self.lista.curselection())
            select = select.split(":")
            oponente = (select[1], int(select[2]))
            tcp_connect.connect((select[1], int(select[2])))
            tcp_connect.send(bytes("START " + self.usuario, encoding='utf8'))
            
            resposta = tcp_connect.recv(1024)
            resposta = str(resposta).split(" ")
            resposta[0] = resposta[0][2:]
            resposta[-1] = resposta[-1][0:-1]
            if (resposta[0] == "START"):
                self.udp.sendto(b"EXIT", self.dest)
                self.udp.close()
                self.master.withdraw()
                self.newWindow = Tk.Toplevel(self.master)
                self.app = jogo(self.newWindow, self.conexaoMaster, tcp_connect, True)
            elif(resposta[0] == "BYE"):
                self.newWindow = Tk.Toplevel(self.master)
                self.app = recusa(self.newWindow)
                tcp_connect.close()
        except:
            print("erro na seleção")

class recusa:
    def __init__(self, master):

        self.master = master
        self.master.wm_title("conexão com servidor")
        self.master.wm_protocol('WM_DELETE_WINDOW', self.master.quit)
        
        self.container = Tk.Frame(self.master)
        self.container1 = Tk.Frame(self.container)
        self.lbl = Tk.Label(self.container, text="O jogador recusou o convite")
        self.b_nega = Tk.Button(self.container1, text="Ok",bg="red", fg="white", command = self.__retorna)

        self.container.pack(side = Tk.TOP, expand = 1, pady = 5, padx = 10)        
        self.lbl.pack(side = Tk.TOP, padx = 8, pady=5)
        self.container1.pack()
        self.b_nega.pack(side = Tk.LEFT, padx = 8, pady=5)

    def __retorna(self):
        self.master.withdraw()

class convite:
    def __init__(self, master, conexaoMaster, desafiante, tcp, udp, dest):
        self.udp = udp
        self.dest = dest
        self.desafiante = desafiante
        self.tcp = tcp
        self.conexaoMaster = conexaoMaster
        self.master = master
        self.master.wm_title("conexão com servidor")
        self.master.wm_protocol('WM_DELETE_WINDOW', self.master.quit)
        
        self.container = Tk.Frame(self.master)
        self.container1 = Tk.Frame(self.container)
        self.lbl = Tk.Label(self.container, text= self.desafiante + " esta te desafianado! \nDeseja aceitar??")
        self.b_confirma = Tk.Button(self.container1, text="Aceitar",bg="blue", fg="white", command = self.__aceita)
        self.b_nega = Tk.Button(self.container1, text="Rejeitar",bg="red", fg="white", command = self.__regeita)

        self.container.pack(side = Tk.TOP, expand = 1, pady = 5, padx = 10)        
        self.lbl.pack(side = Tk.TOP, padx = 8, pady=5)
        self.container1.pack()
        self.b_confirma.pack(side = Tk.LEFT, padx = 8, pady=5)
        self.b_nega.pack(side = Tk.LEFT, padx = 8, pady=5)

    def __regeita(self):
        print("regeita")
        self.tcp.send(b"BYE")
        self.master.withdraw()

    def __aceita(self):
        print("aceita")
        self.tcp.send(b"START OK")
        self.udp.sendto(b"EXIT", self.dest)
        self.udp.close()
        self.master.withdraw()
        self.newWindow = Tk.Toplevel(self.master)
        self.app = jogo(self.newWindow, self.conexaoMaster, self.tcp, False)
    
class jogo:
    def __init__(self, master, conexaoMaster, tcp, desafiante = True):

        self.tcp = tcp
        self.desafiante = desafiante
        self.imagem_X = Tk.PhotoImage(file = r"X.png").subsample(2, 2)
        self.imagem_O = Tk.PhotoImage(file = r"O.png").subsample(2, 2)
        self.imagem_vazio = Tk.PhotoImage(file = r"vazio.png").subsample(2, 2)
        
        self.conexaoMaster = conexaoMaster
        self.master = master
        self.master.wm_title("Jogo Da Velha")
        self.master.wm_protocol('WM_DELETE_WINDOW', self.master.quit)
        self.container = Tk.Frame(self.master)
        self.container1 = Tk.Frame(self.container, bg = "maroon")
        self.b11 = Tk.Button(self.container1, bg="white", width = 100, height = 100, image = self.imagem_vazio, command = self.__botao11)
        self.b12 = Tk.Button(self.container1, bg="white", width = 100, height = 100, image = self.imagem_vazio, command = self.__botao12)
        self.b13 = Tk.Button(self.container1, bg="white", width = 100, height = 100, image = self.imagem_vazio, command = self.__botao13)     
        self.container2 = Tk.Frame(self.container, bg = "maroon")
        self.b21 = Tk.Button(self.container2, bg="white", width = 100, height = 100, image = self.imagem_vazio, command = self.__botao21)
        self.b22 = Tk.Button(self.container2, bg="white", width = 100, height = 100, image = self.imagem_vazio, command = self.__botao22)
        self.b23 = Tk.Button(self.container2, bg="white", width = 100, height = 100, image = self.imagem_vazio, command = self.__botao23)  
        self.container3 = Tk.Frame(self.container, bg = "maroon")
        self.b31 = Tk.Button(self.container3, bg="white", width = 100, height = 100, image = self.imagem_vazio, command = self.__botao31)
        self.b32 = Tk.Button(self.container3, bg="white", width = 100, height = 100, image = self.imagem_vazio, command = self.__botao32)
        self.b33 = Tk.Button(self.container3, bg="white", width = 100, height = 100, image = self.imagem_vazio, command = self.__botao33)
        self.container4 = Tk.Frame(self.container)
        self.vez_jogador = Tk.Label(self.container4, text="sua vez", width = 18, anchor = Tk.W)
        self.b_sair = Tk.Button(self.container4, bg="red", fg="white", text = "sair", command = self.__close_windows)
        

        self.container.pack(side = Tk.TOP, expand = 1, pady = 5, padx = 10)  
        self.container1.pack()
        self.container2.pack()
        self.container3.pack()
        self.container4.pack()
        self.vez_jogador.pack(side = Tk.LEFT, padx = 8, pady=5)
        self.b_sair.pack(side = Tk.LEFT, padx = 8, pady=5)
        self.b11.pack(side = Tk.LEFT, padx = 8, pady=8)
        self.b12.pack(side = Tk.LEFT, padx = 8, pady=8)
        self.b13.pack(side = Tk.LEFT, padx = 8, pady=8)
        self.b21.pack(side = Tk.LEFT, padx = 8, pady=8)
        self.b22.pack(side = Tk.LEFT, padx = 8, pady=8)
        self.b23.pack(side = Tk.LEFT, padx = 8, pady=8)
        self.b31.pack(side = Tk.LEFT, padx = 8, pady=8)
        self.b32.pack(side = Tk.LEFT, padx = 8, pady=8)
        self.b33.pack(side = Tk.LEFT, padx = 8, pady=8)

        self.flag_sua_vez = False
        self.t1 = threading.Thread(target=self.__loopJogo, args=(self.desafiante))
        self.t1.daemon = True
        self.t1.start()
        

    def __loopJogo(self, desafiante):
        while(True):
            if(not desafiante):
                self.__flipaVez(self.flag_sua_vez) 
                jogada = self.tcp.recv(1024)
                jogada = str(jogada).split(" ")
                jogada[0] = jogada[0][2:]
                jogada[-1] = jogada[-1][0:-1]
                if(jogada[0] == "PLAY"):
                    self.__jogado(int(jogada[1]), int(jogada[2]), self.imagem_X)
                    desafiante = True
        
    def __flipaVez(self, flag_sua_vez):
        if (flag_sua_vez):
            flag_sua_vez = False
            self.vez_jogador.config(text = "Vez do oponente")
        else:
            flag_sua_vez = True
            self.vez_jogador.config(text = "Sua vez")


    def __botao11(self):
        self.__jogado(1, 1, self.imagem_O)
        self.tcp.send(b"PLAY 1 1")
        self.desafiante = False

    def __botao12(self):
        self.__jogado(1, 2, self.imagem_O)
        self.tcp.send(b"PLAY 1 2")
        self.desafiante = False

    def __botao13(self):
        self.__jogado(1, 3, self.imagem_O)
        self.tcp.send(b"PLAY 1 3")
        self.desafiante = False
 
    def __botao21(self):
        self.__jogado(2, 1, self.imagem_O)
        self.tcp.send(b"PLAY 2 1")
        self.desafiante = False

    def __botao22(self):
        self.__jogado(2, 2, self.imagem_O)
        self.tcp.send(b"PLAY 2 2")
        self.desafiante = False

    def __botao23(self):
        self.__jogado(2, 3, self.imagem_O)
        self.tcp.send(b"PLAY 2 3")
        self.desafiante = False

    def __botao31(self):
        self.__jogado(3, 1, self.imagem_O)
        self.tcp.send(b"PLAY 3 1")
        self.desafiante = False

    def __botao32(self):
        self.__jogado(3, 2, self.imagem_O)
        self.tcp.send(b"PLAY 3 2")
        self.desafiante = False

    def __botao33(self):
        self.__jogado(3, 3, self.imagem_O)
        self.tcp.send(b"PLAY 3 3")
        self.desafiante = False

    def __jogado(self, linha, coluna, imagem):

        if  (linha == 1 and coluna == 1):
            self.b11.config(bg="gray", image = imagem, state = Tk.DISABLED)
        elif  (linha == 1 and coluna == 2):
            self.b12.config(bg="gray", image = imagem, state = Tk.DISABLED)
        elif  (linha == 1 and coluna == 3):
            self.b13.config(bg="gray", image = imagem, state = Tk.DISABLED)
        elif  (linha == 2 and coluna == 1):
            self.b21.config(bg="gray", image = imagem, state = Tk.DISABLED)
        elif  (linha == 2 and coluna == 2):
            self.b22.config(bg="gray", image = imagem, state = Tk.DISABLED)
        elif  (linha == 2 and coluna == 3):
            self.b23.config(bg="gray", image = imagem, state = Tk.DISABLED)
        elif  (linha == 3 and coluna == 1):
            self.b31.config(bg="gray", image = imagem, state = Tk.DISABLED)
        elif  (linha == 3 and coluna == 2):
            self.b32.config(bg="gray", image = imagem, state = Tk.DISABLED)
        elif  (linha == 3 and coluna == 3):
            self.b33.config(bg="gray", image = imagem, state = Tk.DISABLED)
        
        __flipaVez(self.flag_sua_vez)

    def __close_windows(self):
        self.conexaoMaster.destroy()


def main(): 
    root = Tk.Tk()
    app = Conexao(root)
    root.mainloop()

if __name__ == '__main__':
    main()