import pygame

from settings import BLACK


class Scene:
    """Базовый класс для всех сцен"""
    def __init__(self, name, background_color):
        self.name = name
        self.background_color = background_color
        self.buttons = []
        self.running = True
        
    def add_button(self, button):
        self.buttons.append(button)
    
    def handle_events(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                self.running = False
                return False
            
            for button in self.buttons:
                button.handle_event(event)
        return True
    
    def draw(self, surface):
        surface.fill(self.background_color)
        
        # Рисуем заголовок сцены
        font = pygame.font.Font(None, 48)
        title_surf = font.render(self.name, True, BLACK)
        title_rect = title_surf.get_rect(center=(400, 80))
        surface.blit(title_surf, title_rect)
        
        # Рисуем все кнопки
        for button in self.buttons:
            button.draw(surface)
    
    def update(self):
        """Обновление логики сцены (можно переопределить)"""
        pass