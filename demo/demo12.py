from srModule.Model import Audio
from multiprocessing import Pool
import time,threading
def wrapper(songs,index):
    songs[index].getFingerprints()
class _getFingerprints(threading.Thread):
    def __init__(self, threadID,audio):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.audio = audio
    def run(self):
        self.audio.getFingerprints()

if __name__ == '__main__':
    #p = Pool()

    songs = Audio.initFromDir("song")
    print("init songs ")

    total_threads = []
    running_threads = []
    st = 0
    for song in songs:
        total_threads.append(_getFingerprints(st,song))
        st +=1

    st = 0
    print("get")
    a = time.time()
    while st < len(total_threads):
        if len(running_threads) < 6:
            total_threads[st].start()
            running_threads.append(total_threads[st])
            st += 1
            continue
        for t in running_threads:
            if not t.is_alive():
                running_threads.remove(t)
    for t in total_threads:
        t.join()

    print(time.time()-a)

    print("get done")
    for song in songs:
        song.getId()
        a = time.time()
        song.startInsertFingerprints()
        print("inert use",time.time() - a)

    # p = Pool()
    # for song in songs:
    #     print(song.id,"len fp",len(song.fingerprints))
    #     p.apply_async(song.startinsertFingerprints)
    #
    # print("insert")
    # p.close()
    # p.join()
    # print("insertdone")