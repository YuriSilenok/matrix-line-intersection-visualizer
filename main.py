from src.ui.scene import Scene
from settings import BLACK, RED, WHITE
from ui.button import Button


def exit_button_callback(scene):
    """Callback для кнопки выхода - закрывает текущую сцену"""
    print(f"Кнопка 'Выход' нажата на сцене '{scene.name}'")
    scene.running = False


scene = Scene('еуые', BLACK)
exit_btn = Button(300, 400, 200, 50, "Выйти", RED, WHITE, scene, exit_button_callback)