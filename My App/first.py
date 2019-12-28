import getpass
from pytube import YouTube
from pytube import exceptions
import pytube
import urllib
from urllib import error


class UserInteraction:
    def __init__(self):
        self.choice = None
        self.choose = None
        self.get_url = None
        self.url = None
        self.stream_list = None
        self.title = None
        self.thumbnail = None
        self.choose = None
        self.selected_stream = None
        self.menu_choice = None
        self.menu_list = ['Audio and Video (in one file)', 'Audio and Video(Separate files)', 'Only Audio',
                          'Only Video', 'mp4', 'webm', 'All files']

    def enter_url(self):
        try:
            self.get_url = input('Enter/Paste url here: ').strip()
            print('Fetching Data...')
            self.url = YouTube(self.get_url)
        except pytube.exceptions.VideoUnavailable:
            print('This video is unavailable.')
            self.next()
        except urllib.error.URLError:
            print('Unable to download: Please check your internet connection...')
            self.next()
        except KeyError:
            print('\nSORRY!!, there is a problem in the package(pytube)\nPlease try another video...')
            self.next()
        except Exception as e:
            print('Wrong URL (Please check the url)')
            print('Exception: ', e)
            self.next()
        print('\nTitle: ' + self.url.title)
        try:
            print('Thumbnail: ' + self.url.thumbnail_url)
        except KeyError:
            print('Thumbnail: ' + 'Not available')
        self.choose_stream()

    def menu(self):
        print('\n**** MENU (Select the download type) ****')
        for index, data in enumerate(self.menu_list, start=1):
            print(f'{index}.{data}')
        self.menu_choice = int(input('\nEnter your selection(like enter 7 for All files): '))
        if self.menu_choice == 1:
            return self.url.streams.filter(progressive=True).all()
        elif self.menu_choice == 2:
            return self.url.streams.filter(adaptive=True).all()
        elif self.menu_choice == 3:
            return self.url.streams.filter(only_audio=True).all()
        elif self.menu_choice == 4:
            return self.url.streams.filter(only_video=True).all()
        elif self.menu_choice == 5:
            return self.url.streams.filter(file_extension='mp4').all()
        elif self.menu_choice == 6:
            return self.url.streams.filter(file_extension='webm').all()
        elif self.menu_choice == 7:
            return self.url.streams.all()
        else:
            print('You entered wrong choice')
            self.choose_stream()

    def choose_stream(self):
        self.stream_list = self.menu()
        print('\nAvailable files...')
        for index, data in enumerate(self.stream_list, start=1):
            print(f'Press {index} to Download =>  {data}')
        self.choose = int(input('Enter here: ').strip())
        self.download()

    def download(self):
        self.selected_stream = self.stream_list[self.choose-1]
        print('Downloading...')
        username = getpass.getuser()  # it returns us the username of pc (as username is different for different pc's)
        self.selected_stream.download(f'C:\\Users\\{username}\\Downloads')
        print('\nDownloaded Successfully...')
        self.next()

    def next(self):
        self.choice = input('\n\nDo u want to download more(Y/N): ').strip().lower()
        if self.choice == 'y':
            self.enter_url()
        else:
            exit()


obj = UserInteraction()
obj.enter_url()
