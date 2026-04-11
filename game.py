import pygame


class Game:
    """Упрощенная версия игры с встроенными callback-методами"""
    def __init__(self, width=800, height=600):
        pygame.init()
        self.screen = pygame.display.set_mode((width, height))
        self.clock = pygame.time.Clock()
        self.running = True
        self.current_scene = None
        self.scenes = {}
        
    def add_scene(self, name, scene):
        self.scenes[name] = scene
    
    def switch_scene(self, name):
        if name in self.scenes:
            self.current_scene = self.scenes[name]
            print(f"Переключено на: {name}")
    
    def exit_game(self, scene=None):
        """Встроенный метод выхода"""
        print(f"Выход из игры (сцена: {scene.name if scene else 'None'})")
        self.running = False
    
    def run(self):
        while self.running:
            # События
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.exit_game()
                
                if self.current_scene:
                    for button in self.current_scene.buttons:
                        button.handle_event(event)
            
            # Отрисовка
            if self.current_scene:
                self.current_scene.draw(self.screen)
            
            pygame.display.flip()
            self.clock.tick(60)
        
        pygame.quit()