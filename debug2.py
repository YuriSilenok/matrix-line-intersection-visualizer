import math
import random
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
import os
import sys

def find_non_intersecting_tangents(A, B, O, R):
    """
    Находит 2 касательные (по одной от A и B), которые не пересекаются.
    Возвращает (T_A, T_B) - точки касания для A и B соответственно
    """
    
    # Функция для нахождения двух точек касания из точки P к окружности
    def get_tangent_points_from_point(P):
        dx = P[0] - O[0]
        dy = P[1] - O[1]
        d = math.hypot(dx, dy)
        
        if d < R - 1e-10:
            return []
        
        angle_to_point = math.atan2(dy, dx)
        beta = math.acos(R / d)
        
        angle1 = angle_to_point + beta
        angle2 = angle_to_point - beta
        
        T1 = (O[0] + R * math.cos(angle1), O[1] + R * math.sin(angle1))
        T2 = (O[0] + R * math.cos(angle2), O[1] + R * math.sin(angle2))
        
        return [(T1, angle1), (T2, angle2)]  # возвращаем точки и их углы
    
    # Получаем касательные с углами
    tangents_A = get_tangent_points_from_point(A)
    tangents_B = get_tangent_points_from_point(B)
    
    if len(tangents_A) != 2 or len(tangents_B) != 2:
        print("Ошибка: Некоторые точки находятся внутри окружности")
        return None
    
    # Функция для проверки, пересекаются ли отрезки A-T и B-S
    def segments_intersect(A, T, B, S):
        """Проверяет, пересекаются ли отрезки A-T и B-S"""
        def cross(o, a, b):
            return (a[0]-o[0])*(b[1]-o[1]) - (a[1]-o[1])*(b[0]-o[0])
        
        c1 = cross(A, T, B)
        c2 = cross(A, T, S)
        c3 = cross(B, S, A)
        c4 = cross(B, S, T)
        
        return (c1 * c2 < 0) and (c3 * c4 < 0)
    
    # Пробуем все 4 комбинации
    candidates = []
    
    for T_A, angle_A in tangents_A:
        for T_B, angle_B in tangents_B:
            # Проверяем, пересекаются ли отрезки
            if not segments_intersect(A, T_A, B, T_B):
                # Отрезки не пересекаются - хороший кандидат
                # Вычисляем "расстояние" для выбора (чем больше, тем лучше)
                dist_A = math.hypot(A[0] - T_A[0], A[1] - T_A[1])
                dist_B = math.hypot(B[0] - T_B[0], B[1] - T_B[1])
                
                candidates.append({
                    'T_A': T_A,
                    'T_B': T_B,
                    'angle_A': angle_A,
                    'angle_B': angle_B,
                    'dist_A': dist_A,
                    'dist_B': dist_B,
                    'total_dist': dist_A + dist_B
                })
    
    if not candidates:
        print("Не найдено непересекающихся касательных")
        return None
    
    # Выбираем кандидата с максимальной суммой расстояний
    best = max(candidates, key=lambda c: c['total_dist'])
    
    print(f"\nВыбраны непересекающиеся касательные:")
    print(f"  Углы: A={math.degrees(best['angle_A']):.1f}°, B={math.degrees(best['angle_B']):.1f}°")
    print(f"  Расстояния: |AT|={best['dist_A']:.4f}, |BT|={best['dist_B']:.4f}")
    
    return (best['T_A'], best['T_B'])


def generate_random_scenario():
    """Генерирует случайные входные параметры"""
    O = (random.uniform(-5, 5), random.uniform(-5, 5))
    R = random.uniform(1, 4)
    
    def generate_point_outside_circle():
        while True:
            x = random.uniform(-12, 12)
            y = random.uniform(-12, 12)
            dist = math.hypot(x - O[0], y - O[1])
            if dist > R + 0.5:
                return (x, y)
    
    A = generate_point_outside_circle()
    B = generate_point_outside_circle()
    
    return A, B, O, R


def visualize_solution(A, B, O, R, T_A, T_B, filename="non_intersecting_tangents.png"):
    """Визуализирует непересекающиеся касательные"""
    fig, ax = plt.subplots(figsize=(12, 10))
    
    # Рисуем окружность
    circle = Circle(O, R, fill=False, color='blue', linewidth=2, label='Окружность')
    ax.add_patch(circle)
    
    # Рисуем центр
    ax.plot(O[0], O[1], 'bo', markersize=8, label='Центр O', zorder=5)
    
    # Рисуем точки A и B
    ax.plot(A[0], A[1], 'go', markersize=10, label='Точка A', zorder=5)
    ax.plot(B[0], B[1], 'mo', markersize=10, label='Точка B', zorder=5)
    
    # Рисуем точки касания
    ax.plot(T_A[0], T_A[1], 'ro', markersize=8, label='Точки касания', zorder=5)
    ax.plot(T_B[0], T_B[1], 'ro', markersize=8, zorder=5)
    
    # Рисуем касательные (только выбранные)
    ax.plot([A[0], T_A[0]], [A[1], T_A[1]], 'g-', linewidth=3, alpha=0.9, label='Касательная A')
    ax.plot([B[0], T_B[0]], [B[1], T_B[1]], 'm-', linewidth=3, alpha=0.9, label='Касательная B')
    
    # Рисуем радиусы
    ax.plot([O[0], T_A[0]], [O[1], T_A[1]], 'r--', linewidth=1.5, alpha=0.6)
    ax.plot([O[0], T_B[0]], [O[1], T_B[1]], 'r--', linewidth=1.5, alpha=0.6)
    
    # Добавляем подписи
    ax.text(A[0], A[1], '  A', fontsize=14, fontweight='bold', 
            ha='left', va='bottom', color='green')
    ax.text(B[0], B[1], '  B', fontsize=14, fontweight='bold', 
            ha='left', va='bottom', color='magenta')
    ax.text(T_A[0], T_A[1], '  T_A', fontsize=10, ha='left', va='bottom', color='red')
    ax.text(T_B[0], T_B[1], '  T_B', fontsize=10, ha='left', va='bottom', color='red')
    ax.text(O[0], O[1], '  O', fontsize=14, fontweight='bold',
            ha='left', va='bottom', color='blue')
    
    # Настройки графика
    ax.set_aspect('equal')
    ax.grid(True, alpha=0.3)
    ax.axhline(y=0, color='k', linewidth=0.5, alpha=0.3)
    ax.axvline(x=0, color='k', linewidth=0.5, alpha=0.3)
    
    # Границы
    all_x = [A[0], B[0], O[0], T_A[0], T_B[0]]
    all_y = [A[1], B[1], O[1], T_A[1], T_B[1]]
    margin = 2
    ax.set_xlim(min(all_x) - margin, max(all_x) + margin)
    ax.set_ylim(min(all_y) - margin, max(all_y) + margin)
    
    ax.set_xlabel('X', fontsize=12)
    ax.set_ylabel('Y', fontsize=12)
    ax.set_title(f'Непересекающиеся касательные\nЦентр O=({O[0]:.2f}, {O[1]:.2f}), R={R:.2f}', 
                 fontsize=14, fontweight='bold')
    ax.legend(loc='upper left', framealpha=0.9, fontsize=11)
    
    plt.tight_layout()
    plt.savefig(filename, dpi=150, bbox_inches='tight')
    print(f"\n✓ Изображение сохранено как: {filename}")
    plt.close()
    
    return filename


def open_image(filename):
    """Открывает изображение"""
    try:
        if sys.platform == 'win32':
            os.startfile(filename)
        elif sys.platform == 'darwin':
            os.system(f'open "{filename}"')
        else:
            os.system(f'xdg-open "{filename}"')
        print(f"✓ Изображение открыто")
    except Exception as e:
        print(f"⚠ Не удалось открыть изображение: {e}")


def main():
    print("=" * 70)
    print("Поиск непересекающихся касательных к окружности")
    print("=" * 70)
    
    # Генерируем случайные параметры
    A, B, O, R = generate_random_scenario()
    
    print(f"\n📊 Параметры:")
    print(f"   A: ({A[0]:.2f}, {A[1]:.2f})")
    print(f"   B: ({B[0]:.2f}, {B[1]:.2f})")
    print(f"   O: ({O[0]:.2f}, {O[1]:.2f})")
    print(f"   R: {R:.2f}")
    
    # Находим непересекающиеся касательные
    result = find_non_intersecting_tangents(A, B, O, R)
    
    if not result:
        print("\n❌ Ошибка")
        return
    
    T_A, T_B = result
    
    print(f"\n📐 Точки касания:")
    print(f"   T_A: ({T_A[0]:.4f}, {T_A[1]:.4f})")
    print(f"   T_B: ({T_B[0]:.4f}, {T_B[1]:.4f})")
    
    # Проверка перпендикулярности
    print(f"\n✅ Проверка:")
    
    def check_perpendicular(O, T, P, name):
        vec_OT = (T[0]-O[0], T[1]-O[1])
        vec_PT = (T[0]-P[0], T[1]-P[1])
        dot = vec_OT[0]*vec_PT[0] + vec_OT[1]*vec_PT[1]
        is_perp = abs(dot) < 1e-6
        print(f"   OT ⟂ {name}: {dot:.10f} → {'✓' if is_perp else '✗'}")
        return is_perp
    
    check_perpendicular(O, T_A, A, "AT_A")
    check_perpendicular(O, T_B, B, "BT_B")
    
    # Визуализация
    print("\n🎨 Визуализация...")
    filename = "tangents.png"
    visualize_solution(A, B, O, R, T_A, T_B, filename)
    # open_image(filename)
    
    print("\n" + "=" * 70)
    print("✨ Готово!")
    print("=" * 70)


if __name__ == "__main__":
    main()