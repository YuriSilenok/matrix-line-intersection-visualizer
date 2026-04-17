import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
from datetime import datetime


class LayerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Создание проекта слоёв")
        self.root.geometry("500x500")
        self.root.resizable(True, True)

        # Основные переменные
        self.num_longitudinal = tk.IntVar(value=0)
        self.longitudinal_frames = []
        self.num_transverse = tk.IntVar(value=0)

        # Главный фрейм с прокруткой
        self.main_canvas = tk.Canvas(root)
        self.scrollbar = ttk.Scrollbar(root, orient="vertical", command=self.main_canvas.yview)
        self.scrollable_frame = ttk.Frame(self.main_canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.main_canvas.configure(scrollregion=self.main_canvas.bbox("all"))
        )

        self.main_canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.main_canvas.configure(yscrollcommand=self.scrollbar.set)

        # Фрейм для ввода количества продольных слоёв
        self.input_frame = ttk.LabelFrame(self.scrollable_frame, text="Общие параметры", padding=10)
        self.input_frame.pack(fill="x", padx=10, pady=10)

        ttk.Label(self.input_frame, text="Количество продольных слоёв:").grid(row=0, column=0, sticky="w", padx=5,
                                                                              pady=5)
        self.longitudinal_spinbox = ttk.Spinbox(self.input_frame, from_=0, to=20, textvariable=self.num_longitudinal,
                                                width=10, command=self.on_longitudinal_change)
        self.longitudinal_spinbox.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(self.input_frame, text="Количество поперечных слоёв:").grid(row=1, column=0, sticky="w", padx=5,
                                                                              pady=5)
        self.transverse_spinbox = ttk.Spinbox(self.input_frame, from_=0, to=20, textvariable=self.num_transverse,
                                              width=10, command=self.on_transverse_change)
        self.transverse_spinbox.grid(row=1, column=1, padx=5, pady=5)

        # Фрейм для динамических данных продольных слоёв
        self.longitudinal_container = ttk.LabelFrame(self.scrollable_frame, text="Продольные слои и подслои",
                                                     padding=10)
        self.longitudinal_container.pack(fill="x", padx=10, pady=10)

        # Фрейм для информации о поперечных слоях
        self.transverse_container = ttk.LabelFrame(self.scrollable_frame, text="Поперечные слои", padding=10)
        self.transverse_container.pack(fill="x", padx=10, pady=10)

        # Кнопка сохранения
        self.save_button = ttk.Button(self.scrollable_frame, text="Создать конфигурацию проекта",
                                      command=self.create_project)
        self.save_button.pack(pady=20)

        self.main_canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

    def on_longitudinal_change(self):
        """Обработчик изменения количества продольных слоёв"""
        # Очищаем контейнер
        for widget in self.longitudinal_container.winfo_children():
            widget.destroy()

        self.longitudinal_frames = []
        num_layers = self.num_longitudinal.get()

        if num_layers == 0:
            ttk.Label(self.longitudinal_container, text="Нет продольных слоёв").pack()
            return

        # Создаём заголовки
        header_frame = ttk.Frame(self.longitudinal_container)
        header_frame.pack(fill="x", pady=5)
        ttk.Label(header_frame, text="Слой", width=10).pack(side="left", padx=5)
        ttk.Label(header_frame, text="Количество подслоёв", width=20).pack(side="left", padx=5)

        # Создаём поля для каждого слоя
        for i in range(num_layers):
            layer_frame = ttk.Frame(self.longitudinal_container)
            layer_frame.pack(fill="x", pady=2)

            ttk.Label(layer_frame, text=f"Слой {i + 1}", width=10).pack(side="left", padx=5)

            sublayer_var = tk.IntVar(value=0)
            sublayer_spinbox = ttk.Spinbox(layer_frame, from_=0, to=50, textvariable=sublayer_var, width=18)
            sublayer_spinbox.pack(side="left", padx=5)

            self.longitudinal_frames.append({
                'layer_num': i + 1,
                'var': sublayer_var
            })

    def on_transverse_change(self):
        """Обработчик изменения количества поперечных слоёв"""
        # Очищаем контейнер
        for widget in self.transverse_container.winfo_children():
            widget.destroy()

        num_layers = self.num_transverse.get()

        if num_layers == 0:
            ttk.Label(self.transverse_container, text="Нет поперечных слоёв").pack()
            return

        # Просто показываем количество поперечных слоёв
        ttk.Label(self.transverse_container, text=f"Количество поперечных слоёв: {num_layers}",
                  font=('Arial', 10, 'bold')).pack(pady=5)

    def create_project(self):
        """Создание конфигурации проекта и открытие окна проекта"""
        # Проверяем ввод
        num_long = self.num_longitudinal.get()
        num_trans = self.num_transverse.get()

        if num_long == 0 and num_trans == 0:
            messagebox.showwarning("Предупреждение", "Не указано ни одного слоя!")
            return

        # Собираем данные
        project_data = {
            'project_name': f"Project_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            'created_at': datetime.now().isoformat(),
            'longitudinal_layers': [],
            'transverse_layers_count': num_trans
        }

        for layer in self.longitudinal_frames:
            sublayers = layer['var'].get()
            project_data['longitudinal_layers'].append({
                'layer_number': layer['layer_num'],
                'sublayers_count': sublayers
            })

        # Сохраняем в JSON файл
        filename = f"{project_data['project_name']}.json"
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(project_data, f, ensure_ascii=False, indent=4)

        messagebox.showinfo("Успех", f"Конфигурация сохранена в файл:\n{filename}")

        # Открываем окно проекта
        self.open_project_window(project_data)

    def open_project_window(self, project_data):
        """Открытие окна проекта с отображением кругов"""
        project_window = tk.Toplevel(self.root)
        project_window.title(f"Проект: {project_data['project_name']}")
        project_window.geometry("800x600")
        project_window.minsize(600, 400)

        # Создаём основной фрейм
        main_frame = ttk.Frame(project_window)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Информационная панель
        info_frame = ttk.LabelFrame(main_frame, text="Информация о проекте", padding=10)
        info_frame.pack(fill="x", pady=(0, 10))

        info_text = f"Продольные слои: {len(project_data['longitudinal_layers'])}\n"
        for layer in project_data['longitudinal_layers']:
            info_text += f"  • Слой {layer['layer_number']}: {layer['sublayers_count']} подслоёв\n"
        info_text += f"Поперечные слои: {project_data['transverse_layers_count']}"

        ttk.Label(info_frame, text=info_text, justify="left").pack(anchor="w")

        # Canvas для отображения кругов
        canvas_frame = ttk.LabelFrame(main_frame, text="Визуализация поперечных слоёв", padding=10)
        canvas_frame.pack(fill="both", expand=True)

        canvas = tk.Canvas(canvas_frame, bg='white', highlightthickness=1, highlightbackground='gray')
        canvas.pack(fill="both", expand=True)

        # Рисуем круги
        self.draw_circles(canvas, project_data['transverse_layers_count'])

        # Добавляем информацию о кругах
        legend_frame = ttk.Frame(main_frame)
        legend_frame.pack(fill="x", pady=(10, 0))

        ttk.Label(legend_frame, text=f"● Каждый круг соответствует одному поперечному слою",
                  foreground="blue").pack(side="left", padx=10)
        ttk.Label(legend_frame, text=f"Всего: {project_data['transverse_layers_count']} кругов",
                  font=('Arial', 9, 'bold')).pack(side="right", padx=10)

        # Кнопка закрытия
        close_button = ttk.Button(main_frame, text="Закрыть", command=project_window.destroy)
        close_button.pack(pady=10)

        # Обработчик изменения размера окна
        def on_resize(event=None):
            self.draw_circles(canvas, project_data['transverse_layers_count'])

        canvas.bind("<Configure>", on_resize)

    def draw_circles(self, canvas, num_circles):
        """Рисование кругов на Canvas вертикально"""
        if num_circles == 0:
            canvas.create_text(canvas.winfo_width() // 2, canvas.winfo_height() // 2,
                               text="Нет поперечных слоёв", font=('Arial', 14, 'bold'), fill='gray')
            return

        canvas.delete("all")

        # Получаем размеры canvas
        width = canvas.winfo_width()
        height = canvas.winfo_height()

        if width <= 1 or height <= 1:
            return

        # Параметры кругов
        circle_radius = min(width * 0.1, 50)  # Радиус круга
        spacing = circle_radius * 2.5  # Расстояние между кругами
        total_height = num_circles * spacing
        start_y = (height - total_height) // 2  # Вертикальное центрирование

        # Цветовая схема
        colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7',
                  '#DDA0DD', '#98D8C8', '#F7DC6F', '#BB8FCE', '#85C1E2']

        # Рисуем круги
        for i in range(num_circles):
            x = width // 2  # Горизонтальное центрирование
            y = start_y + i * spacing + circle_radius

            # Выбираем цвет
            color = colors[i % len(colors)]

            # Рисуем круг
            circle = canvas.create_oval(x - circle_radius, y - circle_radius,
                                        x + circle_radius, y + circle_radius,
                                        fill=color, outline='black', width=2)

            # Добавляем номер слоя
            canvas.create_text(x, y, text=str(i + 1), font=('Arial', int(circle_radius * 0.8), 'bold'))

            # Добавляем подпись (опционально)
            if i % 2 == 0:  # Для некоторых кругов добавляем подпись справа
                canvas.create_text(x + circle_radius + 10, y,
                                   text=f"Слой {i + 1}",
                                   anchor="w", font=('Arial', 9), fill='gray')
            else:  # Для остальных слева
                canvas.create_text(x - circle_radius - 10, y,
                                   text=f"Слой {i + 1}",
                                   anchor="e", font=('Arial', 9), fill='gray')


def main():
    root = tk.Tk()
    app = LayerApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()