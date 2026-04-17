import tkinter as tk

class Toolbar:
    def __init__(self, root, matrix_drawer):
        self.root = root
        self.matrix_drawer = matrix_drawer
        
        # Создаем панель инструментов
        self.toolbar_frame = tk.Frame(root, bd=1, relief=tk.RAISED)
        self.toolbar_frame.pack(side=tk.TOP, fill=tk.X)
        
        # Кнопки инструментов
        self.create_toolbar_buttons()
        
        # Разделитель
        tk.Frame(root, height=2, bd=1, relief=tk.SUNKEN).pack(side=tk.TOP, fill=tk.X)
    
    def create_toolbar_buttons(self):
        # Кнопка Edit Mode
        self.edit_btn = tk.Button(self.toolbar_frame, text="✏️ Edit Cells", 
                                  command=self.enable_edit_mode, padx=5, pady=2)
        self.edit_btn.pack(side=tk.LEFT, padx=2, pady=2)
        
        # Кнопка Draw Mode
        self.draw_btn = tk.Button(self.toolbar_frame, text="🎨 Draw Thread", 
                                  command=self.enable_draw_mode, padx=5, pady=2)
        self.draw_btn.pack(side=tk.LEFT, padx=2, pady=2)
        
        # Разделитель
        tk.Label(self.toolbar_frame, text="|").pack(side=tk.LEFT, padx=5)
        
        # Кнопка Enable All
        self.enable_all_btn = tk.Button(self.toolbar_frame, text="✓ Enable All", 
                                        command=self.enable_all_cells, padx=5, pady=2)
        self.enable_all_btn.pack(side=tk.LEFT, padx=2, pady=2)
        
        # Кнопка Disable All
        self.disable_all_btn = tk.Button(self.toolbar_frame, text="✗ Disable All", 
                                         command=self.disable_all_cells, padx=5, pady=2)
        self.disable_all_btn.pack(side=tk.LEFT, padx=2, pady=2)
        
        # Разделитель
        tk.Label(self.toolbar_frame, text="|").pack(side=tk.LEFT, padx=5)
        
        # Кнопка Clear Points
        self.clear_btn = tk.Button(self.toolbar_frame, text="🗑️ Clear Points", 
                                   command=self.clear_points, padx=5, pady=2)
        self.clear_btn.pack(side=tk.LEFT, padx=2, pady=2)
        
        # Статус режима
        self.mode_label = tk.Label(self.toolbar_frame, text="", font=("Arial", 9, "bold"))
        self.mode_label.pack(side=tk.RIGHT, padx=10)
        
        self.update_button_states()
    
    def update_button_states(self):
        """Обновление состояния кнопок в зависимости от режима"""
        if not self.matrix_drawer.binary_matrix:
            state = tk.DISABLED
            mode_text = "No Project"
        else:
            state = tk.NORMAL
            if self.matrix_drawer.edit_mode:
                mode_text = "✏️ EDIT MODE"
                self.edit_btn.config(relief=tk.SUNKEN, bg='lightblue')
                self.draw_btn.config(relief=tk.RAISED, bg='SystemButtonFace')
                self.enable_all_btn.config(state=tk.NORMAL)
                self.disable_all_btn.config(state=tk.NORMAL)
                self.clear_btn.config(state=tk.DISABLED)
            else:
                mode_text = "🎨 DRAW MODE"
                self.edit_btn.config(relief=tk.RAISED, bg='SystemButtonFace')
                self.draw_btn.config(relief=tk.SUNKEN, bg='lightgreen')
                self.enable_all_btn.config(state=tk.DISABLED)
                self.disable_all_btn.config(state=tk.DISABLED)
                self.clear_btn.config(state=tk.NORMAL)
        
        self.mode_label.config(text=mode_text)
        
        # Обновляем состояние всех кнопок
        for child in self.toolbar_frame.winfo_children():
            if isinstance(child, tk.Button) and child not in [self.edit_btn, self.draw_btn]:
                if not self.matrix_drawer.binary_matrix:
                    child.config(state=tk.DISABLED)
    
    def enable_edit_mode(self):
        if self.matrix_drawer.binary_matrix:
            self.matrix_drawer.set_edit_mode(True)
            self.update_button_states()
    
    def enable_draw_mode(self):
        if self.matrix_drawer.binary_matrix:
            self.matrix_drawer.set_edit_mode(False)
            self.update_button_states()
    
    def enable_all_cells(self):
        if self.matrix_drawer.binary_matrix and self.matrix_drawer.edit_mode:
            for i in range(self.matrix_drawer.rows):
                for j in range(self.matrix_drawer.cols):
                    self.matrix_drawer.binary_matrix[i][j] = 1
            self.matrix_drawer.draw_matrix()
    
    def disable_all_cells(self):
        if self.matrix_drawer.binary_matrix and self.matrix_drawer.edit_mode:
            for i in range(self.matrix_drawer.rows):
                for j in range(self.matrix_drawer.cols):
                    self.matrix_drawer.binary_matrix[i][j] = 0
            self.matrix_drawer.draw_matrix()
    
    def clear_points(self):
        if self.matrix_drawer.binary_matrix and not self.matrix_drawer.edit_mode:
            self.matrix_drawer.points = []
            self.matrix_drawer.redraw_points_and_lines()