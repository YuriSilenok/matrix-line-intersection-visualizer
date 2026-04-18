import tkinter as tk

from ui.menu import Menu

class Home(tk.Tk):

    def __init__(self):

        super().__init__()
        self.title('Слойка')
        self.geometry('1280x720')
        self.menu = Menu(self)

        self.menu.create_project()
