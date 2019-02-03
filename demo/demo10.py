from srModule.Model import Audio
import time
songs = Audio.initFromDir("song")
#song0 = song.initFromFile("/Users/luyijou/Desktop/ Mine/Python/SongRecogn/song/nicengshishaonian.mp3")
for song in songs:
    id = song.getId()
    if id != -1:
        continue
    song.getId(new=True)
    print("len fp",len(song.getFingerprint()))
    print("insert")
    song.startinsertFingerprints()
    print("down")
