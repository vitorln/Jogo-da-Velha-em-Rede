#-*-confg: utf-8 -*-
import socket
import time
from tkinter import *
import tkinter as Tk

log = Tk.Tk()

arq = open('./Servidor.txt', 'r')
texto = arq.read()

salvos = texto.split("\n")
arq.close()
x1, x2 = salvos[0].split()
y1, y2 = salvos[1].split()

ip = StringVar()
ip.set(x1)
porta = StringVar()
porta.set(x2)
nick = StringVar()
nick.set(y1)
porta2 = StringVar()
porta2.set(y2)


log.wm_title("conexão com servidor")
log.wm_protocol('WM_DELETE_WINDOW', log.quit)
container = Tk.Frame(log)
container.pack(side = TOP, expand = 1, pady = 5, padx = 10)
def conectando():
    print("ok")
    

def conecta():
    host = ipText.get()     # Endereco IP do Servidor
    port = int(portaText.get())  # Porta que o Servidor esta
    usuario = nickText.get()
    minhaPorta = porta2Text.get()
    arq = open('./Servidor.txt', 'w')
    texto = host + " " + str(port) + "\n" + usuario + " " + minhaPorta
    arq.write(texto)
    arq.close()
    log.withdraw()
    conexao1 = Tk.Tk()
    udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    dest = (host, port)

    conexao = "USER " + usuario + " " + minhaPorta
    print(conexao)
    while (True):
        udp.sendto(bytes(conexao, encoding='utf8'), dest) 
        time.sleep(10)
    udp.close()


container1 = Tk.Frame(container)
container1.pack()

lbl1 = Label(container1, text="Endereco do servidor: ", anchor = W, width = 18)
lbl1.pack(side = LEFT, padx = 8, pady=5)

ipText = Entry(container1, width=15, textvariable = ip)
ipText.pack(side = RIGHT)

container2 = Tk.Frame(container)
container2.pack()

lbl2 = Label(container2, text="Porta do servidor: ", anchor = W, width = 18)
lbl2.pack(side = LEFT, padx = 8, pady=5)

portaText = Entry(container2,width=15, textvariable = porta)
portaText.pack(side = RIGHT)

container3 = Tk.Frame(container)
container3.pack()

lbl3 = Label(container3, text="Seu usuario: ", anchor = W, width = 18)
lbl3.pack(side = LEFT, padx = 8, pady=5)

nickText = Entry(container3, width=15, textvariable = nick)
nickText.pack(side = RIGHT)

container4 = Tk.Frame(container)
container4.pack()

lbl4 = Label(container4, text="Sua porta: ", anchor = W, width = 18)
lbl4.pack(side = LEFT, padx = 8, pady=5)

porta2Text = Entry(container4,width=15, textvariable = porta2)
porta2Text.pack(side = RIGHT)

b_porta = Button(container, text="conectar", command=conecta ,bg="blue", fg="white")
b_porta.pack(padx = 8, pady=5)

Tk.mainloop()