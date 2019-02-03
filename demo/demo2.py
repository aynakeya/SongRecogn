from srModule.Fingerprint import getSpecgramArr,getConstellationMap,getFBHashGenerator
from srModule import AudioDecoder


filename = "song/liangyu.mp3"

hs,fs,channels = AudioDecoder.read(filename)

for channel in channels:
    arr = getSpecgramArr(channel,fs)
    temp = getConstellationMap(arr,plot=True)

    fp = getFBHashGenerator(temp)
    print(len(set(fp)))
    break