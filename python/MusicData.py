import os

class MusicData():
    flag = False
    playlist = []
    song_count = 0
    current_song_pos = 0
    current_song = ""

    def __init__(self, **kwargs):
        # Lay danh sach bai hat tu thu muc music
        music_dir = "music"
        music_files = os.listdir(music_dir)
        playlist = [x for x in music_files if x.endswith(('.mp3'))]

        # So bai hat co trong playlist
        self.song_count = len(playlist)

        # Tai bai hat dau tien cua playlist len current
        self.current_song = self.playlist[self.current_song_pos]
