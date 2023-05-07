import os
import glob
from mutagen.easyid3 import EasyID3
from mutagen.id3 import ID3
from mutagen.mp3 import MP3
from io import BytesIO
from PIL import Image

class MusicMetadata():
    # Ham lay sieu du lieu dang chuoi theo key
    def getMetadata(song, key):
        audio = MP3("music/" + song, ID3=EasyID3)
        result =  str(audio[key])
        return result[2:len(result)-2]
    
    # Ham lay sieu du lieu APIC va tra ve link dan den anh lay tu sieu du lieu do
    def getCover(song):        
        tags = ID3("music/" + song)
        pict = tags.get("APIC:").data
        im = Image.open(BytesIO(pict))
        return "image/" + MusicMetadata.getMetadata(song, "title") + ".jpg"
    
    # Ham tao cover cho tat ca bai hat trong playlist
    def makeCover(playlist):
        for song in playlist:
            tags = ID3("music/" + song)
            pict = tags.get("APIC:").data
            im = Image.open(BytesIO(pict))
            im.save("image/" + MusicMetadata.getMetadata(song, "title") + ".jpg")

    # Ham xoa tat ca cover
    def deleteAllCover():
        image_dir = glob.glob("image/*.jpg")
        for f in image_dir:
            os.remove(f)
