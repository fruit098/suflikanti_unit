import eyed3
from os import listdir
from os.path import isfile, join, realpath

## Getting all files from folder
def create_album_record(path_to_mp3):
    album_music = list()

    final_output = list()
    mypath = path_to_mp3

    onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]

    for filename in onlyfiles:
        album_music.append(filename)

    for mp3_file in album_music:
        mp3 = eyed3.load(mypath + mp3_file)

        duration = mp3.info.time_secs
        song_path = realpath(mypath + mp3_file)

        final_output.append({"songname" : mp3_file, "duration" : duration, "path" : song_path})

    return final_output



print(create_album_record("./music/"))