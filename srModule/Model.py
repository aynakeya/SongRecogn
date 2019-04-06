from . import AudioDecoder,Fingerprint,Database
from .Config import srConfig
from sqlalchemy.orm import sessionmaker,session,scoped_session
import os,threading,time,random,gc

class Audio(object):
    db,db_enigne = Database.initSession()

    def __init__(self,filepath,filename,filehash):
        self.filepath = filepath
        self.filename = filename
        self.filehash = filehash
        self.fs = None
        self.channels = None
        self.fingerprints = None
        self.id = None
        self.name = None


    @classmethod
    def initFromFile(cls,filepath):
        filepath = os.path.realpath(filepath)
        filehash= AudioDecoder.generateFilehash(filepath)
        filename = os.path.splitext(os.path.split(filepath)[1])[0]
        return cls(filepath,filename,filehash)

    @classmethod
    def initFromDir(cls,dir):
        dir = os.path.realpath(dir)
        audio = []
        audiofiles = AudioDecoder.readDir(dir)
        for filepath,filename,filehash in audiofiles:
            audio.append(cls(filepath,filename,filehash))
        return audio

    def isFingerprinted(self):
        dbs = self.db()
        result = dbs.query(Database.Songs).filter_by(filehash=self.filehash).first()
        if result == None:
            return False
        return result.fingerprinted

    def read(self):
        self.fs,self.channels = AudioDecoder.read(self.filepath)

    def getFingerprints(self):
        fingerprints = set()
        for channel in self.channels:
            arr = Fingerprint.getSpecgramArr(channel, self.fs)
            peaks = Fingerprint.getConstellationMap(arr)
            del arr
            fp = Fingerprint.getFBHashGenerator(peaks)
            del peaks
            # get unioin for different channel
            fingerprints |= set(fp)

        self.fingerprints = fingerprints
        del fingerprints
        gc.collect()
        return

    def getId(self,new=False):
        dbs = self.db()
        result = dbs.query(Database.Songs).filter_by(filehash=self.filehash).first()
        if result != None:
            self.id = result.id
            self.name = result.name
            return result.id
        if new:
            song0 = Database.Songs(name=self.filename, filehash=self.filehash)
            dbs.add(song0)
            dbs.commit()
            self.id = song0.id
            self.name = self.filename
            dbs.close()
            return song0.id
        else:
            return -1

    # multi-threads
    def startInsertFingerprints(self,thread_num=srConfig.mysql_max_connection,insert_num=srConfig.mysql_insert_number):
        dbs = self.db()
        song = dbs.query(Database.Songs).filter_by(id=self.id).first()
        if song.fingerprinted:
            print("This song already be fingerprinted")
            return
        fingerprints = list(self.fingerprints)
        st = 0
        total_threads = []
        running_threads = []
        while True:
            if (st+1)*insert_num > len(fingerprints):
                total_threads.append(_insertFingerprints(st,self.db,self.id,fingerprints[st*insert_num::]))
                break
            else:
                total_threads.append(_insertFingerprints(st, self.db,self.id,fingerprints[st*insert_num:(st+1)*insert_num:]))
            st += 1
        st = 0
        while st < len(total_threads):
            if len(running_threads) < thread_num:
                total_threads[st].start()
                running_threads.append(total_threads[st])
                st += 1
                continue
            for t in running_threads:
                if not t.is_alive():
                    running_threads.remove(t)
        for t in total_threads:
            t.join()
        song.fingerprinted = True
        dbs.commit()
        dbs.close()

    # single thread
    def insertFingerprints(self):
        ss = scoped_session(self.db)
        dbs = ss()
        song = dbs.query(Database.Songs).filter_by(id=self.id).first()
        if song.fingerprinted:
            print("This song already be fingerprinted")
            return
        dbs.execute(Database.Fingerprints.__table__.insert(),
                    [{"song_id": self.id, "fingerprint": fingerprint, "offset": int(offset)} for
                     fingerprint, offset in self.fingerprints])

        song.fingerprinted = True
        dbs.commit()
        dbs.close()
        ss.remove()

    def recognize(self):
        dbs = self.db()

        matches = []
        songs = {}

        for fingerprint,offest in self.fingerprints:
            # find all the record match hash.
            result = dbs.query(Database.Fingerprints).filter_by(fingerprint=fingerprint).all()
            for r in result:
                s = dbs.query(Database.Songs).filter_by(id=r.song_id).first()
                matches.append((str(s.id),str(abs(r.offset-offest))))
                if not (str(s.id)) in songs:
                    songs[str(s.id)] = s.name

        posibility = {}
        mostpossible = {"id":"","name":"","count":0}
        largest = 0
        for song_id,offest_diff in matches:
            if not song_id in posibility:
                posibility[song_id] = dict()
            if not offest_diff in posibility[song_id]:
                posibility[song_id][offest_diff] = 0
            posibility[song_id][offest_diff] += 1
            if posibility[song_id][offest_diff] > largest:
                largest = posibility[song_id][offest_diff]
                mostpossible["id"] = song_id
                mostpossible["name"] = songs[song_id]
                mostpossible["count"] = largest

        # for key in posibility.keys():
        #     print(key,max(posibility[key].values()))
        return mostpossible

    def cleanup(self):
        del self.fingerprints
        del self.channels
        gc.collect()

class _insertFingerprints(threading.Thread):
    def __init__(self, threadID,db,song_id,data):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.db = db
        self.song_id = song_id
        self.data = data

    # using add()
    # def run(self):
    #     dbs = scoped_session(self.db)()
    #     for data in self.data:
    #         fingerprint, offset = data
    #         fingerprint0 = Database.Fingerprints(song_id=self.song_id, fingerprint=fingerprint, offset=int(offset))
    #         dbs.add(fingerprint0)
    #     dbs.commit()
    #     dbs.close()

    # using bulk_save_objects
    # def run(self):
    #     ss = scoped_session(self.db)
    #     dbs = ss()
    #     dbs.bulk_save_objects([Database.Fingerprints(song_id=self.song_id, fingerprint=fingerprint, offset=int(offset)) for fingerprint, offset in self.data])
    #     dbs.commit()
    #     dbs.close()
    #     ss.remove()

    # using bulk_insert_mappings
    # def run(self):
    #     ss = scoped_session(self.db)
    #     dbs = ss()
    #     dbs.bulk_insert_mappings(Database.Fingerprints,[{"song_id":self.song_id,"fingerprint":fingerprint, "offset":int(offset)} for fingerprint, offset in self.data])
    #     dbs.commit()
    #     dbs.close()
    #     ss.remove()

    # using core
    def run(self):
        ss = scoped_session(self.db)
        dbs = ss()
        dbs.execute(Database.Fingerprints.__table__.insert(),[{"song_id":self.song_id,"fingerprint":fingerprint, "offset":int(offset)} for fingerprint, offset in self.data])
        dbs.commit()
        dbs.close()
        ss.remove()

class _getFingerprints(threading.Thread):
    def __init__(self, threadID,audio):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.audio = audio
    def run(self):
        if self.audio.channels is None:
            self.audio.read()
        self.audio.getFingerprints()