from pydub import AudioSegment
import numpy as np

filename = "song/liangyu.mp3"

audiofile = AudioSegment.from_file(filename) # type:pydub.audio_segment.AudioSegment
print(audiofile.channels)
print(audiofile.converter)
print(audiofile.DEFAULT_CODECS)
print(audiofile.frame_rate)
print(audiofile.frame_width)
#print(audiofile.raw_data)
d1 = audiofile.get_array_of_samples()

print(len(d1))
print("a",d1[10000000])
data = np.fromstring(audiofile.raw_data, np.int16)
print("b",data[10000000])

a = [2,4,5]
b = [2,4,5]
print(a==b)