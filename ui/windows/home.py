import tkinter as tk

from ui.menu import Menu

class Home(tk.Tk):

    def __init__(self):

        super().__init__()
        self.title('Слойка')
        self.geometry('1920x1080')
        self.menu = Menu(self)
