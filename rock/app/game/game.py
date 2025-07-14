import pygame
import game.ui as ui
import sys
import globals as gl
import game.timer as tm
import network.client as cl

import datetime

class Game():
    def __init__(self):

        pygame.init()
        pygame.mixer.init()

        self.screen = pygame.display.set_mode((500, 600))
        self.clock = pygame.time.Clock()
        self.FPS = 144
        self.running = True

        self.sprites={}

        self.load_image()

    def connection(self):
        self.client = cl.Client()
        self.client.start()

    def register(self,addr):
        name='admin'
        self.client.send(f'register/{addr}/{name}')

    def join_room(self,addr, room):
        self.client.send(f'join/{addr}/{room}')

    def end_round(self):
        gl.game_state = 'wait_server'
        choice = gl.player_choice
        self.client.send(f'round/{self.client.addr}/{choice}')

    def wait_round(self):
        gl.game_state = 'start_round'

    def main(self):
        self.click_x, self.click_y=[-100,-100]

        self.button_rock=ui.Button(100,500,100,100,'Камень',[100,100,0],[100,100,0],lambda: setattr(gl, 'player_choice', 'rock'))
        self.button_scissors = ui.Button(300, 500, 100, 100, 'Ножницы', [100, 100, 0], [100, 100, 0],lambda: setattr(gl, 'player_choice', 'scissors'))
        self.button_paper=ui.Button(200,500,100,100,'Бумага',[100,100,0],[100,100,0],lambda: setattr(gl, 'player_choice', 'paper'))

        self.connection()
        self.register(self.client.addr)
        self.join_room(self.client.addr, 'test_room')

        while self.running:
            pygame.display.set_caption(f'{gl.game_state}------{len(gl.timers)}')
            dt = self.clock.tick(self.FPS) / 1000.0
            gl.time+=dt

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.click_x, self.click_y = event.pos
                self.button_rock.check_click([self.click_x, self.click_y], event)
                self.button_paper.check_click([self.click_x, self.click_y], event)
                self.button_scissors.check_click([self.click_x, self.click_y], event)

            keys = pygame.key.get_pressed()

            self.screen.fill((120,120,120))
            self.button_rock.draw(self.screen)
            self.button_paper.draw(self.screen)
            self.button_scissors.draw(self.screen)

            #if gl.winner_name:
                #ui.label(self.screen,f'{gl.winner_name}',[200,100])

            if gl.game_state == 'start_round':
                gl.game_state = 'round'
                gl.timers.clear()
                tm.Timer(gl.time, 4, self.end_round, screen=self.screen, type=1)
            elif gl.game_state == 'start_pause':
                gl.game_state = 'pause'
                gl.timers.clear()
                tm.Timer(gl.time, 2, self.wait_round, screen=self.screen, type=0)
            elif gl.game_state == 'pause':
                if gl.winner_choice != "None":
                    self.screen.blit(self.sprites[gl.winner_choice], [200, 150])
                    if gl.winner_addr == self.client.addr:
                        ui.label(self.screen, 'Ты победил', [200,100], size=32)
                    else:
                        ui.label(self.screen, 'Ты проиграл', [200, 100], size=32)
                else:
                    ui.label(self.screen, 'Ничья', [200, 100], size=32)

            for timer in gl.timers:
                #ui.label(self.screen, f'{gl.time}', [20, 20])
                timer.start_timer(gl.time)

            self.screen.blit(self.sprites[gl.player_choice],[200,350])

            pygame.display.update()
        pygame.quit()

    def load_image(self):
        image_rock = pygame.image.load('resources//rock.png').convert_alpha()
        image_paper = pygame.image.load('resources//paper.png').convert_alpha()
        image_scissors = pygame.image.load('resources//scissors.png').convert_alpha()

        self.sprites = {'rock': image_rock, 'paper': image_paper, 'scissors': image_scissors}