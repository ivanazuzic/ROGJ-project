#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 23 02:50:48 2020

@author: petra
"""
import sys
import re
no_args = len(sys.argv)
if no_args >= 2:
    BATCH_NO = int(sys.argv[1])
else:
    BATCH_NO = 1 

BATCH_SIZE = 2328

path_txt = "../VEPRAD/Txt/"

#Load the names of paired txt files
def get_txt_list():
    names_list = []
    with open('paired_files.txt', 'r') as input_file:
        for row in input_file:
            txt_name = row.split()[1]
            names_list.append(txt_name)
    return names_list

# Selects a batch that we want to search through
def select_batch(names_list, batch_no, batch_size):
    b_start = (batch_no - 1) * batch_size
    b_end = (batch_no) * batch_size
    return names_list[b_start : b_end]

#To get rid of unnecessary symbols and replace some of them
def get_sentces_with_symbols(batch):
    symbol=list()
    txt_name=list()
    for filename in batch:
        with open(path_txt+filename,"r") as f:
               recenica='"'+f.read()+'"'
               pattern ="<(.\W*?)>"
               pattern2="<(.*?)>"
               try:
                   substring = re.search(pattern, recenica).group(1)
                   if(substring in symbol):
                       continue
                   else:
                       print(recenica)
                       symbol.append(substring)
                       txt_name.append(filename)

               except:
                   substring=None
               try:
                   substring2=re.search(pattern2, recenica).group(1)
                   if(substring2 in symbol):
                       continue
                   else:
                       print(recenica)
                       symbol.append(substring2)
                       txt_name.append(filename)
               except:
                  substring2=None
    return symbol,txt_name

txt_names = get_txt_list()
curr_batch_txt=select_batch(txt_names, BATCH_NO, BATCH_SIZE)
symbols,txt_datoteka=get_sentces_with_symbols(curr_batch_txt)

