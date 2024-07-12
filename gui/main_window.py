import tkinter as tk
import customtkinter as ctk
from idlelib.tooltip import Hovertip
from custom_widgets import ACTkFrame, ACTkLabel, LoadingAnimation


class MainWindow:
    def __init__(self, root: ctk.CTk):
        self.root = root
        self.root.title("EasyYoutubeDownloader")
        self.root.resizable(False, False)
        self.root.geometry("1280x720+20+20")

        # select theme
        ctk.set_appearance_mode("dark")

        self.is_panel_open = False
        self.panels_animating = False

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

        # get the background color of the preview frame
        self.bg_color = self.preview_frame.cget("fg_color")[1]

        # canvas for showing the thumbnail
        self.thumbnail_canvas = ctk.CTkCanvas(self.preview_frame, width=384, height=216)
        self.thumbnail_canvas.grid(row=1, column=0, sticky='n')
        self.thumbnail_canvas.configure(bg=self.bg_color, highlightthickness=0)
        self.loading = LoadingAnimation(self.thumbnail_canvas, '../assets/logo_frames', 600)

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
            command=self.test_animate
        )
        self.get_info_btn.grid(row=1, column=1, padx=5, pady=10, sticky='e')

        # this button is for downloading the video with the selected formats
        self.download_video_btn = ctk.CTkButton(self.actions_frame, text="Download Video", state=tk.DISABLED)
        self.download_video_btn.grid(row=1, column=2, padx=5, pady=10, sticky='w')

        # formats frame
        self.formats_frame = ACTkFrame(
            master=self.main_frame,
            border_width=2,
            corner_radius=10,
            fg_color="#f02524",
            width=250, height=350,
            duration=800, dx=260, dy=0, easing='ease-out'
        )
        self.formats_frame.place(x=-250, y=100)
        self.tooltip = Hovertip(self.formats_frame, 'ID: %')

        self.video_details_frame = ACTkFrame(
            master=self.main_frame,
            border_width=2,
            corner_radius=10,
            fg_color="#f02524",
            width=250, height=350,
            duration=800, dx=-260, dy=0, easing='ease-out'
        )
        self.video_details_frame.place(x=1280, y=100)

        self._bind_events()

    def _bind_events(self):
        pass

    def create_about_window(self):
        pass

    def test_animate(self):
        pass


if __name__ == "__main__":
    rt = ctk.CTk()
    MainWindow(rt)
    rt.mainloop()
