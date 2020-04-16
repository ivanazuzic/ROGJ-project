#!/usr/bin/python

import os, sys

# Open a file
path_wav = "../VEPRAD/Wav/"
path_txt = "../VEPRAD/Txt/"
dirs = os.listdir(path_wav)

# Go through all the files and directories
with open('paired_files.txt', 'w') as output_file:
    for wav_file in dirs:
        #print(wav_file)
        txt_file = wav_file[:-4] + ".txt"
        if not os.path.isfile(path_txt + txt_file):
            print(txt_file, "doesn't exist")
        else:
            output_file.write("%s %s\n" % (wav_file, txt_file))