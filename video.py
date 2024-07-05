import random
import string
from yt_dlp import YoutubeDL
from utils import *


def generate_random_string(length):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(length))


class Video:
    def __init__(self, url):
        self.url = url
        self.ydl = YoutubeDL()
        self.status = None
        self.info_dict = self.extract_info()
        self.threads = 4

    # make sure that approximate file sizes are included
    def extract_info(self):
        try:
            info = self.ydl.extract_info(self.url, download=False)
            self.status = "Success"
            return info
        except Exception as e:
            if "Read timed out" in str(e):
                self.status = "Error: timed out"
            elif "Video unavailable" in str(e):
                self.status = "Error: video unavailable"
            elif "Failed to resolve" in str(e):
                self.status = "Error: failed to resolve"
            elif "is not a valid URL" in str(e):
                self.status = "Error: invalid url"
                print(self.status)
            else:
                self.status = "Error"
            raise e

    def get_formats(self):
        return self.info_dict.get('formats', [])

    def video_details(self):
        details = {
            'title': self.info_dict.get('title'),
            'duration': convert_duration(self.info_dict.get('duration')),
            'timestamp': convert_timestamp(int(self.info_dict.get('timestamp'))),
            'thumbnail': self.info_dict.get('thumbnail'),
            'id': self.info_dict.get('id'),
        }
        return details

    def get_audio_formats(self):
        raw_formats = [f for f in self.get_formats()
                       if f.get('acodec') not in ['none', None] and f.get('vcodec') in ['none', None]]

        formats = []
        for f in raw_formats:
            formats.append({
                'ID': f.get('format_id'),
                'Size': convert_file_size(f.get('filesize')),
                'TBR': f.get('tbr'),
                'ACodec': f.get('acodec'),
            })
        return formats

    def get_video_formats(self):
        raw_formats = [f for f in self.get_formats() if
                       f.get('acodec') in ['none', None] and f.get('vcodec') not in ['none', None]]

        formats = []
        for f in raw_formats:
            formats.append({
                'ID': f.get('format_id'),
                'TBR': f.get('tbr'),
                'Resolution': f.get('resolution'),
                'FPS': f.get('fps'),
                'VCodec': f.get('vcodec'),
                'Size': (convert_file_size(f.get('filesize'))
                         if f.get('filesize')
                         else f"≈ {approximate_filesize(f.get('tbr'), self.info_dict.get('duration'))}"),
            })
        return formats

    # download video with given video and audio ids
    def download(self, video_id, audio_id, path='./', progress_hook=None):
        ydl_opts = {
            'format': f'{audio_id}+{video_id}',
            'outtmpl': path + '/' + f'%(title)s [%(id)s] - {generate_random_string(4)}.%(ext)s',
            'concurrent_fragment_downloads': self.threads,
            'progress_hooks': [progress_hook],
        }

        with YoutubeDL(ydl_opts) as ydl:
            ydl.download([self.url])
