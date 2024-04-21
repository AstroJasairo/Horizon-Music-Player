import os
import shutil
import subprocess
import tkinter as tk
from tkinter import filedialog
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import Screen
from kivy.properties import BooleanProperty
from kivymd.uix.card.card import MDCard
from kivy.uix.filechooser import FileChooserListView
from kivymd.uix.gridlayout import MDGridLayout
from python.MusicMetadata import MusicMetadata
from python.MusicData import MusicData
from kivy.clock import Clock

class PlaylistScreen(Screen):
    load_status = BooleanProperty(defaultvalue = False)

    def set_selected_song(pos):
        MusicData.current_song_pos = pos
        MusicData.flag = True

    # Di chuyen file
    def move_file_to_music_folder(self, source_file, music_folder):
        if os.path.exists(source_file) and os.path.isdir(music_folder):
            shutil.move(source_file, os.path.join(music_folder, os.path.basename(source_file)))

    # Mo giao dien them nhac
    def open_file_dialog(self):
        root = tk.Tk()
        root.withdraw()

        file_path = filedialog.askopenfilename()

        music_folder = 'music'

        if file_path:
            self.move_file_to_music_folder(file_path, music_folder)


class PlaylistSpace(MDGridLayout):
    # Load playlist
    def refreshPlaylist(self):
        music_dir = "music"
        music_files = os.listdir(music_dir)
        playlist = [x for x in music_files if x.endswith(('.mp3'))]
        pos = 0
        for song in playlist:
            title = MusicMetadata.getMetadata(song, "title")
            artist = MusicMetadata.getMetadata(song, "artist")
            cover = MusicMetadata.getCover(song)
            self.add_widget(MyMusic(title, artist, cover, pos))
            pos += 1
        PlaylistScreen.load_status = True

class MyMusic(MDCard):
    # Tao moi music item
    def __init__(self, title, artist, cover, pos, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.cardimage.source = cover
        self.cardtitle.text = title
        self.cardartist.text = artist
        self.cardbtn.bind(on_press = lambda x:PlaylistScreen.set_selected_song(pos))
