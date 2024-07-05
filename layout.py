import PySimpleGUI as sg


class Layout:
    def __init__(self):
        pass

    @property
    def main_window_layout(self):
        return [
            [
                sg.Menu([["File", ["Exit"]],
                         ["Help", ["About"]]]),
                sg.Column([
                    [
                        sg.Text('YouTube URL:', size=(15, 1)),
                        sg.InputText(key='-URL-', size=(40, 1)),
                        sg.Button('Check')
                    ],
                    [
                        sg.Text('Video Format:', size=(15, 1)),
                        sg.Combo([], key='-VIDEO-', size=(40, 1), disabled=True, enable_events=True, readonly=True)
                    ],
                    [
                        sg.Text('Audio Format:', size=(15, 1)),
                        sg.Combo([], key='-AUDIO-', size=(40, 1), disabled=True, enable_events=True, readonly=True)
                    ],
                    [
                        sg.Text('Number of Threads:', size=(15, 1)),
                        sg.InputText('1', key='-THREADS-', size=(5, 1))
                    ],
                    [
                        sg.Text('Download Path:', size=(15, 1)),
                        sg.InputText(key='-PATH-', size=(40, 1), readonly=True),
                        sg.FolderBrowse()
                    ],
                    [
                        sg.Button('Download', disabled=True),
                        sg.ProgressBar(100, orientation='h', size=(25, 15), key='-PROGRESS-', pad=((62, 0), (0, 0))),
                        sg.Text('', key='-STATUS-')
                    ],
                    [sg.HorizontalSeparator()],
                    [
                        sg.Column([
                            [sg.Text('Video details:', font=('Helvetica', 12, 'bold'))],
                            [
                                sg.Text('Resolution:', size=(15, 1)),
                                sg.Text('', size=(15, 1), key='-RESOLUTION-')
                            ],
                            [
                                sg.Text('Frame Rate:', size=(15, 1)),
                                sg.Text('', size=(15, 1), key='-FRAMERATE-')
                            ],
                            [
                                sg.Text('Size:', size=(15, 1)),
                                sg.Text('', size=(15, 1), key='-VSIZE-')
                            ],
                            [
                                sg.Text('Bitrate:', size=(15, 1)),
                                sg.Text('', size=(15, 1), key='-VBITRATE-')
                            ],
                            [
                                sg.Text('Codec:', size=(15, 1)),
                                sg.Text('', size=(15, 1), key='-VCODEC-')
                            ]
                        ], vertical_alignment='top')
                        ,
                        sg.VerticalSeparator(),
                        sg.Column([
                            [sg.Text('Audio details:', font=('Helvetica', 12, 'bold'))],
                            [
                                sg.Text('Size:', size=(15, 1)),
                                sg.Text('', size=(15, 1), key='-ASIZE-')
                            ],
                            [
                                sg.Text('Bitrate:', size=(15, 1)),
                                sg.Text('', size=(15, 1), key='-ABITRATE-')
                            ],
                            [
                                sg.Text('Codec:', size=(15, 1)),
                                sg.Text('', size=(15, 1), key='-ACODEC-')
                            ]
                        ], vertical_alignment='top')
                    ]
                ], vertical_alignment='top'),
                sg.VerticalSeparator(),
                sg.Column([
                    [sg.Text('Video Information:', font=('Helvetica', 14, 'bold'))],
                    [sg.Text('Title:'), sg.Text('', size=(30, 1), key='-TITLE-')],
                    [sg.Text('Duration:'), sg.Text('', size=(30, 1), key='-DURATION-')],
                    [sg.Text('Release Time:'), sg.Text('', size=(30, 1), key='-RELEASE-')],
                    [sg.Text('Thumbnail:')],
                    [sg.Image(key='-THUMBNAIL-', size=(300, 200))]
                ], vertical_alignment='top')
            ]
        ]

    @property
    def about_window_layout(self):
        about_text = """\
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
        """

        layout = [
            [sg.Text('About YouTube Downloader', font=('Helvetica', 16, 'bold'))],
            [sg.Multiline(about_text, size=(60, 23), disabled=True, no_scrollbar=True)],
        ]

        return layout
        # return [
        #     [sg.Text('About EasyYouTubeDownloader', font=('Helvetica', 14, 'bold'))],
        #     [sg.Multiline(default_text="", key='-ABOUT1-',disabled=True)],
        # ]
