import pygame

class Entity:
    def __init__(self,type,rect):
        self.rect=rect
        self.type=type

        self.img=pygame.image.load(f'app//resources//{self.type}.png')
    
    def draw(self,screen):
        screen.blit(self.img,[self.rect.x,self.rect.y])
