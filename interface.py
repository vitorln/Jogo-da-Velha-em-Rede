#-*-confg: utf-8 -*-
import tkinter as Tk

class jogo:
    def __init__(self, master):
        self.imagem_X = Tk.PhotoImage(file = r"X.png")
        self.imagem_O = Tk.PhotoImage(file = r"O.png")
        self.imagem_vazio = Tk.PhotoImage(file = r"vazio.png")

        self.master = master
        self.master.wm_title("Jogo Da Velha")
        self.master.wm_protocol('WM_DELETE_WINDOW', self.master.quit)
        self.container = Tk.Frame(self.master)
        self.container1 = Tk.Frame(self.container, bg = "maroon")
        self.b11 = Tk.Button(self.container1, bg="white", width = 100, height = 100, image = self.imagem_vazio)
        self.b12 = Tk.Button(self.container1, bg="white", width = 100, height = 100, image = self.imagem_vazio)
        self.b13 = Tk.Button(self.container1, bg="white", width = 100, height = 100, image = self.imagem_vazio)     
        self.container2 = Tk.Frame(self.container, bg = "maroon")
        self.b21 = Tk.Button(self.container2, bg="white", width = 100, height = 100, image = self.imagem_vazio)
        self.b22 = Tk.Button(self.container2, bg="white", width = 100, height = 100, image = self.imagem_vazio)
        self.b23 = Tk.Button(self.container2, bg="white", width = 100, height = 100, image = self.imagem_vazio)  
        self.container3 = Tk.Frame(self.container, bg = "maroon")
        self.b31 = Tk.Button(self.container3, bg="white", width = 100, height = 100, image = self.imagem_vazio)
        self.b32 = Tk.Button(self.container3, bg="white", width = 100, height = 100, image = self.imagem_vazio)
        self.b33 = Tk.Button(self.container3, bg="white", width = 100, height = 100, image = self.imagem_vazio)
        self.container4 = Tk.Frame(self.container)
        self.lbl4 = Tk.Label(self.container4, text="sua vez", width = 18, anchor = Tk.W)
        self.b_sair = Tk.Button(self.container4, bg="red", fg="white", text = "sair")


        self.container.pack(side = Tk.TOP, expand = 1, pady = 5, padx = 10)  
        self.container1.pack()
        self.container2.pack()
        self.container3.pack()
        self.container4.pack()
        self.lbl4.pack(side = Tk.LEFT, padx = 8, pady=5)
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



def main(): 
    root = Tk.Tk()
    app = jogo(root)
    root.mainloop()

if __name__ == '__main__':
    main()