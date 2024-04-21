import os
import time
import random
from kivy.clock import Clock
from kivy.animation import Animation
from kivy.uix.screenmanager import Screen
from kivy.core.audio import SoundLoader
from kivy.properties import ObjectProperty
from kivy.properties import NumericProperty
from kivy.properties import BooleanProperty
from kivymd.uix.boxlayout import MDBoxLayout
from python.MusicMetadata import MusicMetadata
from python.MusicData import MusicData

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
    volume_status = NumericProperty(defaultvalue = 3)
    shuffle_status = BooleanProperty(defaultvalue = False)
    play_status = BooleanProperty(defaultvalue = False)
    pause_status = BooleanProperty(defaultvalue = False)
    replay_status = NumericProperty(defaultvalue = 0)

    # Lay danh sach bai hat tu thu muc music
    music_dir = "music"
    music_files = os.listdir(music_dir)
    playlist = [x for x in music_files if x.endswith(('.mp3'))]

    # So bai hat co trong playlist
    song_count = len(playlist)

    # Tai bai hat dau tien cua playlist len current
    current_song_pos = MusicData.current_song_pos
    current_song = MusicData.current_song
    sound = SoundLoader.load('{}/{}'.format(music_dir, current_song))

    # Tai bai hat tai vi tri pos trong playlist len current
    def loadAudio(self, pos):
        if MusicData.flag == True:
            self.current_song_pos = MusicData.current_song_pos
            MusicData.flag = False
        else:
            self.current_song_pos = pos
        self.current_song = self.playlist[self.current_song_pos]
        self.sound = SoundLoader.load('{}/{}'.format(self.music_dir, self.current_song))
        self.totaltime.text = time.strftime('%M:%S', time.gmtime(self.sound.length))
        self.progress.max = str(self.sound.length)
        self.progress.value = 0
        self.progress.bind(on_touch_up = self.catchProgressChange)

    # Phat bai hat hien tai
    def playAudio(self):
        if self.play_status == True: return False
        self.songname.text = MusicMetadata.getMetadata(self.current_song, "title")
        self.songartist.text = MusicMetadata.getMetadata(self.current_song, "artist")
        self.ewc.source = MusicMetadata.getCover(self.current_song)
        self.songcover.source = MusicMetadata.getCover(self.current_song)
        self.sound.play()
        self.volumeChecking()
        self.progressBarEvent = Clock.schedule_interval(self.progressBarUpdate, 1)
        self.updateTimeEvent = Clock.schedule_interval(self.timeUpdate, 1)
        self.changeSongEvent = Clock.schedule_interval(self.changeSong, 0.1)
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

    # Tam dung bai hat hien tai
    def pauseAudio(self):
        if self.play_status == True:
            self.sound.stop()
            self.progressBarEvent.cancel()
            self.updateTimeEvent.cancel()
            self.pause_status = True
            self.play_status = False

    # Tiep tuc bai hat hien tai
    def continueAudio(self):
        if self.play_status == True: return False
        self.sound.volume = 0
        self.sound.play()
        time.sleep(1.5)
        self.sound.seek(self.progress.value)
        self.volumeChecking()
        self.progressBarEvent = Clock.schedule_interval(self.progressBarUpdate, 1)
        self.updateTimeEvent = Clock.schedule_interval(self.timeUpdate, 1)
        self.pause_status = False
        self.play_status = True

    # Chon bai hat ngau nhien
    def shuffleAudio(self):
        random_pos = -1
        if self.song_count > 1:
            random_pos = random.randrange(0,self.song_count)
            while random_pos == self.current_song_pos:
                random_pos = random.randrange(0,self.song_count)
            self.loadAudio(random_pos)

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
            self.playAndPauseAudio()
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

    # Kiem tra am luong
    def volumeChecking(self):
        if self.volume_status == 3:
            self.sound.volume = 1
        elif self.volume_status == 2:
            self.sound.volume = 0.5
        elif self.volume_status == 1:
            self.sound.volume = 0.25
        else:
            self.sound.volume = 0

    # Ham bat xu li thay doi bai hat
    def changeSong(self, t):
        if MusicData.flag:
            self.stopAudio()
            self.loadAudio(0)
            self.playAudio()

#================================================BUTTON================================================
    # Nut bat tat am luong
    def volumeToggle(self):
        if self.volume_status == 0:
            self.sound.volume = 0.25
            self.volumebtn.icon = 'volume-low'
            self.volume_status = 1
        elif self.volume_status == 1:
            self.sound.volume = 0.5
            self.volumebtn.icon = 'volume-medium'
            self.volume_status = 2
        elif self.volume_status == 2:
            self.sound.volume = 1
            self.volumebtn.icon = 'volume-high'
            self.volume_status = 3
        else:
            self.sound.volume = 0
            self.volumebtn.icon = 'volume-off'
            self.volume_status = 0

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
        self.playbtn.icon = 'pause'
        self.playAudio()
        
    # Nut phat/dung bai hat hien tai
    def playAndPauseAudio(self):
        if self.play_status:
            self.pauseAudio()
            self.playbtn.icon = 'play'
        else:
            if self.pause_status:
                self.continueAudio()
            else:
                self.loadAudio(self.current_song_pos)
                self.playAudio()
            self.playbtn.icon = 'pause'

    # Nut bai hat ke tiep
    def nextAudio(self):
        self.stopAudio()
        if self.shuffle_status:
            self.shuffleAudio()
        elif (self.current_song_pos == self.song_count - 1):
            self.loadAudio(0)
        else:
            self.loadAudio(self.current_song_pos + 1)
        self.playbtn.icon = 'pause'
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
    anim = Animation(angle=-360, d=10, t='linear')
    anim += Animation(angle=0, d=0, t='linear')
    anim.repeat = True

    # Ham xoay anh bia
    def rotate(self):
        if self.anim.have_properties_to_animate(self):
            self.anim.stop(self)
        else:
            self.anim.start(self)
