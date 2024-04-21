import os
from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.core.window import Window
from python.MusicScreen import MusicScreen
from python.MusicMetadata import MusicMetadata
from python.PlaylistScreen import PlaylistScreen
from kivy.uix.screenmanager import ScreenManager

os.environ['KIVY_AUDIO'] = 'ffpyplayer'
Builder.load_file('kv/main.kv')
Window.size = (360, 600)

class HorizonApp(MDApp):
    # Khoi tao app, them 2 man hinh chinh va man hinh playlist
    def build(self):
        sm = ScreenManager()
        sm.add_widget(MusicScreen())
        sm.add_widget(PlaylistScreen())
        return ScreenManager()
    
    # Tai anh cover cua tat ca bai hat tu sieu du lieu
    def on_start(self):
        music_dir = "music"
        music_files = os.listdir(music_dir)
        playlist = [x for x in music_files if x.endswith(('.mp3'))]
        MusicMetadata.makeCover(playlist)

    # Xoa tat ca cover
    def on_stop(self):
        MusicMetadata.deleteAllCover()
        