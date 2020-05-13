#!/usr/bin/python

import sys
import speech_recognition as sr
#dodala
import jiwer

no_args = len(sys.argv)
if no_args >= 2:
    BATCH_NO = int(sys.argv[1])
else:
    BATCH_NO = 1 

BATCH_SIZE = 10
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
            
#dodala
#To get rid of unnecessary symbols and replace some of them
def get_paired_text_corrected(batch):
    sentences=list()
    for filename in batch:
        with open(path_txt+filename,"r") as f:
            
               sentence=jiwer.RemoveKaldiNonWords()(f.read())
               sentence=sentence.replace("^","ć");
               sentences.append(jiwer.RemoveMultipleSpaces()(sentence))
               #print(sentence)
               #print(jiwer.SubstituteRegexes({r"^": r"ć"})(sentence))
               
               #sentences = ["is the world doomed or loved?", "edibles are allegedly cultivated"]
               #print(jiwer.SubstituteRegexes({r"t": r"ć"})(sentences))
    #print(sentences)
    #print(jiwer.SubstituteRegexes({r"{": r"š",r"`":r"ž",r"}":r"đ",r"~":r"č",r"#":r"dž"})(sentences))
    sentences=jiwer.SubstituteRegexes({r"{": r"š",r"`":r"ž",r"}":r"đ",r"~":r"č",r"#":r"dž"})(sentences)
    return sentences


               
wav_names = get_wav_list()
txt_names = get_txt_list()

curr_batch = select_batch(wav_names, BATCH_NO, BATCH_SIZE)
#dohvati popis txt datoteka koje odgovaraju audio zapisima
curr_batch_txt=select_batch(txt_names, BATCH_NO, BATCH_SIZE)
#izfiltrirane rečenice
corrected_sentences=get_paired_text_corrected(curr_batch_txt)
print(corrected_sentences)
