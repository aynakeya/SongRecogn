from . import AudioDecoder, Fingerprint, Database, Model, Console
from .Config import srConfig
from sqlalchemy.orm import sessionmaker, session
import os, time

def parsePath(args):
    path = "".join(args)
    if path[0] == "\"" and path[-1] == "\"":
        path = path[1:-1:]
    return os.path.realpath(path)

def recognize(args):
    filepath = parsePath(args)
    if os.path.exists(filepath):
        Console.recognizeAudio(filepath)
    else:
        Console.log("File not exists: %s" % filepath)


def add_audio(args):
    filepath = parsePath(args)
    print(filepath)
    if os.path.exists(filepath):
        Console.addAudio(filepath)
    else:
        Console.log("File not exists: %s" % filepath)


def add_dir(args):
    dirpath = parsePath(args)
    if os.path.exists(dirpath):
        Console.addAudioFromDir(dirpath)
    else:
        Console.log("File not exists: %s" % dirpath)
