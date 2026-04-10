import tkinter as tk
import math

class MatrixDrawer:
    def __init__(self, root, filename):
        self.root = root
        self.root.title("Matrix Drawer")
        
        # Загрузка матриц из файла
        self.matrices = self.load_matrices(filename)
        
        # Параметры отображения
        self.cell_size = 0  # будет вычислен при изменении размера
        self.margin = 20
        self.matrix_gap = 0  # отступ между матрицами (0 по условию)
        self.circles = []  # список всех кругов (для кликов)
        self.points = []   # список точек (x, y)
        self.lines = []    # список линий (id на canvas)
        self.hover_circle = None
        
        # Настройка canvas
        self.canvas = tk.Canvas(root, bg='white', highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=True)
        
        # Привязка событий
        self.canvas.bind('<Configure>', self.on_resize)
        self.canvas.bind('<Motion>', self.on_mouse_move)
        self.canvas.bind('<Button-1>', self.on_left_click)
        self.canvas.bind('<Button-3>', self.on_right_click)
        
        # Информационная метка
        self.info_label = tk.Label(root, text="")
        self.info_label.pack(side=tk.BOTTOM, pady=5)
        
        # Рисуем все матрицы
        self.draw_all_matrices()
    
    def load_matrices(self, filename):
        """Загрузка матриц из файла"""
        matrices = []
        try:
            with open(filename, 'r') as f:
                for line in f.readlines():
                    if not line:
                        continue
                    n, m = map(int, line.split())
                    matrices.append((n, m))
        except FileNotFoundError:
            print(f"Файл {filename} не найден!")
            return []
        
        return matrices
    
    def on_resize(self, event):
        """Обработка изменения размера окна"""
        self.draw_all_matrices()
    
    
    def calculate_cell_size(self):
        """Вычисление размера ячейки на основе текущего размера canvas и всех матриц"""
        if not self.matrices:
            return 20
        
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()
        
        if canvas_width <= 1 or canvas_height <= 1:
            return 20
        
        # Вычисляем общее количество столбцов во всех матрицах
        total_cols = sum(m[1] for m in self.matrices)
        
        # Находим максимальное количество строк среди всех матриц
        max_rows = max(m[0] for m in self.matrices)
        
        if total_cols == 0 or max_rows == 0:
            return 20
        
        # Вычисляем доступное пространство для всех матриц
        available_width = canvas_width - 2 * self.margin
        available_height = canvas_height - 2 * self.margin
        
        # Размер ячейки (минимальный из доступных)
        cell_by_width = available_width / total_cols if total_cols > 0 else 20
        cell_by_height = available_height / max_rows if max_rows > 0 else 20
        
        return min(cell_by_width, cell_by_height)
    
    def draw_all_matrices(self):
        """Отрисовка всех матриц на одном canvas"""
        if not self.matrices:
            self.canvas.delete("all")
            self.canvas.create_text(self.canvas.winfo_width()//2, self.canvas.winfo_height()//2,
                                   text="No matrices loaded", font=("Arial", 16))
            return
        
        # Очищаем canvas и списки
        self.canvas.delete("all")
        self.circles = []
        self.points = []
        self.lines = []
        self.hover_circle = None
        
        # Вычисляем размер ячейки
        self.cell_size = self.calculate_cell_size()
        circle_radius = self.cell_size / 4  # диаметр в 2 раза меньше ячейки
        
        # Вычисляем общую ширину всех матриц
        total_width = sum(m[1] * self.cell_size for m in self.matrices)
        
        # Находим максимальную высоту среди всех матриц
        max_rows = max(m[0] for m in self.matrices)
        max_height = max_rows * self.cell_size
        
        # Начальная позиция по X (центрируем все матрицы вместе)
        start_x = (self.canvas.winfo_width() - total_width) / 2
        
        # Начальная позиция по Y (выравнивание по нижнему краю)
        start_y = self.canvas.winfo_height() - self.margin - max_height
        
        # Обновляем информационную метку
        total_matrices = len(self.matrices)
        self.info_label.config(text=f"Total matrices: {total_matrices} | Cell size: {self.cell_size:.1f}px")
        
        current_x = start_x
        
        # Рисуем каждую матрицу
        for matrix_idx, matrix in enumerate(self.matrices):
            rows, cols = matrix
            
            if rows == 0 or cols == 0:
                continue
            
            # Высота текущей матрицы
            matrix_height = rows * self.cell_size

            # Рисуем границу матрицы
            x1 = current_x
            y1 = start_y + (max_height - matrix_height)
            x2 = current_x  + self.cell_size * cols
            y2 = start_y + max_height
            self.canvas.create_rectangle(x1, y1, x2, y2, outline='black', fill='', width=2)
            
            # Y-координата для выравнивания по нижнему краю
            matrix_start_y = start_y + (max_height - matrix_height)
            
            # Рисуем сетку и круги для текущей матрицы
            for i in range(rows):
                for j in range(cols):
                    x1 = current_x + j * self.cell_size
                    y1 = matrix_start_y + i * self.cell_size
                    x2 = x1 + self.cell_size
                    y2 = y1 + self.cell_size
                    
                    # Рисуем границу ячейки
                    self.canvas.create_rectangle(x1, y1, x2, y2, outline='black', fill='', width=1)
                    
                    # Рисуем круг в центре ячейки
                    center_x = x1 + self.cell_size / 2
                    center_y = y1 + self.cell_size / 2
                    circle = self.canvas.create_oval(
                        center_x - circle_radius, center_y - circle_radius,
                        center_x + circle_radius, center_y + circle_radius,
                        outline='black', fill='white', width=1
                    )
                    
                    # Сохраняем информацию о круге
                    self.circles.append({
                        'id': circle,
                        'center': (center_x, center_y),
                        'radius': circle_radius,
                        'matrix_idx': matrix_idx,
                        'row': i,
                        'col': j,
                        'x1': x1, 'y1': y1, 'x2': x2, 'y2': y2
                    })
            
            # Перемещаем X-координату для следующей матрицы
            current_x += cols * self.cell_size + self.matrix_gap
        
        # Рисуем сохраненные точки и линии
        self.redraw_points_and_lines()
    
    def redraw_points_and_lines(self):
        """Перерисовка всех точек и линий"""
        # Удаляем старые линии
        for line_id in self.lines:
            self.canvas.delete(line_id)
        self.lines = []
        
        # Рисуем линии
        for i in range(len(self.points) - 1):
            line = self.canvas.create_line(
                self.points[i][0], self.points[i][1],
                self.points[i + 1][0], self.points[i + 1][1],
                fill='black', width=2
            )
            self.lines.append(line)
        
        # Рисуем точки (черные залитые круги)
        for point in self.points:
            self.canvas.create_oval(
                point[0] - 4, point[1] - 4,
                point[0] + 4, point[1] + 4,
                fill='black', outline='black'
            )
    
    def on_mouse_move(self, event):
        """Обработка движения мыши для подсветки круга"""
        if not self.matrices:
            return
        
        # Проверяем, находится ли курсор над каким-либо кругом
        for circle_data in self.circles:
            center_x, center_y = circle_data['center']
            radius = circle_data['radius']
            
            # Вычисляем расстояние от курсора до центра круга
            distance = math.sqrt((event.x - center_x)**2 + (event.y - center_y)**2)
            
            if distance <= radius:
                # Подсвечиваем круг зеленым
                if self.hover_circle != circle_data['id']:
                    # Сбрасываем предыдущую подсветку
                    if self.hover_circle:
                        for cd in self.circles:
                            if cd['id'] == self.hover_circle:
                                self.canvas.itemconfig(cd['id'], fill='white')
                                break
                    
                    # Подсвечиваем новый круг
                    self.canvas.itemconfig(circle_data['id'], fill='lightgreen')
                    self.hover_circle = circle_data['id']
                    
                    # Обновляем информацию
                    self.info_label.config(
                        text=f"Matrix {circle_data['matrix_idx'] + 1}, Row {circle_data['row'] + 1}, Col {circle_data['col'] + 1}"
                    )
                return
        
        # Если курсор не над кругом, сбрасываем подсветку
        if self.hover_circle:
            for circle_data in self.circles:
                if circle_data['id'] == self.hover_circle:
                    self.canvas.itemconfig(circle_data['id'], fill='white')
                    break
            self.hover_circle = None
            total_matrices = len(self.matrices)
            self.info_label.config(text=f"Total matrices: {total_matrices} | Cell size: {self.cell_size:.1f}px")
    
    def on_left_click(self, event):
        """Обработка левого клика мыши"""
        if not self.matrices:
            return
        
        # Проверяем, кликнули ли по кругу
        for circle_data in self.circles:
            center_x, center_y = circle_data['center']
            radius = circle_data['radius']
            
            distance = math.sqrt((event.x - center_x)**2 + (event.y - center_y)**2)
            
            if distance <= radius:
                # Точка ставится выше круга (в верхней части ячейки)
                point_x = center_x
                point_y = center_y - radius - 2  # выше круга
                
                # Добавляем точку
                self.points.append((point_x, point_y))
                
                # Перерисовываем точки и линии
                self.redraw_points_and_lines()
                break
    
    def on_right_click(self, event):
        """Обработка правого клика мыши (удаление последней точки)"""
        if self.points:
            self.points.pop()
            self.redraw_points_and_lines()

def main():
    root = tk.Tk()
    
    # Создаем тестовый файл, если его нет
    import os
    if not os.path.exists('matrices.txt'):
        with open('matrices.txt', 'w') as f:
            f.write("1 1\n")
            f.write("1 2\n")
            f.write("2 1\n")
            f.write("2 2\n")
            f.write("\n")
            f.write("3 3\n")
            f.write("3 3\n")
            f.write("3 3\n")
            f.write("\n")
            f.write("2 4\n")
            f.write("4 2\n")
            f.write("3 3\n")
    
    app = MatrixDrawer(root, 'matrices.txt')
    
    # Устанавливаем начальный размер окна
    root.geometry("1000x600")
    root.mainloop()

if __name__ == "__main__":
    main()