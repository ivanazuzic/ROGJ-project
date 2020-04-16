#!/usr/bin/python

import sys

import speech_recognition as sr

no_args = len(sys.argv)
if no_args >= 2:
    BATCH_NO = int(sys.argv[1])
else:
    BATCH_NO = 1 

BATCH_SIZE = 1000
GOOGLE_SPEECH_API_KEY = None

path_wav = "../VEPRAD/Wav/"
path_txt = "../VEPRAD/Txt/"
path_output = "../GoogleOutput/"

# Loads the names of paired wav files
def get_wav_list():
    names_list = []
    with open('paired_files.txt', 'r') as input_file:
        for row in input_file:
            wav_name = row.split()[0]
            names_list.append(wav_name)
    return names_list

# Selects a batch that we want to upload
def select_batch(names_list, batch_no, batch_size):
    b_start = (batch_no - 1) * batch_size
    b_end = (batch_no) * batch_size
    return names_list[b_start : b_end]

# Get the Google Speech output for a batch of data
def get_output_for_batch(batch, path_output):
    for filename in batch:
        output_filename = filename[:-4] + "GoogleOutput" + ".txt"
        get_single_file_output(path_wav, filename, path_output, output_filename)

# Send a single file to the Google Speech API and retrieve output
def get_single_file_output(path_to_wav, filename, output_path, output_filename):
    recognizer = sr.Recognizer()
    audio_file = sr.AudioFile(path_to_wav + filename)
    with audio_file as source:
        audio_data = recognizer.record(source)
        try:
            text = recognizer.recognize_google(
                audio_data, 
                key=GOOGLE_SPEECH_API_KEY, 
                language="hr-HR"
            )
            with open(output_path + output_filename, 'w') as output_file:
                output_file.write(text)
            print(filename)
            print(text)
        except sr.UnknownValueError:
            print("Google could not understand audio: UnknownValueError")
            with open(output_path + output_filename, 'w') as output_file:
                output_file.write("UnknownValueError")
        except sr.RequestError as e:
            print("Google error: RequestError; {0}".format(e))

wav_names = get_wav_list()
curr_batch = select_batch(wav_names, BATCH_NO, BATCH_SIZE)
get_output_for_batch(curr_batch, path_output)

