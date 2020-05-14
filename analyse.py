#!/usr/bin/python

import sys
import jiwer
import distance
import csv
import os

no_args = len(sys.argv)
if no_args >= 2:
    BATCH_NO = int(sys.argv[1])
else:
    BATCH_NO = 1 

BATCH_SIZE = 2328

path_wav = "../VEPRAD/Wav/"
path_txt = "../VEPRAD/Txt/"
path_output = "../GoogleOutput2/"

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

#To get rid of unnecessary symbols and replace some of them
def get_paired_text_corrected(batch):
    sentences=list()
    for filename in batch:
        with open(path_txt+filename,"r") as f:
            sentence=jiwer.RemoveKaldiNonWords()(f.read())
            sentence=sentence.replace("^","ć");
            sentences.append(jiwer.RemoveMultipleSpaces()(sentence))
            sentences=jiwer.SubstituteRegexes({r"{": r"š",r"`":r"ž",r"}":r"đ",r"~":r"č",r"#":r"dž"})(sentences)
    return sentences

def extract_contents(path, names):
    sentences = list()
    for filename in names:
        file_to_open = path + "GoogleOutput.".join(filename.split("."))
        try:
            with open(file_to_open, "r") as f:
                sentence = f.read()
                sentences.append(jiwer.RemoveMultipleSpaces()(sentence))
        except:
            sentences.append("unknownvalueerror")
    return sentences

def put_to_lowercase(sentences):
    ret = list()
    for sentence in sentences:
        ret.append(sentence.lower())
    return ret
    
def analyse_wer(corrected_sentences, predicted_sentences):
    word_error_rate = list()
    match_error_rate = list()
    word_info_lost = list()
    for i in range(len(corrected_sentences)):
        all_measures = jiwer.compute_measures(predicted_sentences[i], corrected_sentences[i])
        word_error_rate.append(all_measures["wer"])
        match_error_rate.append(all_measures['mer'])
        word_info_lost.append(all_measures['wil'])
    return (word_error_rate, match_error_rate, word_info_lost)

## If file exists, delete it ##
if os.path.isfile("affected_words.txt"):
    os.remove("affected_words.txt")

txt_names = get_txt_list()

# fetch the content of txt files that correspond the audio files
curr_batch_txt=select_batch(txt_names, BATCH_NO, BATCH_SIZE)
# filtered sentences
corrected_sentences=get_paired_text_corrected(curr_batch_txt)

# fetch the content of txt files that came from Google API
predicted_sentences=extract_contents(path_output, curr_batch_txt)

# lowercase all the sentences ot avoid unnecessary differences
corrected_sentences = put_to_lowercase(corrected_sentences)
predicted_sentences = put_to_lowercase(predicted_sentences)

#print(corrected_sentences)
#print(predicted_sentences)

# Analysing WER(word error rate), MER (match error rate) and WIL (word information lost)
word_error_rate, match_error_rate, word_info_lost = analyse_wer(corrected_sentences, predicted_sentences)

avg_wer = sum(word_error_rate)/len(word_error_rate)
print("Average WER:", avg_wer)

with open('statistics.csv', mode='w') as csv_file:
    writer = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    writer.writerow([
        "Filename", 
        "Corrected sentence", 
        "Predicted sentence", 
        "WER from jiwer", 
        "Substitutions", 
        "Deletions", 
        "Insertions", 
        "Correct", 
        "N", 
        "Our WER",
        "MER from jiwer",
        "WIL from jiwer"
    ])
    for i in range(len(word_error_rate)):
        filename = txt_names[i]
        seq1 = corrected_sentences[i].strip().split(" ")
        seq2 = predicted_sentences[i].strip().split(" ")
        jiwers_wer = word_error_rate[i]
        S, D, In, C = distance.get_steps(seq2, seq1, "affected_words.txt")
        N = S + D + C
        our_wer = distance.wer(S, D, In, C)
        jiwers_mer = match_error_rate[i]
        jiwers_wil = word_info_lost[i]
        writer.writerow([
            filename,
            corrected_sentences[i],
            predicted_sentences[i],
            jiwers_wer,
            S,
            D,
            In,
            C,
            N,
            our_wer,
            jiwers_mer,
            jiwers_wil
        ])