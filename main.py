import PySimpleGUI as sg
import threading
import urllib.request
from PIL import Image, ImageTk
from utils import convert_file_size

from video import Video
from layout import Layout


def create_about_window():
    wnd = sg.Window('About', layouts.about_window_layout, modal=True, finalize=True)
    wnd.bind('<Escape>', '-ESCAPE-')
    return wnd


def fetch_video_info(url):
    video = Video(url)
    if video.status != 'Success':
        # show an error popup
        main_window.write_event_value('-FORMATS-', (None, video.status, None))
        return
    vfs = video.get_video_formats()
    vfs = {name: value for name, value in zip(video_format_to_str(vfs), vfs)}
    afs = video.get_audio_formats()
    afs = {name: value for name, value in zip(audio_format_to_str(afs), afs)}
    main_window.write_event_value('-FORMATS-', (vfs, afs, video.video_details()))


def video_format_to_str(vfs):
    # resolution | FPS | VCodec | Size
    return [f"{f['Resolution']} | {f['FPS']} FPS | {f['VCodec']} | {f['Size']}" for f in vfs]


def audio_format_to_str(afs):
    # TBR | ACodec | Size
    return [f"{f['TBR']} TBR | {f['ACodec']} | {f['Size']}" for f in afs]


def update_info_boxes(mode):
    if mode == 'video':
        video_dic = {'-RESOLUTION-': 'Resolution', '-FRAMERATE-': 'FPS', '-VCODEC-': 'VCodec', '-VBITRATE-': 'TBR',
                     '-VSIZE-': 'Size'}
        for key, value in video_dic.items():
            main_window[key].update(value=video_formats[values['-VIDEO-']][value])
        return video_formats[values['-VIDEO-']]['ID']
    elif mode == 'audio':
        audio_dic = {'-ABITRATE-': 'TBR', '-ACODEC-': 'ACodec', '-ASIZE-': 'Size'}
        for key, value in audio_dic.items():
            main_window[key].update(value=audio_formats[values['-AUDIO-']][value])
        return audio_formats[values['-AUDIO-']]['ID']


def download_video(video_id, audio_id, path, progress_hook, threads):
    video = Video(url)
    video.threads = threads
    try:
        video.download(video_id, audio_id, path, progress_hook)
    except Exception as e:
        main_window.write_event_value('-DOWNLOAD-', f"Download Failed: {e}")


def progress_hook(d):
    if d['status'] == 'finished':
        main_window['-PROGRESS-'].update(current_count=100)
        main_window.write_event_value('-DOWNLOAD-', 'Success')
        main_window['Check'].update(disabled=False)
        main_window['Download'].update(disabled=False)
        main_window['-STATUS-'].update(value="Done!")
    elif d['status'] == 'downloading':
        total_bytes = d['total_bytes'] if d.get('total_bytes') \
            else d['total_bytes_estimate'] \
            if d.get('total_bytes_estimate') else None
        downloaded_bytes = d['downloaded_bytes'] if d.get('downloaded_bytes') else None
        percentage = round(downloaded_bytes / total_bytes * 100) if total_bytes else None
        percentage_str = f"{percentage}%" if percentage else None
        speed = convert_file_size(d['speed']) + "/s" if d.get('speed') else None
        main_window['-PROGRESS-'].update(current_count=percentage)
        stats = " | ".join([str(_) for _ in [speed, percentage_str] if _])
        main_window['-STATUS-'].update(value=stats)
    elif d['status'] == 'error':
        main_window['-PROGRESS-'].update(current_count=0)
        main_window.write_event_value('-DOWNLOAD-', "Download Failed!")
        main_window['-STATUS-'].update(value="Error!")


layouts = Layout()

video_formats = {}
audio_formats = {}
video_id = audio_id = None
program_status = 'idle'
downloaded_parts = 0

# Create the window
main_window = sg.Window('EasyYoutubeDownloader', layouts.main_window_layout, finalize=True)

# Create the 'about' window
about_window = None

# Event loop
while True:
    window, event, values = sg.read_all_windows()
    if window == main_window:
        if event in [sg.WINDOW_CLOSED, '-ESCAPE-', 'Exit']:
            break
        elif event == 'Check':
            url = values['-URL-']
            if url:
                threading.Thread(target=fetch_video_info, args=(url,), daemon=True).start()
        # get the selected video and audio format on change
        elif event == '-VIDEO-' or event == '-AUDIO-':
            if event == '-VIDEO-':
                video_id = update_info_boxes('video')
            elif event == '-AUDIO-':
                audio_id = update_info_boxes('audio')

            if video_id and audio_id:
                main_window['Download'].update(disabled=False)
        elif event == '-FORMATS-':
            video_formats, audio_formats, video_details = values['-FORMATS-']
            if video_formats is None:
                sg.popup_error(f'\n{audio_formats}\n')
                continue
            if video_formats and audio_formats:
                window['-VIDEO-'].update(values=list(video_formats.keys()), disabled=False, )
                window['-AUDIO-'].update(values=list(audio_formats.keys()), disabled=False, )

                window['-TITLE-'].update(value=video_details['title'])
                window['-DURATION-'].update(value=video_details['duration'])
                window['-RELEASE-'].update(value=video_details['timestamp'])
                img = Image.open(urllib.request.urlretrieve(video_details['thumbnail'])[0])
                img.thumbnail((300, 200))
                window['-THUMBNAIL-'].update(data=ImageTk.PhotoImage(img))
            else:
                sg.popup_error("Failed to fetch formats")
        elif event == 'Download':
            url = values['-URL-']
            threads = int(values['-THREADS-'])
            download_path = values['-PATH-']
            if url and video_id and audio_id and download_path and threads > 0:
                threading.Thread(target=download_video,
                                 args=(video_id, audio_id, download_path, progress_hook, threads),
                                 daemon=True).start()
                if program_status == 'idle':
                    main_window['Check'].update(disabled=True)
                    main_window['Download'].update(disabled=True)
                    program_status = 'downloading'
            else:
                sg.popup_error("Please enter valid inputs")
        elif event == '-DOWNLOAD-':
            result = values['-DOWNLOAD-']
            if result != 'Success':
                sg.popup_error(result)
                main_window['Check'].update(disabled=False)
                main_window['Download'].update(disabled=False)
                downloaded_parts = 0
            if downloaded_parts == 2:
                main_window['Check'].update(disabled=False)
                main_window['Download'].update(disabled=False)
                program_status = 'idle'
                downloaded_parts = 0
        elif event == 'About':
            if not about_window:
                about_window = create_about_window()
                about_window.bring_to_front()
                about_window.TKroot.focus_force()

    elif window == about_window:
        if event in [sg.WINDOW_CLOSED, '-ESCAPE-']:
            about_window.close()
            about_window = None

if about_window:
    about_window.close()
window.close()
