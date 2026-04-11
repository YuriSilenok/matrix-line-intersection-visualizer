# Цвета
import pygame

from settings import BLACK


class Button:
    """Кнопка, которая знает свою сцену и метод для вызова"""
    def __init__(self, x, y, width, height, text, color, hover_color, scene, callback):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.scene = scene  # ссылка на сцену, которой принадлежит кнопка
        self.callback = callback  # метод, который нужно вызвать при клике
        self.is_hovered = False
        self.font = pygame.font.Font(None, 36)
        
    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            self.is_hovered = self.rect.collidepoint(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.is_hovered:
                # Вызываем переданный метод, передавая ему сцену
                if self.callback:
                    self.callback(self.scene)
                return True
        return False
    
    def draw(self, surface):
        color = self.hover_color if self.is_hovered else self.color
        pygame.draw.rect(surface, color, self.rect)
        pygame.draw.rect(surface, BLACK, self.rect, 3)
        
        text_surf = self.font.render(self.text, True, BLACK)
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)