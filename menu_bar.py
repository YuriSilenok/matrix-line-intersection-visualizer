import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
import os

class MenuBar:
    def __init__(self, root, matrix_drawer):
        self.root = root
        self.matrix_drawer = matrix_drawer
        
        # Создаем меню
        self.menubar = tk.Menu(root)
        root.config(menu=self.menubar)
        
        # Меню File
        self.file_menu = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="File", menu=self.file_menu)
        self.file_menu.add_command(label="New Project", command=self.new_project_dialog, accelerator="Ctrl+N")
        self.file_menu.add_command(label="Open Project", command=self.open_project_dialog, accelerator="Ctrl+O")
        self.file_menu.add_command(label="Save Project", command=self.save_project_dialog, accelerator="Ctrl+S")
        self.file_menu.add_command(label="Save As...", command=self.save_as_dialog, accelerator="Ctrl+Shift+S")
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Exit", command=root.quit)
        
        # Меню Edit
        self.edit_menu = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="Edit", menu=self.edit_menu)
        self.edit_menu.add_command(label="Edit Cells", command=self.enable_edit_mode)
        self.edit_menu.add_command(label="Draw Thread", command=self.enable_draw_mode)
        self.edit_menu.add_separator()
        self.edit_menu.add_command(label="Clear All Points", command=self.clear_points)
        self.edit_menu.add_command(label="Enable All Cells", command=self.enable_all_cells)
        self.edit_menu.add_command(label="Disable All Cells", command=self.disable_all_cells)
        
        # Меню View
        self.view_menu = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="View", menu=self.view_menu)
        self.view_menu.add_command(label="Reset Zoom", command=self.reset_view)
        
        # Меню Help
        self.help_menu = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="Help", menu=self.help_menu)
        self.help_menu.add_command(label="About", command=self.show_about)
        
        # Привязка горячих клавиш
        root.bind('<Control-n>', lambda e: self.new_project_dialog())
        root.bind('<Control-o>', lambda e: self.open_project_dialog())
        root.bind('<Control-s>', lambda e: self.save_project_dialog())
        root.bind('<Control-Shift-S>', lambda e: self.save_as_dialog())
        
        # Текущий файл проекта
        self.current_file = None
    
    def new_project_dialog(self):
        """Диалог создания нового проекта"""
        dialog = NewProjectDialog(self.root)
        if dialog.result:
            rows, cols, name = dialog.result
            self.matrix_drawer.create_new_project(rows, cols, name)
            self.current_file = None
            self.root.title(f"Matrix Drawer - {name}")
    
    def open_project_dialog(self):
        """Диалог открытия проекта"""
        filename = filedialog.askopenfilename(
            title="Open Project",
            filetypes=[("Matrix Project files", "*.matrix"), ("All files", "*.*")]
        )
        if filename:
            if self.matrix_drawer.load_project(filename):
                self.current_file = filename
                self.root.title(f"Matrix Drawer - {os.path.basename(filename)}")
                messagebox.showinfo("Success", "Project loaded successfully!")
            else:
                messagebox.showerror("Error", "Failed to load project!")
    
    def save_project_dialog(self):
        """Сохранение проекта"""
        if not self.matrix_drawer.binary_matrix:
            messagebox.showwarning("Warning", "No project to save!")
            return
        
        if self.current_file:
            if self.matrix_drawer.save_project(self.current_file):
                messagebox.showinfo("Success", "Project saved successfully!")
            else:
                messagebox.showerror("Error", "Failed to save project!")
        else:
            self.save_as_dialog()
    
    def save_as_dialog(self):
        """Диалог сохранения проекта как"""
        if not self.matrix_drawer.binary_matrix:
            messagebox.showwarning("Warning", "No project to save!")
            return
        
        filename = filedialog.asksaveasfilename(
            title="Save Project As",
            defaultextension=".matrix",
            filetypes=[("Matrix Project files", "*.matrix"), ("All files", "*.*")]
        )
        if filename:
            if self.matrix_drawer.save_project(filename):
                self.current_file = filename
                self.root.title(f"Matrix Drawer - {os.path.basename(filename)}")
                messagebox.showinfo("Success", "Project saved successfully!")
            else:
                messagebox.showerror("Error", "Failed to save project!")
    
    def enable_edit_mode(self):
        """Включение режима редактирования"""
        if self.matrix_drawer.binary_matrix:
            self.matrix_drawer.set_edit_mode(True)
    
    def enable_draw_mode(self):
        """Включение режима рисования"""
        if self.matrix_drawer.binary_matrix:
            self.matrix_drawer.set_edit_mode(False)
    
    def clear_points(self):
        """Очистка всех точек"""
        if self.matrix_drawer.binary_matrix and not self.matrix_drawer.edit_mode:
            self.matrix_drawer.points = []
            self.matrix_drawer.redraw_points_and_lines()
    
    def enable_all_cells(self):
        """Включение всех ячеек"""
        if self.matrix_drawer.binary_matrix and self.matrix_drawer.edit_mode:
            for i in range(self.matrix_drawer.rows):
                for j in range(self.matrix_drawer.cols):
                    self.matrix_drawer.binary_matrix[i][j] = 1
            self.matrix_drawer.draw_matrix()
    
    def disable_all_cells(self):
        """Выключение всех ячеек"""
        if self.matrix_drawer.binary_matrix and self.matrix_drawer.edit_mode:
            for i in range(self.matrix_drawer.rows):
                for j in range(self.matrix_drawer.cols):
                    self.matrix_drawer.binary_matrix[i][j] = 0
            self.matrix_drawer.draw_matrix()
    
    def reset_view(self):
        """Сброс масштаба"""
        if self.matrix_drawer.binary_matrix:
            self.matrix_drawer.draw_matrix()
    
    def show_about(self):
        """Показ информации о программе"""
        about_text = """Matrix Drawer v2.0
        
A tool for creating and editing binary matrices
and drawing paths through enabled cells.

Features:
• Create and edit binary matrices
• Draw paths through enabled cells
• Save and load projects
• Visual feedback for path under cells

Created with Python and Tkinter."""
        
        messagebox.showinfo("About Matrix Drawer", about_text)


class NewProjectDialog:
    def __init__(self, parent):
        self.result = None
        
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("New Project")
        self.dialog.geometry("300x250")
        self.dialog.resizable(False, False)
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        # Центрирование окна
        self.dialog.geometry("+%d+%d" % (parent.winfo_rootx() + 50, parent.winfo_rooty() + 50))
        
        self.create_widgets()
        
        # Ожидание закрытия диалога
        parent.wait_window(self.dialog)
    
    def create_widgets(self):
        # Заголовок
        title_label = tk.Label(self.dialog, text="Create New Project", font=("Arial", 12, "bold"))
        title_label.pack(pady=10)
        
        # Имя проекта
        name_frame = tk.Frame(self.dialog)
        name_frame.pack(pady=5)
        tk.Label(name_frame, text="Project Name:").pack(side=tk.LEFT, padx=5)
        self.name_entry = tk.Entry(name_frame, width=20)
        self.name_entry.insert(0, "New Project")
        self.name_entry.pack(side=tk.LEFT)
        
        # Размер матрицы
        size_frame = tk.Frame(self.dialog)
        size_frame.pack(pady=10)
        
        tk.Label(size_frame, text="Rows:").grid(row=0, column=0, padx=5, pady=5)
        self.rows_var = tk.StringVar(value="8")
        self.rows_spinbox = tk.Spinbox(size_frame, from_=1, to=50, textvariable=self.rows_var, width=10)
        self.rows_spinbox.grid(row=0, column=1, padx=5, pady=5)
        
        tk.Label(size_frame, text="Columns:").grid(row=1, column=0, padx=5, pady=5)
        self.cols_var = tk.StringVar(value="8")
        self.cols_spinbox = tk.Spinbox(size_frame, from_=1, to=50, textvariable=self.cols_var, width=10)
        self.cols_spinbox.grid(row=1, column=1, padx=5, pady=5)
        
        # Информация
        info_label = tk.Label(self.dialog, text="All cells will be enabled by default", font=("Arial", 8))
        info_label.pack(pady=5)
        
        # Кнопки
        button_frame = tk.Frame(self.dialog)
        button_frame.pack(pady=20)
        
        tk.Button(button_frame, text="Create", command=self.on_ok, width=10).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="Cancel", command=self.on_cancel, width=10).pack(side=tk.LEFT, padx=5)
        
        self.dialog.bind('<Return>', lambda e: self.on_ok())
        self.dialog.bind('<Escape>', lambda e: self.on_cancel())
    
    def on_ok(self):
        try:
            rows = int(self.rows_var.get())
            cols = int(self.cols_var.get())
            name = self.name_entry.get().strip()
            
            if not name:
                name = "Untitled"
            
            if rows > 0 and cols > 0:
                self.result = (rows, cols, name)
                self.dialog.destroy()
            else:
                messagebox.showerror("Error", "Rows and columns must be positive numbers!")
        except ValueError:
            messagebox.showerror("Error", "Invalid input values!")
    
    def on_cancel(self):
        self.dialog.destroy()