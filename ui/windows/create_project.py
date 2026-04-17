from tkinter import Toplevel, Label, StringVar, Button, Frame
from tkinter.ttk import Spinbox

from ui.windows.utils import center_window


class CreateProject(Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent

        # Количество продольных слоёв
        self.number_longitudinal_layers_label = Label(self, text='Количество продольных слоёв')
        self.number_longitudinal_layers_label.grid(row=0, column=0, sticky="e", padx=5, pady=5)

        self.number_longitudinal_layers = Spinbox(self, from_=1, to=10, width=10, textvariable=StringVar(value='4'))
        self.number_longitudinal_layers.insert(0, "4")
        self.number_longitudinal_layers.grid(row=0, column=1, sticky="w", padx=5, pady=5)

        # Количество поперечных слоёв
        self.number_transverse_layers_label = Label(self, text='Количество поперечных слоёв')
        self.number_transverse_layers_label.grid(row=1, column=0, sticky="e", padx=5, pady=5)

        self.number_transverse_layers = Spinbox(self, from_=1, to=10, width=10)
        self.number_transverse_layers.insert(0, "4")
        self.number_transverse_layers.grid(row=1, column=1, sticky="w", padx=5, pady=5)

        self.grid_columnconfigure(index=0, weight=1)
        self.grid_columnconfigure(index=1, weight=1)

        self.buttons = Frame(self)
        self.buttons.grid(row=100, column=1)

        self.cancel_button = Button(self.buttons, text='Отмена', command=self.cancel_handler)
        self.cancel_button.grid(row=0, column=0, padx=3, pady=3)

        self.create_button = Button(self.buttons, text='Создать', command=self.create_handler)
        self.create_button.grid(row=0, column=1, padx=3, pady=3)


        # настройка окна
        self.geometry('400x100')
        self.minsize(width=400, height=100)
        center_window(self)
        self.transient(parent)
        self.grab_set()
        self.focus_set()
        self.wait_window(self)

    def cancel_handler(self):
        self.destroy()

    def create_handler(self):

        self.cancel_handler()