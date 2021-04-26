import os
import piexif
import shutil
import time

from settings import *


def get_date(photo):
    """
    The function checks for exif data in the file.
    If they do not exist, then sorts by known data
    :param photo: pass the name of photo
    :return: tuple(int(year), int(month))
    """
    try:
        date = piexif.load(photo, key_is_name='Exif')['0th']['DateTime']
    except KeyError:
        date = time.gmtime(os.path.getmtime(os.path.normpath(DIRECTORY + f'/{photo}')))
        year = date.tm_year
        month = date.tm_mon
        return year, month
    return int(date[0:4]), int(date[5:7])


def start_sort(file_name):
    """
    The function moves files to folders by date exif from a photo
    :param file_name: pass the filename in the folder with all files
    :return: None
    """
    if file_name.endswith('.jpg'):
        if get_date(file_name):
            year = str(get_date(file_name)[0])
            month = MONTHS[str(get_date(file_name)[1])]
            photo_path = os.path.normpath(DIRECTORY + f'/{file_name}')
            under_path = os.path.normpath(DIRECTORY + f'/{year}/{month}')
            if not os.path.exists(year):
                os.mkdir(year, mode=0o777, dir_fd=None)
            os.chdir(os.path.normpath(DIRECTORY + f'/{year}'))
            if not os.path.exists(month):
                os.mkdir(month, mode=0o777, dir_fd=None)
            os.chdir(os.path.normpath(DIRECTORY + f'/{year}/{month}'))
            shutil.copy(photo_path, under_path, follow_symlinks=True)
            os.chdir(DIRECTORY)
            os.remove(photo_path)
    elif file_name.endswith('.mp4'):
        if not os.path.exists('Video'):
            os.mkdir('Video', mode=0o777, dir_fd=None)
        video_path = os.path.normpath(DIRECTORY + f'/Video')
        file_path = os.path.normpath(DIRECTORY + f'/{file_name}')
        os.chdir(video_path)
        shutil.copy(file_path, video_path, follow_symlinks=True)
        os.chdir(DIRECTORY)
        os.remove(file_path)


def start(directory):
    """
    The function runs through the files in the folder
    :param directory: name of directory with photos
    :return: None
    """
    os.chdir(directory)
    for file in os.listdir(directory):
        start_sort(file)
