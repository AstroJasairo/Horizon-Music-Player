import os
import kivy
import time
import random
from kivy.clock import Clock
from kivy.lang import Builder
from kivy.animation import Animation
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.core.window import Window
from kivy.core.audio import SoundLoader
from kivy.properties import ObjectProperty
from kivy.properties import NumericProperty
from kivy.properties import BooleanProperty
from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.card.card import MDCard
from python.MusicMetadata import MusicMetadata

Builder.load_file('kv/main.kv')
Window.size = (360, 600)

class MusicScreen(Screen):
    # Cac module kivy
    ewc = ObjectProperty(None)
    sc = ObjectProperty(None)
    songcover = ObjectProperty(None)
    songname = ObjectProperty(None)
    songartist = ObjectProperty(None)
    currenttime = ObjectProperty(None)
    totaltime = ObjectProperty(None)
    progress = ObjectProperty(None)
    volumebtn = ObjectProperty(None)
    shufflebtn = ObjectProperty(None)
    playbtn = ObjectProperty(None)
    replaybtn = ObjectProperty(None)
    playlistspace = ObjectProperty(None)
   
    # Cac bien luu giu trang thai cua he thong
    volume_status = BooleanProperty(defaultvalue = True)
    shuffle_status = BooleanProperty(defaultvalue = False)
    play_status = BooleanProperty(defaultvalue = False)
    replay_status = NumericProperty(defaultvalue = 0)

    # Lay danh sach bai hat tu thu muc music
    music_dir = "music"
    music_files = os.listdir(music_dir)
    playlist = [x for x in music_files if x.endswith(('.mp3'))]

    # So bai hat co trong playlist
    song_count = len(playlist)

    # Tai bai hat dau tien cua playlist len current
    current_song_pos = 0
    current_song = playlist[current_song_pos]
    sound = SoundLoader.load('{}/{}'.format(music_dir, current_song))

    # Tai bai hat tai vi tri pos trong playlist len current
    def loadAudio(self, pos):
        self.current_song_pos = pos
        self.current_song = self.playlist[self.current_song_pos]
        self.sound = SoundLoader.load('{}/{}'.format(self.music_dir, self.current_song))
        self.totaltime.text = time.strftime('%M:%S', time.gmtime(self.sound.length))
        self.progress.max = str(self.sound.length)
        self.progress.bind(on_touch_up = self.catchProgressChange)

    # Phat bai hat hien tai
    def playAudio(self):
        self.loadAudio(self.current_song_pos)
        if self.play_status == True: return False
        if self.volume_status:
            self.sound.volume = 1
        else:
            self.sound.volume = 0
        self.songname.text = MusicMetadata.getMetadata(self.current_song, "title")
        self.songartist.text = MusicMetadata.getMetadata(self.current_song, "artist")
        self.ewc.source = MusicMetadata.getCover(self.current_song)
        self.songcover.source = MusicMetadata.getCover(self.current_song)
        self.sound.play()
        self.progressBarEvent = Clock.schedule_interval(self.progressBarUpdate, 1)
        self.updateTimeEvent = Clock.schedule_interval(self.timeUpdate, 1)
        self.play_status = True

    # Dung bai hat hien tai
    def stopAudio(self):
        if self.play_status == True:
            self.sound.stop()
            self.progressBarEvent.cancel()
            self.updateTimeEvent.cancel()
            self.currenttime.text = "00:00"
            self.progress.value = 0
            self.play_status = False

    # Chon bai hat ngau nhien
    def shuffleAudio(self):
        self.loadAudio(random.randrange(0,self.song_count))

    # Xu li thanh progress bar chay theo thoi gian bai hat
    def progressBarUpdate(self, value):
        if self.progress.value < self.progress.max-1:
            self.progress.value += 1
        else:
            self.replayAudio()            

    # Xu li bo dem thoi gian chay theo thoi gian bai hat
    def timeUpdate(self, t):
        self.currenttime.text = time.strftime('%M:%S', time.gmtime(self.progress.value))

    # Xu li lap lai bai hat
    def replayAudio(self):
        if self.replay_status == 0:
            self.playAndStopAudio()
            self.sc.rotate()
        elif self.replay_status == 1:
            self.stopAudio()
            self.playAudio()
        else:
            self.nextAudio()

    # Ham thay phat bai hat tai vi tri hien tai cua progress bar
    def catchProgressChange(self, slider, touch):
        if self.progress.collide_point(*touch.pos):
            self.sound.seek(self.progress.value)

#================================================BUTTON================================================
    # Nut bat tat am luong
    def volumeToggle(self):
        if self.volume_status:
            self.sound.volume = 0
            self.volumebtn.icon = 'volume-off'
            self.volume_status = False
        else:
            self.sound.volume = 1
            self.volumebtn.icon = 'volume-high'
            self.volume_status = True

    # Nut bat tat chon bai hat ngau nhien
    def shuffleToggle(self):
        if self.shuffle_status:
            self.shufflebtn.icon = 'shuffle-disabled'
            self.shuffle_status = False
        else:
            self.shufflebtn.icon = 'shuffle-variant'
            self.shuffle_status = True

    # Nut bai hat truoc
    def previousAudio(self):
        self.stopAudio()
        if self.shuffle_status:
            self.shuffleAudio()
        elif (self.current_song_pos == 0):
            self.loadAudio(self.song_count - 1)
        else:
            self.loadAudio(self.current_song_pos - 1)
        self.playbtn.icon = 'stop'
        self.playAudio()
        
    # Nut phat/dung bai hat hien tai
    def playAndStopAudio(self):
        if self.play_status:
            self.stopAudio()
            self.playbtn.icon = 'play'
        else:
            self.playAudio()
            self.playbtn.icon = 'stop'

    # Nut bai hat ke tiep
    def nextAudio(self):
        self.stopAudio()
        if self.shuffle_status:
            self.shuffleAudio()
        elif (self.current_song_pos == self.song_count - 1):
            self.loadAudio(0)
        else:
            self.loadAudio(self.current_song_pos + 1)
        self.playbtn.icon = 'stop'
        self.playAudio()

    # Nut thay doi trang thai phat lai bai hat
    def replayToggle(self):
        if self.replay_status == 0:
            self.replaybtn.icon = 'repeat-once'
            self.replay_status = 1
        elif self.replay_status == 1:
            self.replaybtn.icon = 'repeat'
            self.replay_status = 2
        else:
            self.replaybtn.icon = 'repeat-off'
            self.replay_status = 0
#======================================================================================================

class SongCover(MDBoxLayout):
    angle = NumericProperty()
    anim = Animation(angle=-360, d=3, t='linear')
    anim += Animation(angle=0, d=0, t='linear')
    anim.repeat = True

    # Ham xoay anh bia
    def rotate(self):
        if self.anim.have_properties_to_animate(self):
            self.anim.stop(self)
        else:
            self.anim.start(self)

class PlaylistScreen(Screen):
    load_status = BooleanProperty(defaultvalue = False)

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
        self.cardbtn.bind(on_press = lambda x:self.playThis(pos))
    
    # Thay doi bai hat hien tai
    def playThis(self, pos):
        MusicScreen.current_song_pos = pos

class WindowManager(ScreenManager):
    pass

class HorizonApp(MDApp):
    def build(self):
        return WindowManager()
    
    def on_start(self):
        music_dir = "music"
        music_files = os.listdir(music_dir)
        playlist = [x for x in music_files if x.endswith(('.mp3'))]
        MusicMetadata.makeCover(playlist)

    def on_stop(self):
        MusicMetadata.deleteAllCover()
