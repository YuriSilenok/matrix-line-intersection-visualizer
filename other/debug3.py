import tkinter as tk
from tkinter import messagebox

def show_info():
    messagebox.showinfo("Информация", "Это информационное сообщение")

def show_warning():
    messagebox.showwarning("Предупреждение", "Это предупреждение")

def show_error():
    messagebox.showerror("Ошибка", "Это сообщение об ошибке")

window = tk.Tk()

window.title("Пример с messagebox")

window.geometry("400x300")

info_button = tk.Button(window, text="Информация", command=show_info, width=20)
warning_button = tk.Button(window, text="Предупреждение", command=show_warning, width=20)
error_button = tk.Button(window, text="Ошибка", command=show_error, width=20)

info_button.pack(pady=10)
warning_button.pack(pady=10)
error_button.pack(pady=10)

window.mainloop()