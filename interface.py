#-*-confg: utf-8 -*-
import tkinter as Tk
class jogo:
    def __init__(self, master):
        self.imagem_X = Tk.PhotoImage(file = r"X.png").subsample(2, 2)
        self.imagem_O = Tk.PhotoImage(file = r"O.png").subsample(2, 2)
        self.imagem_vazio = Tk.PhotoImage(file = r"vazio.png").subsample(2, 2)
        
        self.master = master
        self.master.wm_title("Jogo Da Velha")
        self.master.wm_protocol('WM_DELETE_WINDOW', self.master.quit)
        self.container = Tk.Frame(self.master)
        self.container1 = Tk.Frame(self.container, bg = "maroon")
        self.b11 = Tk.Button(self.container1, bg="white", width = 100, height = 100, image = self.imagem_vazio, command = self.botao11)
        self.b12 = Tk.Button(self.container1, bg="white", width = 100, height = 100, image = self.imagem_vazio, command = self.botao12)
        self.b13 = Tk.Button(self.container1, bg="white", width = 100, height = 100, image = self.imagem_vazio, command = self.botao13)     
        self.container2 = Tk.Frame(self.container, bg = "maroon")
        self.b21 = Tk.Button(self.container2, bg="white", width = 100, height = 100, image = self.imagem_vazio, command = self.botao21)
        self.b22 = Tk.Button(self.container2, bg="white", width = 100, height = 100, image = self.imagem_vazio, command = self.botao22)
        self.b23 = Tk.Button(self.container2, bg="white", width = 100, height = 100, image = self.imagem_vazio, command = self.botao23)  
        self.container3 = Tk.Frame(self.container, bg = "maroon")
        self.b31 = Tk.Button(self.container3, bg="white", width = 100, height = 100, image = self.imagem_vazio, command = self.botao31)
        self.b32 = Tk.Button(self.container3, bg="white", width = 100, height = 100, image = self.imagem_vazio, command = self.botao32)
        self.b33 = Tk.Button(self.container3, bg="white", width = 100, height = 100, image = self.imagem_vazio, command = self.botao33)
        self.container4 = Tk.Frame(self.container)
        self.vez_jogador = Tk.Label(self.container4, text="sua vez", width = 18, anchor = Tk.W)
        self.b_sair = Tk.Button(self.container4, bg="red", fg="white", text = "sair", command = self.close_windows)
        

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

        self.flag_sua_vez = True 

    
    def botao11(self):
        self.jogado(1, 1, self.imagem_O)

    def botao12(self):
        self.jogado(1, 2, self.imagem_O)

    def botao13(self):
        self.jogado(1, 3, self.imagem_O)
 
    def botao21(self):
        self.jogado(2, 1, self.imagem_O)

    def botao22(self):
        self.jogado(2, 2, self.imagem_O)

    def botao23(self):
        self.jogado(2, 3, self.imagem_O)

    def botao31(self):
        self.jogado(3, 1, self.imagem_O)

    def botao32(self):
        self.jogado(3, 2, self.imagem_O)

    def botao33(self):
        self.jogado(3, 3, self.imagem_O)

    def jogado(self, linha, coluna, imagem):
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
        
        if (self.flag_sua_vez):
            self.flag_sua_vez = False
            self.vez_jogador.config(text = "Vez do oponente")
        else:
            self.flag_sua_vez = True
            self.vez_jogador.config(text = "Sua vez")

    def close_windows(self):
        self.master.destroy()

        

def main(): 
    root = Tk.Tk()
    app = jogo(root)
    root.mainloop()

if __name__ == '__main__':
    main()