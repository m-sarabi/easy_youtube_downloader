import math
import tkinter as tk
from tkinter import ttk
import customtkinter as ctk
from idlelib.tooltip import Hovertip


class MainWindow:
    def __init__(self, root: ctk.CTk):
        self.root = root
        self.root.title("EasyYoutubeDownloader")
        self.root.resizable(False, False)
        self.root.geometry("1280x720+20+20")

        self.menu = tk.Menu(self.root)
        self.root.config(menu=self.menu)
        # self.root.config(padx=10, pady=10)

        self.file_menu = tk.Menu(self.menu, tearoff=0)
        self.menu.add_cascade(label="File", menu=self.file_menu)
        self.file_menu.add_command(label="Exit", command=self.root.quit)

        self.help_menu = tk.Menu(self.menu, tearoff=0)
        self.menu.add_cascade(label="Help", menu=self.help_menu)
        self.help_menu.add_command(label="About", command=self.create_about_window)

        # container frame for the whole window
        self.main_frame = ctk.CTkFrame(master=self.root)
        self.main_frame.configure(fg_color="transparent")
        self.main_frame.pack(fill="both", expand=True)
        self.main_frame.grid_rowconfigure(0, weight=2)
        self.main_frame.grid_rowconfigure(1, weight=1)
        self.main_frame.grid_columnconfigure(0, weight=1)

        # for previewing the video details, thumbnail, and animated audio/video formats
        self.preview_frame = ctk.CTkFrame(master=self.main_frame)
        # preview_frame.configure(fg_color="#f0232A")
        self.preview_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=5)
        self.preview_frame.grid_rowconfigure(0, weight=3)
        self.preview_frame.grid_rowconfigure(1, weight=2)
        self.preview_frame.grid_columnconfigure(0, weight=1)

        # title of the video
        self.video_title = ctk.CTkLabel(self.preview_frame, text="Video Title", font=('Arial', 22),
                                        wraplength=600)
        self.video_title.grid(row=0, column=0, sticky='s', pady=20)

        # canvas for showing the thumbnail
        self.thumbnail_canvas = ctk.CTkCanvas(self.preview_frame, width=384, height=216)
        self.thumbnail_canvas.grid(row=1, column=0, sticky='n')

        # for inputs and buttons and so on
        self.actions_frame = ctk.CTkFrame(master=self.main_frame)
        # actions_frame.configure(fg_color="#20232A")
        self.actions_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=5)
        # actions_frame.grid_rowconfigure(0, weight=1)
        self.actions_frame.grid_columnconfigure(tuple(range(4)), weight=1)

        # url input
        self.url_input = ctk.CTkEntry(self.actions_frame, justify=ctk.CENTER, height=40, font=("Arial", 16),
                                      placeholder_text="Enter YouTube URL", state=tk.DISABLED)
        self.url_input.grid(row=0, column=1, columnspan=2, sticky='ew', pady=10)

        # This button is for getting the video formats
        self.get_info_btn = ctk.CTkButton(
            self.actions_frame,
            text="Get Video Data",
            command=self.start_animation
        )
        self.get_info_btn.grid(row=1, column=1, padx=5, pady=10, sticky='e')

        # this button is for downloading the video with the selected formats
        self.download_video_btn = ctk.CTkButton(self.actions_frame, text="Download Video", state=tk.DISABLED)
        self.download_video_btn.grid(row=1, column=2, padx=5, pady=10, sticky='w')

        # formats frame
        self.formats_frame = ctk.CTkFrame(
            master=self.main_frame,
            border_width=2,
            corner_radius=10,
            fg_color="#f02524",
            width=250, height=350,
        )
        self.formats_frame.place(x=-250, y=100)
        self.tooltip = Hovertip(self.formats_frame, 'ID: %')

        self.video_details_frame = ctk.CTkFrame(
            master=self.main_frame,
            border_width=2,
            corner_radius=10,
            fg_color="#f02524",
            width=250, height=350,
        )
        self.video_details_frame.place(x=1280, y=100)

        self._bind_events()

    # These two methods are for testing rn
    def start_animation(self):
        self.animate_move_x(self.formats_frame, 260, 1000)
        self.animate_move_x(self.video_details_frame, -260, 1000)

    def animate_move_x(self, widget, dx, duration):
        dt = int(1000 / 60)
        count = duration // dt
        step = 0
        x0 = widget.winfo_x()
        y0 = widget.winfo_y()

        def easing_function(t, mode='linear'):
            if mode == 'linear':
                return dx / duration * t
            elif mode == 'ease-out':
                return dx * math.sin(math.pi * t / (2 * duration))

        def move():
            nonlocal step
            step += 1
            if step <= count:
                pos = easing_function(step * dt, 'ease-out')
                widget.place(x=x0 + round(pos), y=y0)
                self.root.after(dt, move)
            else:
                widget.place(x=x0 + dx, y=y0)

        self.root.after(dt, move)

    def _bind_events(self):
        pass

    def create_about_window(self):
        pass


if __name__ == "__main__":
    rt = ctk.CTk()
    MainWindow(rt)
    rt.mainloop()
