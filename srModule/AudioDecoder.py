from pydub import AudioSegment
from hashlib import sha256
from .Config import srConfig
from . import Console
import numpy as np
import os, subprocess


def generateFilehash(filepath, blocksize=2 ** 16):
    sha = sha256()
    with open(filepath, "rb") as f:
        while True:
            buf = f.read(blocksize)
            if not buf:
                break
            sha.update(buf)
    return sha.hexdigest().upper()


def encodeAudio(filepath, dir="temp"):
    dir = os.path.realpath(dir)
    Console.log("Encode Audio with ffmpeg......", end="")
    if not os.path.exists(dir):
        os.makedirs(dir)
    path = os.path.join(dir, "temp" + generateFilehash(filepath)[:6:] + srConfig.audio_extension)
    os.system(" ".join(["ffmpeg", "-loglevel", "quiet", "-i", "\"%s\"" % filepath, "-y", "-acodec", "mp3", "-ar",
                        str(srConfig.audio_frame_rate), "\"%s\"" % path]))
    return read(path)


def read(filepath):
    try:
        filename, exten = os.path.splitext(filepath)
        audiofile = AudioSegment.from_file(filepath)

        # set all audio file frame rate with a default value and same extensions
        if audiofile.frame_rate != srConfig.audio_frame_rate or exten != srConfig.audio_extension:
            return encodeAudio(filepath)
        # data = audiofile.get_array_of_samples()
        # Stereo audio array is in form of [sample_1_L, sample_1_R, sample_2_L, sample_2_R, …]
        data = np.fromstring(audiofile.raw_data, np.int16)
        channels = []
        # Get data for different channel
        for channel in range(audiofile.channels):
            channels.append(data[channel::audiofile.channels])
    except:
        return 0, 0

    # filename, exten = os.path.splitext(filepath)
    # audiofile = AudioSegment.from_file(filepath)
    #
    # # set all audio file frame rate with a default value and same extensions
    # if audiofile.frame_rate != srConfig.audio_frame_rate or exten != srConfig.audio_extension:
    #     return encodeAudio(filepath)
    # # data = audiofile.get_array_of_samples()
    # # Stereo audio array is in form of [sample_1_L, sample_1_R, sample_2_L, sample_2_R, …]
    # data = np.fromstring(audiofile.raw_data, np.int16)
    # channels = []
    # # Get data for different channel
    # for channel in range(audiofile.channels):
    #     channels.append(data[channel::audiofile.channels])

    return audiofile.frame_rate, channels


def readDir(filesdir):
    for root, dirs, files in os.walk(filesdir):
        for file in files:
            filename, exten = os.path.splitext(os.path.split(file)[1])
            if exten in srConfig.support_audio:
                try:
                    fh = generateFilehash(os.path.join(root, file))
                except:
                    continue
                yield (os.path.join(root, file), filename, fh)
        if not srConfig.search_subdirectories:
            break
