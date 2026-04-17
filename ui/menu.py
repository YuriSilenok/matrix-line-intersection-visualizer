import tkinter as tk

from ui.windows.create_project import CreateProject


class Menu(tk.Menu):

    def __init__(self, master: tk.Tk):
        super().__init__(master=master)

        project_menu = tk.Menu(self, tearoff=0)
        project_menu.add_command(label='Создать', command=self.create_project)

        self.add_cascade(label='Проект', menu=project_menu)

        master.config(menu=self)

    def create_project(self):
        create_project_window = CreateProject(self.master)
