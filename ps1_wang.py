#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
WSUV AI440 PS1
@author: pengwang
"""
import os
import codecs
import collections
import numpy as np
from matplotlib import pyplot
from scipy.optimize import leastsq


def create_corpus(d):
    'list all files including system files under a folder'
    filename_all = os.listdir(path=d)
    filename_txt = []
    filename_all_length = len(filename_all)
    file_name_content_mapping = {}
    'get only *.txt, exclude other types of files'
    while filename_all_length:
        filename = filename_all[filename_all_length-1]
        txt_check = filename.find('.txt')
        if txt_check != -1:
            filename_txt.append(filename_all[filename_all_length-1])
        filename_all_length -= 1
    'create dictionary with filename as key and filecontent as value'
    for item in filename_txt:
        f = codecs.open(d+'/'+item, mode='r', encoding='utf-8')
        filecontent = f.read()
        file_name_content_mapping.update({item:filecontent})
    return file_name_content_mapping

"""((9102, 'OR_Coos_2008-04-03__08003299.txt'), 
(932, 'WA_Kitsap_2009-08-25__200908250022.txt')) """       
def corpus_char_stats(corpus):
    longest = 0
    shortest = 10000000000000000000
    longest_filename = ''
    shortest_filename = ''
    
    'find the longest and shortest' 
    for item in corpus:
        if len(corpus[item]) > longest:
            longest = len(corpus[item])
            longest_filename = item
        else:
            if len(corpus[item]) < shortest:
                shortest = len(corpus[item])
                shortest_filename = item
    shortest_longest_file = ((longest, longest_filename),(shortest, shortest_filename))
    return shortest_longest_file

def words(data):
    wordslist = []
    'split words by space'
    wordslist = data.split()
    
    'chaneg to lower case'
    wordslist_lowercase = []
    for item in wordslist:
        wordslist_lowercase.append(item.lower())
    
    'seperate alphabetic and others'
    alphabetic_only = []
    not_alphabetic_only = []
    for item in wordslist_lowercase:
        if item.isalpha() == True:
            alphabetic_only.append(item)
        else:
            not_alphabetic_only.append(item)
    seperated_words = (alphabetic_only, not_alphabetic_only)
    return seperated_words


"""ratio percent is 51.44124168514412 
WA_Benton_2009-04-06__2009-009261.txt"""
def find_word_ratios(corpus):
    lowest_ratio = 100.0
    lowest_ratio_file = ''
    ratios_list = []
    for item in corpus:
        value  = corpus.get(item)
        value_list = words(value)
        pure_alphabetic = len(value_list[0])
        non_pure_alphabetic = len(value_list[1])
        alphabetic_rate = 100 * (pure_alphabetic/(pure_alphabetic+non_pure_alphabetic))
        if alphabetic_rate < lowest_ratio:
            lowest_ratio = alphabetic_rate
            lowest_ratio_file = item
        ratios_list.append(alphabetic_rate)
        ratios_list.sort()
#    print(lowest_ratio_file)
    return ratios_list

"""[('of', 783), ('the', 665), ('and', 327), ('i', 239), 
('lien', 225), ('to', 186), ('or', 179), ('a', 153), 
('in', 149), ('for', 129)]"""
def word_frequencies(corpus):
    string_all_words = []
    top10words = []
    allwords = []
    for item in corpus:
        value = corpus.get(item)
        value_list = words(value)
        for i in value_list[0]:
            string_all_words.append(i)
    string_all_words.sort()
    'get the top 10 words'
    top10words = collections.Counter(string_all_words).most_common(10)
    
    'get all words frequencies list'
    allwords = collections.Counter(string_all_words).most_common()
#    print(allwords)
    sorted_result = []
    for item in allwords:
        item_reverse = item[::-1]
        sorted_result.append(item_reverse)
    sorted_results = sorted(sorted_result, reverse=True)
#    print(sorted_results)
    return sorted_results
    
 
corpus = create_corpus('Liens-50')
data = word_frequencies(corpus)
word_freq = []
for item in data:
    word_freq.append(item[0])
x_word_rank = np.arange(len(word_freq))+1
y_word_freq = np.array(word_freq)
#print(x_word_rank)
pyplot.figure()
pyplot.scatter(x_word_rank,y_word_freq,color="blue",label="Sample point",linewidth=0.1)
pyplot.xscale('log')
pyplot.yscale('log')
pyplot.savefig('loglog.pdf')

def func(p,x):
    k,b = p
    return k*x+b

def error(p,x,y):
    return func(p,x)-y

p0 = [100,2]
rank_log = np.log10(x_word_rank)
freq_log = np.log10(y_word_freq)
Para = leastsq(error,p0,args=(rank_log,freq_log))
k,b = Para[0]
x=np.linspace(0,5,3000)
y=k*x+b
pyplot.plot(np.power(10,x), np.power(10,y),color="orange",label="Fitting Line",linewidth=2)
pyplot.savefig('loglogfittedline.pdf')