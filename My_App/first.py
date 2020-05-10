from PIL import Image
import requests
from PyQt5 import QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox
from My_App.Ui import Ui_MainWindow
import getpass
from pytube import YouTube
from pytube import exceptions
import pytube
from urllib import parse
from urllib import error
import urllib
import os
import subprocess
from random import randint


class UserInteraction(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(UserInteraction, self).__init__(parent)
        self.setupUi(self)  # here we setup ui file

        self.progressBar.setMaximum(100)
        self.progressBar.setMinimum(0)
        self.progressBar.setValue(0)

        self.flag = None
        self.selected_stream = None
        self.thumbnail_path = None
        self.no_thumbnail_path = None
        self.get_url = None
        self.url = None
        self.length = None
        self.stream_list = None
        self.title = None
        self.thumbnail = None
        self.username = None
        self.video_stream = None
        self.audio_stream = None
        self.size = None
        self.audio_size = None
        self.video_size = None
        self.audio_video_list = []
        self.video_list = []
        self.audio_list = []
        self.msg = QMessageBox()

        self.download_button.setEnabled(False)  # download button kept disabled initially
        self.add_button.setEnabled(False)  # add button kept disabled initially
        self.add_button.clicked.connect(self.add)
        self.process_button.clicked.connect(self.enter_url)
        self.download_button.clicked.connect(self.download)

    def progress_fun(self, chunk, file_handle, bytes_remaining):
        percent = int((100*(self.selected_stream.filesize-bytes_remaining))/self.size)  # here we receive the percentage of bytes we get/downloaded
        self.progressBar.setValue(percent)

    def clear_info(self):
        self.title_label.clear()
        self.file_size_label_2.clear()
        self.file_size_label.clear()
        self.comboBox.clear()
        self.thumbnail_label.clear()
        self.flag = None
        self.selected_stream = None
        self.thumbnail_path = None
        self.no_thumbnail_path = None
        self.get_url = None
        self.url = None
        self.length = None
        self.stream_list = None
        self.title = None
        self.thumbnail = None
        self.username = None
        self.video_stream = None
        self.audio_stream = None
        self.audio_video_list = []
        self.video_list = []
        self.audio_list = []
        self.progressBar.setValue(0)
        self.size = None
        self.audio_size = None
        self.video_size = None

    def enter_url(self):
        try:
            self.clear_info()
            self.delete_audio_video()  # deleted audio video files
            try:
                self.get_url = self.lineEdit.text().strip()
                self.url = YouTube(self.get_url)
                self.url.register_on_progress_callback(self.progress_fun)

            except pytube.exceptions.VideoUnavailable:
                self.clear_info()
                self.msg.setWindowTitle('Video unavailable')
                self.msg.setText('This video is unavailable')
                self.msg.setIcon(QMessageBox.Warning)
                self.msg.exec_()

            except urllib.error.URLError:
                self.clear_info()
                self.msg.setWindowTitle('Network problem')
                self.msg.setText('Please check your Internet connection')
                self.msg.setIcon(QMessageBox.Warning)
                self.msg.exec_()
            except KeyError:
                self.clear_info()
                self.msg.setWindowTitle('Error')
                self.msg.setText('Please try another video')
                self.msg.setIcon(QMessageBox.Warning)
                self.msg.exec_()
            except Exception as e:
                self.clear_info()
                print(e)
                self.msg.setWindowTitle('Error')
                self.msg.setText('Wrong Url')
                self.msg.setIcon(QMessageBox.Warning)
                self.msg.exec_()

            self.title = self.url.title  # get title
        except Exception as e:
            print(e)
        try:
            self.set_info()
        except Exception as e:
            print(e)

    def set_info(self):
        try:
            self.download_thumbnail(self.url.thumbnail_url)
        except KeyError:
            self.thumbnail_label.setPixmap(QtGui.QPixmap("no_thumbnail.jpg"))  # set no_thumbnail
        except Exception as e:
            print(e)
            self.thumbnail_label.setPixmap(QtGui.QPixmap("no_thumbnail.jpg"))   # set no_thumbnail

        try:
            self.thumbnail_label.setPixmap(QtGui.QPixmap(f'..\\temp\\{self.read_resized_thumbnail_image()}'))  # set thumbnail
            self.title_label.setText(self.title)  # set title
            self.delete_images()  # delete images

            self.length = int(self.url.length)  # get length of video
            self.file_size_label_2.setText(str(round(self.url.length/60, 2)) + 'min')  # set length

            self.comboBox.clear()
            self.streams()  # manage streams

            self.download_button.setEnabled(False)  # download button disabled
            self.add_button.setEnabled(True)  # enabled add button
        except Exception as e:
            print(e)

    def download_thumbnail(self, image):
        file_name, extension = os.path.splitext(os.path.basename(urllib.parse.urlsplit(image).path))
        image_name = 'image.'+extension
        r = requests.get(image).content
        with open(f'..\\temp\\{image_name}', 'wb') as f:
            f.write(r)
        self.resize_thumbnail()

    def resize_thumbnail(self):
        img_name = self.read_thumbnail_image()
        img_path = f'..\\temp\\{img_name}'
        img = Image.open(img_path)
        new_size = (280, 170)
        img = img.resize(new_size)
        new_image_name = 'new_'+img_name
        img.save(f'..\\temp\\{new_image_name}')

    @classmethod
    def read_thumbnail_image(cls):
        for _, _, file_name in os.walk('..\\temp'):
            for image_name in file_name:
                img = image_name.split('.')
                if 'image' in img:
                    return image_name

    @classmethod
    def read_resized_thumbnail_image(cls):
        for _, _, file_name in os.walk('..\\temp'):
            for image_name in file_name:
                img = image_name.split('.')
                if 'new_image' in img:
                    return image_name

    @classmethod
    def delete_images(cls):
        for _, _, file_name in os.walk('..\\temp'):
            for image_name in file_name:
                image_path = '..\\temp\\' + image_name
                os.remove(image_path)

    @classmethod
    def delete_audio_video(cls):
        for _, _, file_name in os.walk('..\\temp_a'):  # removed audio file
            for audio_file in file_name:
                audio_path = '..\\temp_a\\' + audio_file
                os.remove(audio_path)
        for _, _, file_name in os.walk('..\\temp_v'):  # removed video file
            for video_file in file_name:
                video_path = '..\\temp_v\\' + video_file
                os.remove(video_path)

    def streams(self):
        self.stream_list = self.url.streams.filter(file_extension='mp4')
        all_pixels_range = []  # All pixels
        for res in self.stream_list:
            str_res = str(res)
            for i in str_res.split(' '):
                if 'res=' in i:
                    new_split = i.split('=')
                    all_pixels_range.append(new_split[1].replace('"', ''))
        all_pixels_range = list(set(all_pixels_range))

        for res in all_pixels_range:  # put all pixels in combobox
            if res == 'None':
                continue
            self.comboBox.addItem(res)

        self.audio_video_list = []
        self.audio_list = []
        self.video_list = []

        for stream in self.stream_list:  # manage above 3 lists
            str_stream = str(stream)
            # print(str_stream)
            if 'acodec=' in str_stream and 'vcodec=' in str_stream:
                self.audio_video_list.append(stream)
            elif 'vcodec=' in str_stream:
                self.video_list.append(stream)
            elif 'acodec=' in str_stream:
                self.audio_list.append(stream)

    def add(self):
        self.delete_audio_video()  # deleted audio video files
        self.download_button.setEnabled(True)  # download button enabled
        res = self.comboBox.currentText()
        for stream in self.audio_video_list:
            split_stream = str(stream).split(' ')
            if f'res="{res}"' in split_stream:
                self.flag = 1
                self.selected_stream = stream
                self.file_size_label.setText(str(round((self.selected_stream.filesize/1024)/1024, 2)) + 'mb')
                self.size = self.selected_stream.filesize
            else:
                self.flag = 0
                self.get_audio_video(res)

    def get_audio_video(self, resolution):
        try:
            for video in self.video_list:
                split_stream = str(video).split(' ')
                if f'res="{resolution}"' in split_stream:
                    self.video_stream = video
            for audio in self.audio_list:
                s_s = str(audio).split(' ')
                if 'mime_type="audio/mp4"' in s_s:
                    self.audio_stream = audio
            audio_size = ...
            video_size = ...
            try:
                audio_size = self.audio_stream.filesize
            except error.HTTPError as err:
                if err.code == 404:
                    audio_size = self.audio_stream.filesize_approx
            try:
                video_size = self.video_stream.filesize
            except error.HTTPError as err:
                if err.code == 404:
                    video_size = self.video_stream.filesize_approx
            self.audio_size = audio_size
            self.video_size = video_size
            size = audio_size + video_size
            self.size = str(round((size / 1024) / 1024, 2)) + 'mb'
            self.file_size_label.setText(self.size)
        except Exception as e:
            print(e)

    def download(self):
        self.username = getpass.getuser()
        if self.flag == 1:
            self.selected_stream.download(f'C:\\Users\\{self.username}\\Downloads')
            self.progressBar.setValue(0)
            self.msg.setWindowTitle('Download')
            self.msg.setText('Downloaded Successfully')
            self.msg.setIcon(QMessageBox.Information)
            self.download_button.setEnabled(False)
            self.msg.exec_()
        elif self.flag == 0:
            try:
                self.selected_stream = self.video_stream
                self.size = self.video_size
                print(self.selected_stream)
                self.selected_stream.download('..\\temp_v')
                self.selected_stream = self.audio_stream
                self.size = self.audio_size
                self.selected_stream.download('..\\temp_a')
                self.msg.setWindowTitle('Download')
                self.msg.setText('Downloaded Successfully')
                self.msg.setIcon(QMessageBox.Information)
                self.download_button.setEnabled(False)
                self.msg.exec_()
                self.change_names()
            except Exception as e:
                print(e)
                self.msg.setWindowTitle('Error')
                self.msg.setText('Resolution not available\n'
                                 'please try the video with another resolution')
                self.msg.setIcon(QMessageBox.Warning)
                self.msg.exec_()

    def change_names(self):   # Changed audio video file names
        for _, _, file_names in os.walk('..\\temp_a'):  # changed audio file name
            for file_name in file_names:
                os.rename(f'..\\temp_a\\{file_name}', '..\\temp_a\\audio.mp4')

        for _, _, file_names in os.walk('..\\temp_v'):  # changed video file name
            for file_name in file_names:
                os.rename(f'..\\temp_v\\{file_name}', '..\\temp_v\\video.mp4')
        self.merge()

    def merge(self):
        video_file = '..\\temp_v\\video.mp4'
        audio_file = '..\\temp_a\\audio.mp4'
        random_number = str(randint(0, 1000000))
        output_file = f'C:\\Users\\{self.username}\\Downloads\\download{random_number}.mov'
        subprocess.run(f"ffmpeg -i {audio_file} -i {video_file} -acodec copy -vcodec copy {output_file}")
        self.delete_audio_video()


if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    win = UserInteraction()
    win.show()
    app.exec_()
