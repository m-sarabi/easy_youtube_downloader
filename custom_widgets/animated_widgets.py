import math
from time import time
from typing import Protocol, Any
import tkinter as tk
import customtkinter as ctk
import pathlib
from PIL import Image, ImageTk


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


class LoadingAnimation:
    def __init__(self, canvas: ctk.CTkCanvas, frames_path, duration):
        self.canvas = canvas
        self.frames_path = frames_path
        self.duration = duration
        self.current_frame = 0
        self.is_animating = False
        self.size = (100, 100)
        self.frames = self._load_frames()

    def _load_frames(self):
        frames = []
        for i in range(12):
            name = pathlib.Path(self.frames_path).joinpath(f"logo_{i + 1:02}.png")
            frame = Image.open(name)
            frame = frame.resize(self.size)
            frames.append(ImageTk.PhotoImage(frame))
        return frames

    def animate(self):
        if not self.is_animating:
            return
        self.canvas.delete('all')
        self.canvas.create_image(0, 0, image=self.frames[self.current_frame], anchor='nw')
        self.current_frame = (self.current_frame + 1) % len(self.frames)
        self.canvas.after(self.duration // 12, self.animate)

    def stop(self):
        if self.is_animating:
            self.is_animating = False
            self._reset()

    def start(self):
        if not self.is_animating:
            self.is_animating = True
            self.animate()

    def _reset(self):
        self.current_frame = 0
        self.canvas.delete('all')


if __name__ == '__main__':
    app = ctk.CTk()

    canvas = ctk.CTkCanvas()
    canvas.pack()
    animation = LoadingAnimation(canvas, "../assets/logo_frames", 600)
    animation.start()

    app.mainloop()
