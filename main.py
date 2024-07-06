import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from threading import Thread
from PIL import Image, ImageTk
import urllib.request
from utils import convert_file_size
from video import Video
import traceback
import webbrowser


class YoutubeDownloaderApp:
    def __init__(self, root):
        self.root = root
        self.root.resizable(False, False)
        self.root.title("EasyYoutubeDownloader")
        self.video_formats = {}
        self.audio_formats = {}
        self.video_id = None
        self.audio_id = None
        self.program_status = 'idle'
        self.downloaded_parts = 0

        # Create the main layout
        self.create_main_layout()

        self.root.bind('<Button-1>', self.focus_out)

    def create_main_layout(self):
        menu = tk.Menu(self.root)
        self.root.config(menu=menu)

        file_menu = tk.Menu(menu, tearoff=0)
        menu.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Exit", command=self.root.quit)

        help_menu = tk.Menu(menu, tearoff=0)
        menu.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="About", command=self.create_about_window)

        self.url_label = tk.Label(self.root, text="YouTube URL:")
        self.url_label.grid(row=0, column=0, sticky='e', padx=5, pady=5)
        self.url_entry = tk.Entry(self.root, width=45)
        self.url_entry.grid(row=0, column=1, padx=5, pady=5)
        self.check_button = tk.Button(self.root, text="Check", command=self.check_url)
        self.check_button.grid(row=0, column=2, padx=5, pady=5)

        self.video_label = tk.Label(self.root, text="Video Format:")
        self.video_label.grid(row=1, column=0, sticky='e', padx=5, pady=5)
        self.video_combo = ttk.Combobox(self.root, state='readonly', width=45)
        self.video_combo.grid(row=1, column=1, padx=5, pady=5)
        self.video_combo.bind('<<ComboboxSelected>>', self.update_video_info)

        self.audio_label = tk.Label(self.root, text="Audio Format:")
        self.audio_label.grid(row=2, column=0, sticky='e', padx=5, pady=5)
        self.audio_combo = ttk.Combobox(self.root, state='readonly', width=45)
        self.audio_combo.grid(row=2, column=1, padx=5, pady=5)
        self.audio_combo.bind('<<ComboboxSelected>>', self.update_audio_info)

        self.threads_label = tk.Label(self.root, text="Number of Threads:")
        self.threads_label.grid(row=3, column=0, sticky='e', padx=5, pady=5)
        self.threads_entry = tk.Entry(self.root, width=5)
        self.threads_entry.insert(0, '1')
        self.threads_entry.grid(row=3, column=1, padx=5, pady=5)

        self.path_label = tk.Label(self.root, text="Download Path:")
        self.path_label.grid(row=4, column=0, sticky='e', padx=5, pady=5)
        self.path_entry = tk.Entry(self.root, width=45, state='readonly')
        self.path_entry.grid(row=4, column=1, padx=5, pady=5)
        self.path_button = tk.Button(self.root, text="Browse", command=self.browse_folder)
        self.path_button.grid(row=4, column=2, padx=5, pady=5)

        self.download_label = tk.Label(self.root, text="Download:")
        self.download_label.grid(row=5, column=0, sticky='e', padx=5, pady=5)
        self.download_button = tk.Button(self.root, text="Download", command=self.download, state='disabled')
        self.download_button.grid(row=5, column=1, padx=5, pady=5)

        self.progress_bar = ttk.Progressbar(self.root, orient='horizontal', length=300, mode='determinate')
        self.progress_bar.grid(row=5, column=2, padx=5, pady=5)
        self.status_label = tk.Label(self.root, text="")
        self.status_label.grid(row=6, column=2, padx=5, pady=5)

        self.video_details_frame = ttk.LabelFrame(self.root, text="Video details")
        self.video_details_frame.grid(row=7, column=0, columnspan=2, padx=5, pady=5, sticky="ew")
        self.video_details_frame.grid_columnconfigure(1, weight=1)

        self.resolution_label = tk.Label(self.video_details_frame, text="Resolution:")
        self.resolution_label.grid(row=0, column=0, sticky='e', padx=5, pady=2)
        self.resolution_value = tk.Label(self.video_details_frame, text="")
        self.resolution_value.grid(row=0, column=1, sticky='w', padx=5, pady=2)

        self.framerate_label = tk.Label(self.video_details_frame, text="Frame Rate:")
        self.framerate_label.grid(row=1, column=0, sticky='e', padx=5, pady=2)
        self.framerate_value = tk.Label(self.video_details_frame, text="")
        self.framerate_value.grid(row=1, column=1, sticky='w', padx=5, pady=2)

        self.vsize_label = tk.Label(self.video_details_frame, text="Size:")
        self.vsize_label.grid(row=2, column=0, sticky='e', padx=5, pady=2)
        self.vsize_value = tk.Label(self.video_details_frame, text="")
        self.vsize_value.grid(row=2, column=1, sticky='w', padx=5, pady=2)

        self.vbitrate_label = tk.Label(self.video_details_frame, text="Bitrate:")
        self.vbitrate_label.grid(row=3, column=0, sticky='e', padx=5, pady=2)
        self.vbitrate_value = tk.Label(self.video_details_frame, text="")
        self.vbitrate_value.grid(row=3, column=1, sticky='w', padx=5, pady=2)

        self.vcodec_label = tk.Label(self.video_details_frame, text="Codec:")
        self.vcodec_label.grid(row=4, column=0, sticky='e', padx=5, pady=2)
        self.vcodec_value = tk.Label(self.video_details_frame, text="")
        self.vcodec_value.grid(row=4, column=1, sticky='w', padx=5, pady=2)

        self.audio_details_frame = ttk.LabelFrame(self.root, text="Audio details")
        self.audio_details_frame.grid(row=7, column=2, columnspan=2, padx=5, pady=5, sticky="ew")
        self.audio_details_frame.grid_columnconfigure(1, weight=1)

        self.asize_label = tk.Label(self.audio_details_frame, text="Size:")
        self.asize_label.grid(row=0, column=0, sticky='e', padx=5, pady=2)
        self.asize_value = tk.Label(self.audio_details_frame, text="")
        self.asize_value.grid(row=0, column=1, sticky='w', padx=5, pady=2)

        self.abitrate_label = tk.Label(self.audio_details_frame, text="Bitrate:")
        self.abitrate_label.grid(row=1, column=0, sticky='e', padx=5, pady=2)
        self.abitrate_value = tk.Label(self.audio_details_frame, text="")
        self.abitrate_value.grid(row=1, column=1, sticky='w', padx=5, pady=2)

        self.acodec_label = tk.Label(self.audio_details_frame, text="Codec:")
        self.acodec_label.grid(row=2, column=0, sticky='e', padx=5, pady=2)
        self.acodec_value = tk.Label(self.audio_details_frame, text="")
        self.acodec_value.grid(row=2, column=1, sticky='w', padx=5, pady=2)

        self.video_info_frame = ttk.LabelFrame(self.root, text="Video Information")
        self.video_info_frame.grid(row=8, column=0, columnspan=4, padx=5, pady=5, sticky="ew")
        self.video_info_frame.grid_columnconfigure(1, weight=1)

        self.title_label = tk.Label(self.video_info_frame, text="Title:")
        self.title_label.grid(row=0, column=0, sticky='e', padx=5, pady=2)
        self.title_value = tk.Label(self.video_info_frame, text="", wraplength=300)
        self.title_value.grid(row=0, column=1, sticky='w', padx=5, pady=2)

        self.duration_label = tk.Label(self.video_info_frame, text="Duration:")
        self.duration_label.grid(row=1, column=0, sticky='e', padx=5, pady=2)
        self.duration_value = tk.Label(self.video_info_frame, text="")
        self.duration_value.grid(row=1, column=1, sticky='w', padx=5, pady=2)

        self.release_label = tk.Label(self.video_info_frame, text="Release Time:")
        self.release_label.grid(row=2, column=0, sticky='e', padx=5, pady=2)
        self.release_value = tk.Label(self.video_info_frame, text="")
        self.release_value.grid(row=2, column=1, sticky='w', padx=5, pady=2)

        self.thumbnail_label = tk.Label(self.video_info_frame, text="Thumbnail:")
        self.thumbnail_label.grid(row=3, column=0, sticky='e', padx=5, pady=2)
        self.thumbnail_canvas = tk.Canvas(self.video_info_frame, width=320, height=180)
        self.thumbnail_canvas.grid(row=3, column=1, sticky='w', padx=5, pady=2)

    def browse_folder(self):
        folder_selected = filedialog.askdirectory()
        if folder_selected:
            self.path_entry.config(state='normal')
            self.path_entry.delete(0, tk.END)
            self.path_entry.insert(0, folder_selected)
            self.path_entry.config(state='readonly')

    def create_about_window(self):
        about_window = tk.Toplevel(self.root)
        about_window.title("About")
        about_window.geometry("300x400")
        about_window.resizable(False, False)
        # focus on the window
        about_window.attributes("-topmost", True)
        about_title_label = tk.Label(about_window, text="EasyYoutubeDownloader", font=("Arial", 16))
        about_title_label.pack(padx=5, pady=10)
        about_text = """
YouTube Downloader lets you easily download YouTube videos. It helps you choose and download audio and video formats, showing you a preview with the title, duration, upload date, and thumbnail.
Features:
- Download audio and video combined.
- Choose different video and audio formats.
- Preview video details before downloading.
Platforms:
- Currently for PC
Developer:
Made by Mohammad Sarabi.
GitHub: https://github.com/m-sarabi
Telegram: @MSarabi
Version:
- Version 1.0 (first release, may have bugs)
For updates, check the GitHub page.
        """.strip()
        about_desc_label = tk.Label(about_window, text=about_text, justify='left', wraplength=250, padx=5, pady=5)
        about_desc_label.pack()

        def github_command():
            webbrowser.open("https://github.com/m-sarabi/easy_youtube_downloader")
            about_window.destroy()

        github_button = tk.Button(about_window, text="GitHub", command=github_command, padx=5, pady=5)
        github_button.pack(side='left', padx=5, pady=5)

        ok_button = tk.Button(about_window, text="Close", command=about_window.destroy, padx=5, pady=5)
        ok_button.pack(side='right', padx=5, pady=5)
        about_window.focus_force()

    def check_url(self):
        self.check_button.config(state='disabled')

        def check_url_thread():
            try:
                video = Video(url)
                fetched_info(video)
            except Exception as e:
                self.check_button.config(state='normal')
                messagebox.showerror("Error", f"An error occurred: {e}")
                print(traceback.format_exc())

        def fetched_info(video):
            self.video_formats = video.get_video_formats()
            self.audio_formats = video.get_audio_formats()

            self.video_combo['values'] = [
                f"{fmt['Resolution']} | {convert_file_size(fmt['FPS'])} FPS | {fmt['VCodec']} | {fmt['Size']}" for fmt
                in self.video_formats]
            self.audio_combo['values'] = [
                f"{fmt['TBR']} TBR | {fmt['ACodec']} | {fmt['Size']}" for fmt
                in self.audio_formats]

            self.video_combo.current(0)
            self.audio_combo.current(0)

            self.update_video_info()
            self.update_audio_info()
            self.display_video_information(video)

            self.check_button.config(state='normal')
            self.download_button.config(state='normal')

        url = self.url_entry.get()
        if not url:
            self.check_button.config(state='normal')
            messagebox.showerror("Error", "Please enter a valid YouTube URL")
            return

        thread = Thread(target=check_url_thread)
        thread.start()

    def update_video_info(self, event=None):
        selected_index = self.video_combo.current()
        if selected_index >= 0:
            selected_format = self.video_formats[selected_index]
            self.resolution_value.config(text=selected_format['Resolution'])
            self.framerate_value.config(text=selected_format['FPS'])
            self.vsize_value.config(text=selected_format['Size'])
            self.vbitrate_value.config(text=selected_format['TBR'])
            self.vcodec_value.config(text=selected_format['VCodec'])
            self.video_id = selected_format['ID']

    def update_audio_info(self, event=None):
        selected_index = self.audio_combo.current()
        if selected_index >= 0:
            selected_format = self.audio_formats[selected_index]
            self.asize_value.config(text=selected_format['Size'])
            self.abitrate_value.config(text=selected_format['TBR'])
            self.acodec_value.config(text=selected_format['ACodec'])
            self.audio_id = selected_format['ID']

    def display_video_information(self, video):
        video_information = video.video_details()
        self.title_value.config(text=video_information['title'])
        self.duration_value.config(text=video_information['duration'])
        self.release_value.config(text=video_information['timestamp'])

        thumbnail_url = video_information['thumbnail']
        image = Image.open(urllib.request.urlretrieve(thumbnail_url)[0])
        image = image.resize((320, 180))
        photo = ImageTk.PhotoImage(image)
        self.thumbnail_canvas.create_image(0, 0, anchor=tk.NW, image=photo)
        self.thumbnail_canvas.image = photo

    def download(self):
        def progress_hook(d):
            if d['status'] == 'finished':
                self.progress_bar['value'] = 100
                self.check_button.config(state='normal')
                self.download_button.config(state='normal')
                self.status_label.config(text="100%")
            elif d['status'] == 'downloading':
                total_bytes = d['total_bytes'] if d.get('total_bytes') \
                    else d['total_bytes_estimate'] \
                    if d.get('total_bytes_estimate') else None
                downloaded_bytes = d['downloaded_bytes'] if d.get('downloaded_bytes') else None
                percentage = round(downloaded_bytes / total_bytes * 100) if total_bytes else 0
                percentage_str = f"{percentage}%" if percentage else None
                speed = convert_file_size(d['speed']) + "/s" if d.get('speed') else None
                stats = " | ".join([str(_) for _ in [speed, percentage_str] if _])
                self.status_label.config(text=stats)

                self.progress_bar['value'] = percentage
            elif d['status'] == 'error':
                self.check_button.config(state='normal')
                self.download_button.config(state='normal')
                self.status_label.config(text="Error")
                messagebox.showerror("Error", "An error occurred!")

        url = self.url_entry.get()
        path = self.path_entry.get()
        threads = self.threads_entry.get()
        video_format = self.video_id
        audio_format = self.audio_id

        if not all([url, path, threads, video_format, audio_format]):
            messagebox.showerror("Error", "Please fill all the fields")
            return

        try:
            threads = int(threads)
            if threads < 1:
                messagebox.showerror("Error", "Threads must be greater than 0")
                return
        except ValueError:
            messagebox.showerror("Error", "Threads must be a number")
            return

        self.download_button.config(state='disabled')
        self.check_button.config(state='disabled')

        def download_thread():
            video = Video(url)
            video.threads = threads
            video.download(video_format, audio_format, path, progress_hook)
            self.download_complete()

        Thread(target=download_thread).start()

    def download_complete(self):
        self.download_button.config(state='normal')
        self.check_button.config(state='normal')
        messagebox.showinfo("Download Complete", "The video has been downloaded successfully")

    def focus_out(self, event):
        widget = event.widget
        # if clicked on the root or on any frame widget
        if widget.winfo_class() in ['Tk', 'Label', 'TLabelframe', 'TProgressbar', 'Canvas']:
            self.root.focus_set()


if __name__ == "__main__":
    root = tk.Tk()
    app = YoutubeDownloaderApp(root)
    root.mainloop()
