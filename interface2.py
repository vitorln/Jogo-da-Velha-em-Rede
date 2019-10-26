#-*-confg: utf-8 -*-
import tkinter as Tk

class recusa:
    def __init__(self, master):

        self.master = master
        self.master.wm_title("conexão com servidor")
        self.master.wm_protocol('WM_DELETE_WINDOW', self.master.quit)
        
        self.container = Tk.Frame(self.master)
        self.container1 = Tk.Frame(self.container)
        self.lbl = Tk.Label(self.container, text="O jogador recusou o convite")
        self.b_nega = Tk.Button(self.container1, text="OK",bg="red", fg="white", command = self.__retorna)

        self.container.pack(side = Tk.TOP, expand = 1, pady = 5, padx = 10)        
        self.lbl.pack(side = Tk.TOP, padx = 8, pady=5)
        self.container1.pack()
        self.b_nega.pack(side = Tk.LEFT, padx = 8, pady=5)

    def __retorna(self):
        self.master.withdraw()


def main(): 
    root = Tk.Tk()
    app = recusa(root)
    root.mainloop()

if __name__ == '__main__':
    main()