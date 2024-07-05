import math
import datetime


def convert_file_size(size_bytes):
    if size_bytes == 0:
        return '0B'
    units = ('B', 'KB', 'MB', 'GB', 'TB', 'PB')
    exponent = int(math.floor(math.log(size_bytes, 1024)))
    base = math.pow(1024, exponent)
    size = round(size_bytes / base, 2)
    return f'{size} {units[exponent]}'


def convert_timestamp(timestamp):
    return datetime.datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')


def convert_duration(duration):
    seconds = int(duration)
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    seconds = seconds % 60
    return f'{hours:02}:{minutes:02}:{seconds:02}'


def approximate_filesize(tbr, duration):
    filesize = int(tbr * duration * 125)
    return convert_file_size(filesize)


if __name__ == "__main__":
    print(convert_file_size(17472059))
    print(convert_duration(311))
