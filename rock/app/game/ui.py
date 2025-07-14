import pygame

def label(screen,text, pos, size=48, color=(255, 0, 255)):
    font = pygame.font.SysFont("TimesNewRoman", size)
    text_render = font.render(text, False, color)
    screen.blit(text_render, pos)


class Button:
    def __init__(self, x, y, width, height, text, color, hover_color, action=None):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.action = action
        self.font = pygame.font.Font(None, 24)
        
    def draw(self, surface):
        mouse_pos = pygame.mouse.get_pos()
        current_color = self.hover_color if self.rect.collidepoint(mouse_pos) else self.color
        
        pygame.draw.rect(surface, current_color, self.rect, border_radius=5)
        pygame.draw.rect(surface, (0, 0, 0), self.rect, 2, border_radius=5)
        
        text_surf = self.font.render(self.text, True, (0, 0, 0))
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)
        
    def check_click(self, pos, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(pos):
                if self.action:
                    self.action()