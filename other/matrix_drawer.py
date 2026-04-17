import tkinter as tk
import math
import json

class MatrixDrawer:
    def __init__(self, root):
        self.root = root
        self.root.title("Matrix Drawer")
        
        # Данные
        self.binary_matrix = []
        self.rows = 0
        self.cols = 0
        self.edit_mode = True  # True - режим редактирования ячеек, False - режим рисования нити
        self.project_name = "Untitled"
        
        # Параметры отображения
        self.cell_size = 0
        self.margin = 20
        self.circles = []
        self.points = []
        self.lines = []
        self.hover_circle = None
        self.gray_circles = set()
        
        # Настройка canvas
        self.canvas = tk.Canvas(root, bg='white', highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=True)
        
        # Привязка событий
        self.canvas.bind('<Configure>', self.on_resize)
        self.canvas.bind('<Motion>', self.on_mouse_move)
        self.canvas.bind('<Button-1>', self.on_left_click)
        self.canvas.bind('<Button-3>', self.on_right_click)
        
        # Информационная метка
        self.info_label = tk.Label(root, text="No project created")
        self.info_label.pack(side=tk.BOTTOM, pady=5)
        
        # Статус режима
        self.mode_label = tk.Label(root, text="", font=("Arial", 10, "bold"))
        self.mode_label.pack(side=tk.BOTTOM, pady=2)
    
    def create_new_project(self, rows, cols, project_name="Untitled"):
        """Создание нового проекта с матрицей заданного размера"""
        self.rows = rows
        self.cols = cols
        self.project_name = project_name
        # Все ячейки изначально включены (1)
        self.binary_matrix = [[1 for _ in range(cols)] for _ in range(rows)]
        self.edit_mode = True
        self.points = []
        self.lines = []
        self.gray_circles.clear()
        self.update_mode_label()
        self.draw_matrix()
    
    def load_project(self, filename):
        """Загрузка проекта из файла"""
        try:
            with open(filename, 'r') as f:
                data = json.load(f)
                self.rows = data['rows']
                self.cols = data['cols']
                self.binary_matrix = data['matrix']
                self.project_name = data.get('name', 'Untitled')
                self.edit_mode = True
                self.points = []
                self.lines = []
                self.gray_circles.clear()
                self.update_mode_label()
                self.draw_matrix()
                return True
        except Exception as e:
            print(f"Error loading project: {e}")
            return False
    
    def save_project(self, filename):
        """Сохранение проекта в файл"""
        try:
            data = {
                'name': self.project_name,
                'rows': self.rows,
                'cols': self.cols,
                'matrix': self.binary_matrix
            }
            with open(filename, 'w') as f:
                json.dump(data, f, indent=2)
            return True
        except Exception as e:
            print(f"Error saving project: {e}")
            return False
    
    def toggle_cell(self, row, col):
        """Переключение состояния ячейки (только в режиме редактирования)"""
        if not self.edit_mode:
            return
        
        if 0 <= row < self.rows and 0 <= col < self.cols:
            self.binary_matrix[row][col] = 1 - self.binary_matrix[row][col]
            self.draw_matrix()
    
    def set_edit_mode(self, mode):
        """Установка режима работы"""
        self.edit_mode = mode
        if not mode:
            # При переходе в режим рисования очищаем линии
            self.points = []
            self.lines = []
            self.gray_circles.clear()
        self.update_mode_label()
        self.draw_matrix()
    
    def update_mode_label(self):
        """Обновление метки режима"""
        if not self.binary_matrix:
            self.mode_label.config(text="")
            return
        
        mode_text = "✏️ EDIT MODE" if self.edit_mode else "🎨 DRAW MODE"
        self.mode_label.config(text=f"{self.project_name} - {mode_text}")
    
    def update_info_label(self):
        """Обновление информационной метки"""
        if not self.binary_matrix:
            self.info_label.config(text="No project created")
            return
        
        enabled_cells = sum(sum(row) for row in self.binary_matrix)
        total_cells = self.rows * self.cols
        self.info_label.config(
            text=f"Matrix: {self.rows}x{self.cols} | Enabled: {enabled_cells}/{total_cells} | Cell size: {self.cell_size:.1f}px"
        )
    
    def on_resize(self, event):
        """Обработка изменения размера окна"""
        self.draw_matrix()
    
    def calculate_cell_size(self):
        """Вычисление размера ячейки"""
        if not self.binary_matrix:
            return 20
        
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()
        
        if canvas_width <= 1 or canvas_height <= 1:
            return 20
        
        if self.cols == 0 or self.rows == 0:
            return 20
        
        available_width = canvas_width - 2 * self.margin
        available_height = canvas_height - 2 * self.margin
        
        cell_by_width = available_width / self.cols
        cell_by_height = available_height / self.rows
        
        return min(cell_by_width, cell_by_height)
    
    def is_point_below_line(self, point, line_start, line_end):
        """Проверяет, находится ли точка под линией"""
        x0, y0 = line_start
        x1, y1 = line_end
        x, y = point
        
        if x0 < x1 and (x < x0 or x > x1):
            return False
        if x1 < x0 and (x < x1 or x > x0):
            return False
        if y0 < y1 and (y < y0 or y > y1):
            return False
        if y1 < y0 and (y < y1 or y > y0):
            return False

        if x1 - x0 == 0:
            return x > x0
        
        k = (y1 - y0) / (x1 - x0)
        y_on_line = k * (x - x0) + y0
        
        return y >= y_on_line
    
    def update_gray_circles(self):
        """Обновляет список кругов под линиями"""
        if len(self.points) < 2:
            for circle_id in self.gray_circles:
                for circle_data in self.circles:
                    if circle_data['id'] == circle_id:
                        self.canvas.itemconfig(circle_id, fill='white')
                        break
            self.gray_circles.clear()
            return
        
        circles_under_lines = set()
        
        for i in range(len(self.points) - 1):
            line_start = self.points[i]
            line_end = self.points[i + 1]
            
            for circle_data in self.circles:
                center = circle_data['center']
                real_line_start = line_start[0], line_start[1] + self.cell_size / 4 + 2
                real_line_end = line_end[0], line_end[1] + self.cell_size / 4 + 2
                if self.is_point_below_line(center, real_line_start, real_line_end):
                    circles_under_lines.add(circle_data['id'])
        
        for circle_data in self.circles:
            if circle_data['id'] not in self.gray_circles:
                if self.hover_circle != circle_data['id']:
                    self.canvas.itemconfig(circle_data['id'], fill='white')
        
        for circle_id in circles_under_lines:
            for circle_data in self.circles:
                if circle_data['id'] == circle_id:
                    if self.hover_circle != circle_id:
                        self.canvas.itemconfig(circle_id, fill='lightgray')
                    break
        
        self.gray_circles = circles_under_lines
        
        if self.hover_circle and self.hover_circle in self.gray_circles:
            for circle_data in self.circles:
                if circle_data['id'] == self.hover_circle:
                    self.canvas.itemconfig(self.hover_circle, fill='lightgreen')
                    break
    
    def draw_matrix(self):
        """Отрисовка матрицы"""
        if not self.binary_matrix:
            self.canvas.delete("all")
            self.canvas.create_text(self.canvas.winfo_width()//2, self.canvas.winfo_height()//2,
                                   text="No project created.\nUse File → New Project to start.",
                                   font=("Arial", 14), justify=tk.CENTER)
            return
        
        self.canvas.delete("all")
        self.circles = []
        self.hover_circle = None
        
        self.cell_size = self.calculate_cell_size()
        circle_radius = self.cell_size / 4
        
        total_width = self.cols * self.cell_size
        total_height = self.rows * self.cell_size
        
        start_x = (self.canvas.winfo_width() - total_width) / 2
        start_y = (self.canvas.winfo_height() - total_height) / 2
        
        self.update_info_label()
        
        # Рисуем границу матрицы
        self.canvas.create_rectangle(
            start_x, start_y,
            start_x + total_width, start_y + total_height,
            outline='black', fill='white', width=2
        )
        
        # Рисуем ячейки
        for i in range(self.rows):
            for j in range(self.cols):
                x1 = start_x + j * self.cell_size
                y1 = start_y + i * self.cell_size
                x2 = x1 + self.cell_size
                y2 = y1 + self.cell_size
                
                # Определяем цвет фона ячейки
                if self.binary_matrix[i][j] == 1:
                    fill_color = 'white'
                else:
                    fill_color = '#f0f0f0'  # Серый фон для выключенных ячеек
                
                self.canvas.create_rectangle(x1, y1, x2, y2, outline='gray', fill=fill_color, width=1)
                
                # Рисуем круг только для включенных ячеек
                if self.binary_matrix[i][j] == 1:
                    center_x = x1 + self.cell_size / 2
                    center_y = y1 + self.cell_size / 2
                    circle = self.canvas.create_oval(
                        center_x - circle_radius, center_y - circle_radius,
                        center_x + circle_radius, center_y + circle_radius,
                        outline='black', fill='white', width=1
                    )
                    
                    self.circles.append({
                        'id': circle,
                        'center': (center_x, center_y),
                        'radius': circle_radius,
                        'row': i,
                        'col': j,
                        'x1': x1, 'y1': y1, 'x2': x2, 'y2': y2
                    })
        
        self.redraw_points_and_lines()
    
    def redraw_points_and_lines(self):
        """Перерисовка точек и линий"""
        for line_id in self.lines:
            self.canvas.delete(line_id)
        self.lines = []
        
        if not self.edit_mode and len(self.points) > 1:
            for i in range(len(self.points) - 1):
                line = self.canvas.create_line(
                    self.points[i][0], self.points[i][1],
                    self.points[i + 1][0], self.points[i + 1][1],
                    fill='blue', width=2
                )
                self.lines.append(line)
        
        for point in self.points:
            color = 'red' if not self.edit_mode else 'green'
            self.canvas.create_oval(
                point[0] - 5, point[1] - 5,
                point[0] + 5, point[1] + 5,
                fill=color, outline='black', width=1
            )
        
        if not self.edit_mode:
            self.update_gray_circles()
    
    def on_mouse_move(self, event):
        """Обработка движения мыши"""
        if not self.binary_matrix:
            return
        
        for circle_data in self.circles:
            center_x, center_y = circle_data['center']
            radius = circle_data['radius']
            
            distance = math.sqrt((event.x - center_x)**2 + (event.y - center_y)**2)
            
            if distance <= radius:
                if self.hover_circle != circle_data['id']:
                    if self.hover_circle:
                        if not self.edit_mode and self.hover_circle in self.gray_circles:
                            self.canvas.itemconfig(self.hover_circle, fill='lightgray')
                        else:
                            self.canvas.itemconfig(self.hover_circle, fill='white')
                    
                    self.canvas.itemconfig(circle_data['id'], fill='lightgreen')
                    self.hover_circle = circle_data['id']
                    
                    status = "ON" if self.binary_matrix[circle_data['row']][circle_data['col']] == 1 else "OFF"
                    self.info_label.config(
                        text=f"Row {circle_data['row'] + 1}, Col {circle_data['col'] + 1} [{status}]"
                    )
                return
        
        if self.hover_circle:
            if not self.edit_mode and self.hover_circle in self.gray_circles:
                self.canvas.itemconfig(self.hover_circle, fill='lightgray')
            else:
                self.canvas.itemconfig(self.hover_circle, fill='white')
            self.hover_circle = None
            self.update_info_label()
    
    def on_left_click(self, event):
        """Обработка левого клика"""
        if not self.binary_matrix:
            return
        
        # В режиме редактирования - переключение ячейки
        if self.edit_mode:
            # Проверяем, кликнули ли по ячейке
            for circle_data in self.circles:
                x1, y1 = circle_data['x1'], circle_data['y1']
                x2, y2 = circle_data['x2'], circle_data['y2']
                
                if x1 <= event.x <= x2 and y1 <= event.y <= y2:
                    self.toggle_cell(circle_data['row'], circle_data['col'])
                    break
        else:
            # В режиме рисования - добавление точки
            for circle_data in self.circles:
                center_x, center_y = circle_data['center']
                radius = circle_data['radius']
                
                distance = math.sqrt((event.x - center_x)**2 + (event.y - center_y)**2)
                
                if distance <= radius:
                    point_x = center_x
                    point_y = center_y - radius - 2
                    
                    self.points.append((point_x, point_y))
                    self.redraw_points_and_lines()
                    break
    
    def on_right_click(self, event):
        """Обработка правого клика"""
        if not self.binary_matrix:
            return
        
        if not self.edit_mode and self.points:
            self.points.pop()
            self.redraw_points_and_lines()