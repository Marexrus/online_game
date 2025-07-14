import globals as gl
import game.ui as ui

class Timer:
    def __init__(self,t0,t1,func=None,screen=None,type=None):
        self.t0=t0
        self.t1=t1
        self.func=func
        self.screen=screen

        self.type=type

        self.active=True

        gl.timers.append(self)

    def start_timer(self,time):
        if not self.active:
            return False
        if self.screen:
            if self.type == 0:
                ui.label(self.screen, "Pause", [20, 20])
            if self.type == 1:
                ui.label(self.screen, "Round", [20, 20])
            ui.label(self.screen,str(round((self.t0+self.t1)-gl.time,1)),[220,20])

        if time >= self.t0+self.t1:
            if self.func:
                self.func()
            self.active = False
            gl.timers.remove(self)
            return False  # Таймер завершен

        return True