class srConfig(object):
    audio_frame_rate = 44100
    audio_extension = ".mp3"
    sqlalchemy_address = 'mysql+mysqlconnector://root:root@localhost:3306/songrecogn'
    support_audio = [".mp3",".m4a"]
    mysql_max_connection = 128
    mysql_insert_number = 20000
    max_audio_process_num = 8
    max_process_num = 8
    enable_console_msg = True
    # if search subdirectories when using addAudioFromDir
    search_subdirectories = False
    def __init__(self):
        pass

