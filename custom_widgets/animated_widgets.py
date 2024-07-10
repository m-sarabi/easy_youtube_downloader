import math
from time import time
from typing import Protocol, Any
import customtkinter as ctk


class PlaceableWidget(Protocol):
    def winfo_x(self) -> int: ...

    def winfo_y(self) -> int: ...

    def place(self, *args, **kwargs) -> Any: ...

    def after(self, *args, **kwargs) -> Any: ...


class AnimatedWidget(PlaceableWidget):
    def __init__(self, duration, dx, dy, easing='linear'):
        self.duration = duration
        self.dx = dx
        self.dy = dy
        self.easing = easing
        self.is_animating = False

    def animate(self):
        if self.is_animating:
            return
        start_time = time() * 1000

        x0 = self.winfo_x()
        y0 = self.winfo_y()

        def easing_function(t, mode='linear'):
            if mode == 'linear':
                return (self.dx / self.duration * t,
                        self.dy / self.duration * t)
            elif mode == 'ease-out':
                return (self.dx * math.sin(math.pi * t / (2 * self.duration)),
                        self.dy * math.sin(math.pi * t / (2 * self.duration)))

        def move():
            self.is_animating = True
            t = time() * 1000 - start_time
            if t < self.duration:
                pos = easing_function(t, self.easing)
                self.place(x=x0 + pos[0], y=y0 + pos[1])
                self.after(16, move)
            else:
                self.place(x=x0 + self.dx, y=y0 + self.dy)
                self.is_animating = False

        move()


class ACTkFrame(ctk.CTkFrame, AnimatedWidget):
    def __init__(self, *args, duration, dx, dy, easing='linear', **kwargs):
        ctk.CTkFrame.__init__(self, *args, **kwargs)
        AnimatedWidget.__init__(self, duration, dx, dy, easing)


class ACTkLabel(ctk.CTkLabel, AnimatedWidget):
    def __init__(self, *args, duration, dx, dy, easing='linear', **kwargs):
        ctk.CTkLabel.__init__(self, *args, **kwargs)
        AnimatedWidget.__init__(self, duration, dx, dy, easing)
