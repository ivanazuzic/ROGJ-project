#!/usr/bin/python

import sys
import speech_recognition as sr
import jiwer
from google.cloud import speech_v1
from google.cloud.speech_v1 import enums
import io
import os

no_args = len(sys.argv)
if no_args >= 2:
    BATCH_NO = int(sys.argv[1])
else:
    BATCH_NO = 1 

BATCH_SIZE = 2328
GOOGLE_SPEECH_API_KEY = None

path_wav = "../VEPRAD/Wav/"
path_txt = "../VEPRAD/Txt/"
path_output = "../GoogleOutput/"
path_output_2 = "../GoogleOutput2/"

# Loads the names of paired wav files
def get_wav_list():
    names_list = []
    with open('paired_files.txt', 'r') as input_file:
        for row in input_file:
            wav_name = row.split()[0]
            names_list.append(wav_name)
    return names_list

#dodala
#Load the names of paired txt files
def get_txt_list():
    names_list = []
    with open('paired_files.txt', 'r') as input_file:
        for row in input_file:
            txt_name = row.split()[1]
            names_list.append(txt_name)
    return names_list
# Selects a batch that we want to work with
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
            with open(output_path + output_filename, 'wb') as output_file:#stavila b jer u pythonu3 treba biti
                output_file.write(text.encode('utf-8'))
            print(filename)
            print(text)
        except sr.UnknownValueError:
            print("Google could not understand audio: UnknownValueError")
            with open(output_path + output_filename, 'w') as output_file:
                output_file.write("UnknownValueError")
        except sr.RequestError as e:
            print("Google error: RequestError; {0}".format(e))
            
#Clean the data:
def clean(content):
    sentence=jiwer.RemoveKaldiNonWords()(content)
    sentence=sentence.replace("^","ć");
    sentence=jiwer.SubstituteRegexes({r"{": r"š",r"`":r"ž",r"}":r"đ",r"~":r"č",r"#":r"dž"})(sentence)
    sentence=jiwer.RemoveMultipleSpaces()(sentence)
    return sentence

#To get rid of unnecessary symbols and replace some of them
def get_paired_text_corrected(batch):
    sentences=list()
    for filename in batch:
        with open(path_txt+filename,"r") as f:
               content = f.read()
               sentence = clean(content)
               sentences.append(sentence)
    #sentences=jiwer.SubstituteRegexes({r"{": r"š",r"`":r"ž",r"}":r"đ",r"~":r"č",r"#":r"dž"})(sentences)
    return sentences

def sample_recognize(local_file_path, destination, sample_rate_hertz = 16000):
    """
    Transcribe a short audio file using synchronous speech recognition

    Args:
      local_file_path Path to local audio file, e.g. /path/audio.wav
    """

    client = speech_v1.SpeechClient()

    # The language of the supplied audio
    language_code = "hr-HR"

    # Sample rate in Hertz of the audio data sent
    #sample_rate_hertz = 16000

    # Encoding of audio data sent. This sample sets this explicitly.
    # This field is optional for FLAC and WAV audio formats.
    encoding = enums.RecognitionConfig.AudioEncoding.LINEAR16
    config = {
        "language_code": language_code,
        "sample_rate_hertz": sample_rate_hertz,
        "encoding": encoding,
    }
    with io.open(local_file_path, "rb") as f:
        content = f.read()
    audio = {"content": content}

    response = client.recognize(config, audio)
    for result in response.results:
        # First alternative is the most probable result
        alternative = result.alternatives[0]
        print(u"Transcript: {}".format(alternative.transcript))
        with open(destination, "w") as out_file:
            out_file.write(alternative.transcript)

def get_multiple_outputs(batch, path_output, sample_rate_hertz=16000):
    for filename in batch:
        output_filename = filename[:-4] + "GoogleOutput" + ".txt"
        sample_recognize(path_wav + filename, path_output + output_filename, sample_rate_hertz)

def get_missing_files(batch, path):
    cnt = 0
    all_files = os.listdir(path)
    missing_f = []
    for filename in batch:
        output_filename = filename[:-4] + "GoogleOutput" + ".txt"
        existance = output_filename in all_files
        if existance:
            cnt += 1
            #print(filename, "exists")
        else:
            print ("File does not exist:" + filename)
            missing_f.append(filename)
    #print("Existing files: ", cnt)
    print(missing_f)
    return(missing_f)


wav_names = get_wav_list()
txt_names = get_txt_list()

curr_batch = select_batch(wav_names, BATCH_NO, BATCH_SIZE)
print("Wav:", len(curr_batch), " wav files found in the batch")
print("Zapisani:", len([name for name in os.listdir(path_output_2) if os.path.isfile(path_output_2+name)]))
#get_multiple_outputs(curr_batch, path_output_2)
print("Txt: ", len(txt_names))
missing = get_missing_files(txt_names, path_output_2)
print("Missing files count:", len(missing))
with open("unable_to_recognise.txt", "w") as out_f:
    for miss in missing:
        out_f.write(miss + ": ")
        with open(path_txt + miss, "r") as miss_f:
            out_f.write(clean(miss_f.read()) + "\n") 
"""
#dohvati popis txt datoteka koje odgovaraju audio zapisima
curr_batch_txt=select_batch(txt_names, BATCH_NO, BATCH_SIZE)
#izfiltrirane rečenice
corrected_sentences=get_paired_text_corrected(curr_batch_txt)
print(corrected_sentences)
"""