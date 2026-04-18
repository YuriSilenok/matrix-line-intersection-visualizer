from tkinter import Toplevel, Label, StringVar, Button, Frame, messagebox
from tkinter.ttk import Spinbox

from ui.windows.utils import center_window


class CreateProject(Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent

        self.data = {
            'number_longitudinal_layers': 4,
            'longitudinal_sublayers': {
                1: 2,
                2: 2,
                3: 2,
                4: 2,
            },
        }

        # Количество продольных слоёв
        self.number_longitudinal_layers = StringVar(
            value=str(self.data['number_longitudinal_layers']),
            name='Количество продольных слоёв')
        self.number_longitudinal_layers.trace('w', self.int_validate)

        self.number_longitudinal_layers_label = Label(self, text='Количество продольных слоёв')
        self.number_longitudinal_layers_label.grid(row=0, column=0, sticky="e", padx=5, pady=5)

        self.number_longitudinal_layers_spinbox = Spinbox(
            self, from_=1, to=10, width=10,
            textvariable=self.number_longitudinal_layers)

        self.number_longitudinal_layers_spinbox.grid(row=0, column=1, sticky="w", padx=5, pady=5)

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

    def number_longitudinal_layers_change(self, *args):
        self

    def int_validate(self, *args):
        print(args)
        try:
            return int(self.number_longitudinal_layers_spinbox.get())
        except ValueError as ex:
            messagebox.showerror(
                title=str(ex),
                message=f"{args[0]} должно задаваться целым числом")
