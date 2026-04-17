import tkinter as tk
from matrix_drawer import MatrixDrawer
from menu_bar import MenuBar
from toolbar import Toolbar

def main():
    root = tk.Tk()
    root.title("Matrix Drawer")
    root.geometry("1000x700")
    
    # Создаем основной компонент
    app = MatrixDrawer(root)
    
    # Добавляем меню
    menu_bar = MenuBar(root, app)
    
    # Добавляем панель инструментов
    toolbar = Toolbar(root, app)
    
    # Расширяем метод set_edit_mode для обновления тулбара
    original_set_edit_mode = app.set_edit_mode
    def set_edit_mode_with_toolbar(mode):
        original_set_edit_mode(mode)
        toolbar.update_button_states()
    app.set_edit_mode = set_edit_mode_with_toolbar
    
    # Расширяем метод create_new_project для обновления тулбара
    original_create_new_project = app.create_new_project
    def create_new_project_with_toolbar(rows, cols, project_name):
        original_create_new_project(rows, cols, project_name)
        toolbar.update_button_states()
    app.create_new_project = create_new_project_with_toolbar
    
    # Расширяем метод load_project для обновления тулбара
    original_load_project = app.load_project
    def load_project_with_toolbar(filename):
        result = original_load_project(filename)
        if result:
            toolbar.update_button_states()
        return result
    app.load_project = load_project_with_toolbar
    
    root.mainloop()

if __name__ == "__main__":
    main()