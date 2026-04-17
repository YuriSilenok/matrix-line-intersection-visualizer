import math
import random
import matplotlib.pyplot as plt
from matplotlib.patches import Circle


def get_tangent_points(P, O, R) -> tuple:
    dx = P[0] - O[0]
    dy = P[1] - O[1]
    d = math.hypot(dx, dy)
    
    if d < R:
        return []
    
    if abs(d - R) < 1e-10:
        return [(P[0], P[1]), (P[0], P[1])]
    
    ang = math.atan2(dy, dx)
    beta = math.acos(R / d)
    a1 = ang + beta
    a2 = ang - beta
    
    T1 = (O[0] + R * math.cos(a1), O[1] + R * math.sin(a1))
    T2 = (O[0] + R * math.cos(a2), O[1] + R * math.sin(a2))
    
    return T1, T2


def segments_intersect(seg1, seg2):
    """
    Проверяет, пересекаются ли два отрезка.
    
    Параметры:
    seg1, seg2 - кортежи из двух точек ((x1,y1), (x2,y2))
    
    Возвращает:
    True - если отрезки пересекаются (включая концы)
    False - если не пересекаются
    """
    (A, B) = seg1
    (C, D) = seg2
    
    def cross(o, a, b):
        return (a[0]-o[0])*(b[1]-o[1]) - (a[1]-o[1])*(b[0]-o[0])
    
    # Проверка на вырожденные отрезки (точки)
    if A == B or C == D:
        return False
    
    # Вычисляем ориентации
    c1 = cross(A, B, C)
    c2 = cross(A, B, D)
    c3 = cross(C, D, A)
    c4 = cross(C, D, B)
    
    # Общий случай: отрезки пересекаются
    if (c1 * c2 < 0) and (c3 * c4 < 0):
        return True
    
    # Проверка особых случаев (когда точка лежит на отрезке)
    def on_segment(p, q, r):
        """Проверяет, лежит ли точка q на отрезке pr"""
        return (min(p[0], r[0]) <= q[0] <= max(p[0], r[0]) and
                min(p[1], r[1]) <= q[1] <= max(p[1], r[1]))
    
    # Точка C лежит на отрезке AB
    if c1 == 0 and on_segment(A, C, B):
        return True
    # Точка D лежит на отрезке AB
    if c2 == 0 and on_segment(A, D, B):
        return True
    # Точка A лежит на отрезке CD
    if c3 == 0 and on_segment(C, A, D):
        return True
    # Точка B лежит на отрезке CD
    if c4 == 0 and on_segment(C, B, D):
        return True
    
    return False


def distance(p1, p2):
    return math.hypot(p2[0] - p1[0], p2[1] - p1[1])


def find_best_tangents(A, B, O, R):

    # Точки касания
    AT1, AT2 = get_tangent_points(A, O, R)
    BT1, BT2 = get_tangent_points(B, O, R)

    ATBT = None
    if segments_intersect((AT1, AT2), (BT1, BT2)):
        if segments_intersect((A, AT1), (B, BT1)):
            ATBT = AT2, BT2
        elif segments_intersect((A, AT1), (B, BT2)):
            ATBT = AT2, BT1
        elif segments_intersect((A, AT2), (B, BT1)):
            ATBT = AT1, BT2
        else:
            ATBT = AT1, BT1
    else:
        if distance(AT1, BT1) < distance(AT1, BT2):
            if distance(AT1, BT1) > distance(AT2, BT2):
                ATBT = AT1, BT1
            else:
                ATBT = AT2, BT2
        else:
            if distance(AT1, BT2) > distance(AT2, BT1):
                ATBT = AT1, BT2
            else:
                ATBT = AT2, BT1
    return ATBT

def generate_random_scenario():
    O = (random.randint(-5, 5), random.randint(-5, 5))
    R = random.randint(1, 4)
    def outside():
        while True:
            x = random.randint(-12, 12)
            y = random.randint(-12, 12)
            if math.hypot(x - O[0], y - O[1]) > R + 0.5:
                return (x, y)
    return outside(), outside(), O, R

def visualize(A, B, O, R, TA, TB, filename="tangents.png"):
    fig, ax = plt.subplots(figsize=(8, 8))
    circle = Circle(O, R, fill=False, color='blue', lw=2)
    ax.add_patch(circle)
    ax.plot(*O, 'bo', markersize=6)
    ax.plot(*A, 'go', markersize=8)
    ax.plot(*B, 'mo', markersize=8)
    ax.plot(*TA, 'ro', markersize=6)
    ax.plot(*TB, 'ro', markersize=6)
    ax.plot([A[0], TA[0]], [A[1], TA[1]], 'g-', lw=2)
    ax.plot([B[0], TB[0]], [B[1], TB[1]], 'm-', lw=2)
    ax.plot([O[0], TA[0]], [O[1], TA[1]], 'r--', lw=1, alpha=0.5)
    ax.plot([O[0], TB[0]], [O[1], TB[1]], 'r--', lw=1, alpha=0.5)
    ax.set_aspect('equal')
    ax.grid(True, alpha=0.3)
    plt.savefig(filename, dpi=150, bbox_inches='tight')
    plt.close()

def main():
    A, B, O, R = generate_random_scenario()
    # A, B, O, R = (-10, -8), (-4, 12), (-4, 1), 3
    print(A, B, O, R)
    res = find_best_tangents(A, B, O, R)
    if res:
        visualize(A, B, O, R, res[0], res[1])

if __name__ == "__main__":
    main()