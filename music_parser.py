from ID3 import *
from os import listdir
from os.path import isfile, join

import re


album_music = list()
mypath = "./input/"

onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]


## Getting all files from folder
for filename in onlyfiles:
    album_music.append(filename)


try:
    id3info = ID3(filename)
    print id3info


    

