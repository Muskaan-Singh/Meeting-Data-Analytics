# -*- coding: utf-8 -*-
"""Bar plots(Averaged over entire dataset)

import pandas as pd
import numpy as np
import nltk
import nltk
nltk.download('stopwords')
nltk.download('punkt')
from nltk.corpus import stopwords
import csv
from nltk.tag import pos_tag # for proper noun
from nltk.tokenize import word_tokenize, sent_tokenize
from statistics import median
import math
from copy import deepcopy
import os
import xml.etree.ElementTree as ET

import matplotlib.pyplot as plt
import seaborn as sns

import statistics

from google.colab import drive
drive.mount('/content/drive')

"""# AMI Corpus

Get data from your drive folder
"""

path='/content/drive/MyDrive/AMICorpusXML-master/AMICorpusXML-master/data/ami-transcripts'
filelist=os.listdir(path)
transcripts={}
for file in filelist:
    with open(f'{path}/{file}', 'r') as f: 
        txt=f.read()
        transcripts[file.split('.')[0]]=txt

path='/content/drive/MyDrive/AMICorpusXML-master/AMICorpusXML-master/data/ami-summary/extractive'
filelist=os.listdir(path)       
extractive_summary={}
for file in filelist:
    with open(f'{path}/{file}', 'r') as f: 
        txt=f.read()
        extractive_summary[file.split('.')[0]]=txt 
        
path='/content/drive/MyDrive/AMICorpusXML-master/AMICorpusXML-master/data/ami-summary/abstractive'
filelist=os.listdir(path)       
abstractive_summary={}
for file in filelist:
    with open(f'{path}/{file}', 'r') as f: 
        txt=f.read()
        abstractive_summary[file.split('.')[0]]=txt

        
inner_join_transcripts=deepcopy(transcripts)
inner_join_extractive_summary=deepcopy(extractive_summary)
inner_join_abstractive_summary=deepcopy(abstractive_summary)
l=list(transcripts.keys())

for i in l:
    if i not in inner_join_abstractive_summary:
        del inner_join_transcripts[i]
        if i in inner_join_extractive_summary:
            del inner_join_extractive_summary[i]
        continue
    if i not in inner_join_extractive_summary:
        del inner_join_transcripts[i]
        if i in inner_join_abstractive_summary:
            del inner_join_abstractive_summary[i]

def ami_mean(transcripts, small_threshold , big_threshold ):
    stopWords = list(set(stopwords.words("english")))
    count_small=0
    count_big=0
    sum_small=0
    sum_big=0
    position_small=[]
    position_big=[]
    total_sent=0
    total_words=0
    total_refined_words=0
    unique={}
    number=len(transcripts)
    total_unique_refined_words=0
    max_len=[]
    position_max_len=[]
    small_bool=[]
    turns=0
    for key in transcripts.keys():
        txt=nltk.sent_tokenize(transcripts[key])
        total_sent+=len(txt)
        m=0
        p=0
        for index,sentence in enumerate(txt):
            temp=nltk.word_tokenize(sentence)
            sen_len=len(temp)
            m=max(m,sen_len)
            if m==sen_len:
                p=index/len(txt)
            temp=[word.lower() for word in temp]
            word_tokens_refined=[x for x in temp if x not in stopWords]
            for word in word_tokens_refined:
                if word not in unique: 
                    total_unique_refined_words+=1
                    unique[word]=1
                elif word in unique:
                    unique[word]+=1

            total_refined_words+=len(word_tokens_refined)
            total_words+=sen_len
            
            if sen_len<small_threshold:
                count_small+=1
                sum_small+=sen_len
                position_small.append(index/len(txt))
                small_bool.append(1)
            elif sen_len>big_threshold:
                count_big+=1
                sum_big+=sen_len
                position_big.append(index/len(txt))
                small_bool.append(0)
            else:
                small_bool.append(0)
                
        max_len.append(m)
        position_max_len.append(p)

    # number of continuous occurances
    small_cont=0
    check=False
    for i in range(0,len(small_bool),4):
        if sum(small_bool[i:i+4])>=2:
            small_cont+=1
            check=False
        else:
            try: 
                if sum(small_bool[i:i+4])==1 and small_bool[i+3]==1:
                    check=True
                elif sum(small_bool[i:i+4])==1 and small_bool[i]==1 and check==True:
                    small_cont+=1
                    check=False            
            except:
                pass

    
    
    return (count_small, count_big, sum_small, sum_big, position_small, position_big, 
total_sent, total_words, total_refined_words, total_unique_refined_words, unique, number, max_len,
            position_max_len, small_cont)

(count_small_transcripts_ami, count_big_transcripts_ami, sum_small_transcripts_ami, 
sum_big_transcripts_ami, position_small_transcripts_ami, position_big_transcripts_ami, 
total_sent_transcripts_ami, total_words_transcripts_ami, total_refined_words_transcripts_ami,
total_refined_unique_words_transcripts_ami, unique_dict_transcripts_ami, number_transcripts_ami,
max_len_transcripts_ami, position_max_len_transcripts_ami, small_cont_transcripts_ami) = ami_mean(transcripts, 5 , 10)

(count_small_esum_ami, count_big_esum_ami, sum_small_esum_ami, 
sum_big_esum_ami, position_small_esum_ami, position_big_esum_ami, 
total_sent_esum_ami, total_words_esum_ami, total_refined_words_esum_ami,
total_refined_unique_words_esum_ami, unique_dict_esum_ami,number_esum_ami,
max_len_esum_ami, position_max_len_esum_ami,small_cont_esum_ami)  = ami_mean(extractive_summary, 5 , 10)

(count_small_asum_ami, count_big_asum_ami, sum_small_asum_ami, 
sum_big_asum_ami, position_small_asum_ami, position_big_asum_ami, 
total_sent_asum_ami, total_words_asum_ami, total_refined_words_asum_ami,
total_refined_unique_words_asum_ami, unique_dict_asum_ami,number_asum_ami,
max_len_asum_ami, position_max_len_asum_ami,small_cont_asum_ami) = ami_mean(abstractive_summary, 5 , 10)

# number of hours:
ami_hours=100  #from their website

"""# ICSI Dataset"""

path='/content/drive/MyDrive/ICSI_original_transcripts/transcripts'
temp=os.listdir(path)
root_list=[]
meeting_name_list=[]
text_list=[]
time_list=[]

path1='/content/drive/MyDrive/ICSI_original_transcripts/Summarization/abstractive'
absumfilelist=os.listdir(path1)

filelist=[]
for file in absumfilelist:
    if f'{file[:-12]}.mrt' in temp:
        filelist.append(f'{file[:-12]}.mrt')


for file in filelist:
    if file[-3:]=='mrt':
        tree = ET.parse(f'{path}/{file}')
        root = tree.getroot()
        root_list.append(root)
        meeting_name=root.attrib['Session']
        meeting_name_list.append(meeting_name)
        time = float(root[1].attrib['EndTime'])-float(root[1].attrib['StartTime'])
        time_list.append(time)
        txt=[]
        for child in root[1]:
            txt.append(child.text)
        text_list.append(txt)
        
ab_sumroot_list=[]
ab_sumtext_list=[]
for f in absumfilelist:
    tree = ET.parse(f'{path1}/{f}')
    root = tree.getroot()
    ab_sumroot_list.append(root)
    txt=[]
    s=[]
    for child in ab_sumroot_list[0]:
        for i in child:
            txt.append(i.text)
    ab_sumtext_list.append(txt)

icsi_hours=sum(time_list)/3600

def icsi_mean(text_list,small_threshold, big_threshold):
    stopWords = list(set(stopwords.words("english")))
    count_small=0
    count_big=0
    sum_small=0
    sum_big=0
    position_small=[]
    position_big=[]
    total_sent=0
    total_words=0
    total_refined_words=0
    unique={}
    total_unique_refined_words=0
    number=len(text_list)
    
    max_len=[]
    position_max_len=[]
    
    small_bool=[]
    for i in range(len(text_list)):
        # index of one document 
        
        total_sent+=len(text_list[i])
        m=0
        p=0
        #m=max(m,len(text_list[i]))
        #if m==len(text_list[i]):
        #    p=i/
        for index,text in enumerate(text_list[i]):
            
            a=nltk.word_tokenize(text)
            m=max(m,len(a))
            if m==len(a):
                p=index/len(text_list[i])
            a=[word.lower() for word in a]
            word_tokens_refined=[x for x in a if x not in stopWords]
            for word in word_tokens_refined:
                if word not in unique: 
                    total_unique_refined_words+=1
                    unique[word]=1
                elif word in unique:
                    unique[word]+=1
            total_refined_words+=len(word_tokens_refined)
            total_words+=len(a)
            
            if len(a)<small_threshold:
                count_small+=1
                sum_small+=len(a)
                position_small.append(index/len(text_list[i]))
                small_bool.append(1)
            elif len(a)>big_threshold:
                count_big+=1
                sum_big+=len(a)
                position_big.append(index/len(text_list[i]))
                small_bool.append(0)
            else:
                small_bool.append(0)
            max_len.append(m)
            position_max_len.append(p)
     
    small_cont=0
    check=False
    for i in range(0,len(small_bool),4):
        if sum(small_bool[i:i+4])>=2:
            small_cont+=1
            check=False
        else:
            try:
                if sum(small_bool[i:i+4])==1 and small_bool[i+3]==1:
                    check=True
                elif sum(small_bool[i:i+4])==1 and small_bool[i]==1 and check==True:
                    small_cont+=1
                    check=False  
            except:
                pass

                
    return (count_small, count_big, sum_small, sum_big, position_small, position_big, total_sent,total_words,
total_refined_words, total_unique_refined_words, unique, number, max_len, position_max_len, small_cont)

(count_small_transcripts_icsi, count_big_transcripts_icsi, sum_small_transcripts_icsi,
sum_big_transcripts_icsi, position_small_transcripts_icsi, position_big_transcripts_icsi,
total_sent_transcripts_icsi,total_words_transcripts_icsi, total_refined_words_transcripts_icsi, 
total_refined_unique_words_transcripts_icsi, unique_dict_transcripts_icsi, number_transcripts_icsi, 
max_len_transcripts_icsi, position_max_len_transcripts_icsi, small_cont_transcripts_icsi)=icsi_mean(text_list,5,10)

(count_small_asum_icsi, count_big_asum_icsi, sum_small_asum_icsi,
sum_big_asum_icsi, position_small_asum_icsi, position_big_asum_icsi,
total_sent_asum_icsi,total_words_asum_icsi, total_refined_words_asum_icsi, 
total_refined_unique_words_asum_icsi, unique_dict_asum_icsi, number_asum_icsi,
max_len_asum_icsi, position_max_len_asum_icsi, small_count_asum_icsi)=icsi_mean(ab_sumtext_list,5,10)

"""# AutoMin Dataset"""

path='/content/drive/MyDrive/deidentified-meetings/deidentified-meetings'
filelist=os.listdir(path)

automin_transcripts={}
automin_summary={}
participants={}
for file in filelist:
    summs={}
    if file[-2:]=='en':
        f=os.listdir(f'{path}/{file}')
        for ts in f:
            if ts[-4:]!='.txt':
                continue
            #print(ts[:7])
            
            if ts[:10]=='transcript':
                name=list(ts.split('_'))[2][:8]
                with open(f'{path}/{file}/{ts}', 'r', encoding='utf8') as f1:
                    txt=f1.read()
                    automin_transcripts[file[:-3]]=txt
                    
            if ts[:7]=='minutes':
                #print(ts[:7])
                name=''.join(list(ts.split('.'))[-3])
                with open(f'{path}/{file}/{ts}', 'r', encoding='utf8') as f2:
                    txt=f2.read()
                    summs[name]=txt
        automin_summary[file[:-3]]=summs

(count_small_transcripts_automin, count_big_transcripts_automin, sum_small_transcripts_automin, 
sum_big_transcripts_automin, position_small_transcripts_automin, position_big_transcripts_automin, 
total_sent_transcripts_automin, total_words_transcripts_automin, total_refined_words_transcripts_automin,
total_refined_unique_words_transcripts_automin, unique_dict_transcripts_automin, number_transcripts_automin,
max_len_transcripts_automin, position_max_len_transcripts_automin, small_cont_transcripts_automin) = ami_mean(automin_transcripts, 5 , 10)

count_small_asum_automin=[]
count_big_asum_automin=[]
sum_small_asum_automin=[]
sum_big_asum_automin=[]
position_small_asum_automin=[]
position_big_asum_automin=[]
total_sent_asum_automin=[]
total_words_asum_automin=[]
total_refined_words_asum_automin=[]
total_refined_unique_words_asum_automin=[]
unique_dict_asum_automin=[]
number_asum_automin=[]
max_len_asum_automin=[]
position_max_len_asum_automin=[]
small_cont_asum_automin=[]

ll=[count_small_asum_automin, count_big_asum_automin, sum_small_asum_automin, 
sum_big_asum_automin, position_small_asum_automin, position_big_asum_automin, 
total_sent_asum_automin, total_words_asum_automin, total_refined_words_asum_automin,
total_refined_unique_words_asum_automin, unique_dict_asum_automin, number_asum_automin,
max_len_asum_automin, position_max_len_asum_automin, small_cont_asum_automin]

for key in automin_summary.keys():
    temp=ami_mean(automin_summary[key], 5,10)
    for index in range(len(temp)):
        ll[index].append(temp[index])
    
count_small_asum_automin=sum(count_small_asum_automin)
count_big_asum_automin=sum(count_big_asum_automin)
sum_small_asum_automin=sum(sum_small_asum_automin)
sum_big_asum_automin=sum(sum_big_asum_automin)
position_small_asum_automin=sum(position_small_asum_automin,[])
position_big_asum_automin=sum(position_big_asum_automin,[])
total_sent_asum_automin=sum(total_sent_asum_automin)
total_words_asum_automin=sum(total_words_asum_automin)
total_refined_words_asum_automin=sum(total_refined_words_asum_automin)
total_refined_unique_words_asum_automin=sum(total_refined_unique_words_asum_automin)
number_asum_automin=sum(number_asum_automin)
max_len_asum_automin=sum(max_len_asum_automin,[])
position_max_len_asum_automin=sum(position_max_len_asum_automin,[])
small_cont_asum_automin=sum(small_cont_asum_automin)

"""# AMI Turns and number of speakers (using change in speaker) """

turns_list=[]
speaker_list=[]

for key in automin_transcripts.keys():
    s=[]
    check=False
    turns=0
    speaker=[]
    for index,i in enumerate(automin_transcripts[key]):
        if check == True:
            s.append(i)
        if i=='(' and automin_transcripts[key][index+1:index+7]=='PERSON':
            turns+=1
            check=True
        if i==')' and check == True:
            check=False
            speaker.append(''.join(s[:-1]))
            s=[]
    turns_list.append(turns)
    speaker_list.append(list(set(speaker)))

# number of speakers

print(len(sum(speaker_list, []))/ len(speaker_list))

# turns

print(sum(turns_list)/len(turns_list))

"""# DataFrame"""

df=pd.DataFrame(columns=['count_small', 'count_big','sum_small','sum_big','position_small','position_big',
    'total_sent','total_words','total_refined_words','total_unique_refined_words','number','unique','max_len',
                         'position_max_len','small_cont_percentage','dataset', 'label'],
                index=['ami_transcripts', 'ami_esum', 'ami_asum','icsi_transcripts', 'icsi_asum','automin_transcripts', 'automin_asum'])
df.count_small=[count_small_transcripts_ami, count_small_esum_ami, count_small_asum_ami,count_small_transcripts_icsi,count_small_asum_icsi, count_small_transcripts_automin, count_small_asum_automin]
df.count_big=[count_big_transcripts_ami, count_big_esum_ami, count_big_asum_ami,count_big_transcripts_icsi, count_big_asum_icsi, count_big_transcripts_automin, count_big_asum_automin]
df.sum_small=[sum_small_transcripts_ami, sum_small_esum_ami, sum_small_asum_ami, sum_small_transcripts_icsi,sum_small_asum_icsi, sum_small_transcripts_automin, sum_small_asum_automin]
df.sum_big=[sum_big_transcripts_ami,sum_big_esum_ami, sum_big_asum_ami, sum_big_transcripts_icsi, sum_big_asum_icsi, sum_big_transcripts_automin, sum_big_asum_automin]
df.position_small=[position_small_transcripts_ami,position_small_esum_ami, position_small_asum_ami, position_small_transcripts_icsi, position_small_asum_icsi, position_small_transcripts_automin, position_small_asum_automin]
df.position_big=[position_big_transcripts_ami,position_big_esum_ami, position_big_asum_ami, position_big_transcripts_icsi, position_big_asum_icsi, position_big_transcripts_automin, position_big_asum_automin]
df.total_sent=[total_sent_transcripts_ami, total_sent_esum_ami, total_sent_asum_ami, total_sent_transcripts_icsi, total_sent_asum_icsi, total_sent_transcripts_automin, total_sent_asum_automin]
df.total_words=[total_words_transcripts_ami,total_words_esum_ami,total_words_asum_ami, total_words_transcripts_icsi, total_words_asum_icsi, total_words_transcripts_automin, total_words_asum_automin]
df.total_refined_words=[total_refined_words_transcripts_ami, total_refined_words_esum_ami, total_refined_words_asum_ami, total_refined_words_transcripts_icsi, total_refined_words_asum_icsi, total_refined_words_transcripts_automin, total_refined_words_asum_automin]
df.total_unique_refined_words=[total_refined_unique_words_transcripts_ami, total_refined_unique_words_esum_ami, total_refined_unique_words_asum_ami, total_refined_unique_words_transcripts_icsi, total_refined_unique_words_asum_icsi, total_refined_unique_words_transcripts_ami, total_refined_unique_words_asum_automin]
df.number=[number_transcripts_ami,number_esum_ami, number_asum_ami, number_transcripts_icsi, number_asum_icsi, number_transcripts_automin, number_asum_automin]
df.unique=[unique_dict_transcripts_ami, unique_dict_esum_ami, unique_dict_asum_ami, unique_dict_transcripts_icsi, unique_dict_asum_icsi, unique_dict_transcripts_automin, unique_dict_asum_automin]
df.max_len=[max_len_transcripts_ami, max_len_esum_ami, max_len_asum_ami,max_len_transcripts_icsi,max_len_asum_icsi, max_len_transcripts_automin, max_len_asum_automin]
df.position_max_len=[position_max_len_transcripts_ami, position_max_len_esum_ami, position_max_len_asum_ami,position_max_len_transcripts_icsi,position_max_len_asum_icsi, position_max_len_transcripts_automin, position_max_len_asum_automin]
df.small_cont_percentage=[small_cont_transcripts_ami/total_sent_transcripts_ami, small_cont_esum_ami/total_sent_esum_ami, small_cont_asum_ami/total_sent_asum_ami,small_cont_transcripts_icsi/total_sent_transcripts_icsi, small_count_asum_icsi/total_sent_asum_icsi, small_cont_transcripts_automin/total_sent_transcripts_automin, small_cont_asum_automin/total_sent_asum_automin]

df.dataset=['ami', 'ami','ami', 'icsi', 'icsi','MinuteMeet', 'MinuteMeet']
df.label=['transcript', 'extractive_summary', 'abstractive_summary','transcript', 'abstractive_summary','transcript', 'abstractive_summary']

# convert list of automin unique words to dict

t={}
for dic in df['unique']['automin_asum']:
    for key in dic:
        if key in t:
            t[key]+=dic[key]
        else:
            t[key]=dic[key]
df['unique']['automin_asum']=t

"""### Novel Summary Words"""

def novel_summ_word(df, dataset):
    t=0
    for i in df['unique'][f'{dataset}_asum'].keys():
        if i not in df['unique'][f'{dataset}_transcripts'].keys():
            t+=1
            
    return t, t/len(df.unique.ami_asum)

print('Novel summary words in AMI: ', novel_summ_word(df, 'ami'))
print('Novel summary words in ICSI: ',novel_summ_word(df, 'icsi'))
print('Novel summary words in AutoMin: ',novel_summ_word(df,'automin'))

df['Novel_summary_words']=[0.13883089770354906,0,0, 0.014613778705636743,0,0.41492693110647183,0]

"""### Average length"""

# In terms of sentences
print('In terms of sentences')
print(df.total_sent/df.number)
# In terms of words
print('In terms of words')
print(df.total_words/df.number)

"""### Max sentence length"""

print('Maximum length of sentences')
print(df.max_len.apply(sum)/df.max_len.apply(len))

"""### T-test"""

from scipy.stats import ttest_ind
print('Position of big sentences in ICSI vs AutoMin: ')
print(ttest_ind(df.position_big.icsi_transcripts,df.position_big.automin_transcripts))
print('Position of big sentences in AMI vs AutoMin: ')
print(ttest_ind(df.position_big.ami_transcripts,df.position_big.automin_transcripts))

df['t_test']=[-1.08813261307985,0,0,3.9913150870382608,0,0,0]

"""### Perplexity and Entropy"""

#ami

vocab={}
for key in df.unique.ami_transcripts.keys():
    vocab[key]=df.unique.ami_transcripts[key]/len(df.unique.ami_transcripts)
stopWords = list(set(stopwords.words("english")))
perplexity=[]
for key in abstractive_summary.keys():
    asb=[]
    for sentence in nltk.sent_tokenize(abstractive_summary[key]):
        t=0
        words=nltk.word_tokenize(sentence)
        words=[word.lower() for word in words]
        word_tokens_refined=[x for x in words if x not in stopWords]
        for word in word_tokens_refined:
            if word in vocab:
                t+=np.log2(vocab[word])
        
        t=t/len(word_tokens_refined)
        asb.append(np.power(2, -t))
    perplexity.append(sum(asb)/len(asb))
print('Perplexity: ', sum(perplexity)/len(perplexity))
print('Entropy: ', np.log2(sum(perplexity)/len(perplexity)))

#icsi
vocab={}
for key in df.unique.icsi_transcripts.keys():
    vocab[key]=df.unique.icsi_transcripts[key]/len(df.unique.icsi_transcripts)
stopWords = list(set(stopwords.words("english")))
perplexity=[]

for i in range(len(ab_sumtext_list)):

    asb=[]
    for sentence in nltk.sent_tokenize(' '.join(ab_sumtext_list[i])):
        t=0
        words=nltk.word_tokenize(sentence)
        words=[word.lower() for word in words]
        word_tokens_refined=[x for x in words if x not in stopWords]
        for word in word_tokens_refined:
            if word in vocab:
                t+=np.log2(vocab[word])
        
        t=t/len(word_tokens_refined)
        asb.append(np.power(2, -t))
    perplexity.append(sum(asb)/len(asb))

print('Perplexity: ', sum(perplexity)/len(perplexity))
print('Entropy: ', np.log2(sum(perplexity)/len(perplexity)))

#automin
vocab={}
for key in df.unique.automin_transcripts.keys():
    vocab[key]=df.unique.automin_transcripts[key]/len(df.unique.automin_transcripts)
stopWords = list(set(stopwords.words("english")))

perplexity=[]
for key in automin_summary.keys():
    for key2 in automin_summary[key].keys():
        asb=[]
        for sentence in nltk.sent_tokenize(automin_summary[key][key2]):
            t=0
            words=nltk.word_tokenize(sentence)
            words=[word.lower() for word in words]
            word_tokens_refined=[x for x in words if x not in stopWords]
            for word in word_tokens_refined:
                if word in vocab:
                    t+=np.log2(vocab[word])

            t=t/len(word_tokens_refined)
            asb.append(np.power(2, -t))
        perplexity.append(sum(asb)/len(asb))

print('Perplexity: ', sum(perplexity)/len(perplexity))
print('Entropy: ', np.log2(sum(perplexity)/len(perplexity)))

"""### Correlation"""

# Correlation between transcript and summary vocabulary

from scipy.stats import pearsonr
def correlation(dataset):
    #normalize score
    t_vocab={}
    for key in df['unique'][f'{dataset}_transcripts'].keys():
        t_vocab[key]=df['unique'][f'{dataset}_transcripts'][key]/len(df['unique'][f'{dataset}_transcripts'])

    s_vocab={}
    for key in df['unique'][f'{dataset}_asum'].keys():
        s_vocab[key]=df['unique'][f'{dataset}_asum'][key]/len(df['unique'][f'{dataset}_asum'])

    corr=[]
    x=[]
    y=[]
    for key in t_vocab:
        if key in s_vocab:
            x.append(t_vocab[key])
            y.append(s_vocab[key])

    return pearsonr(x,y)[0]

print('AMI :', correlation('ami'))
print('ICSI: ', correlation('icsi'))
print('AutoMin:', correlation('automin'))

df['Correlation']=[0.84792612505478,0,0,0.9087136658578838,0,0.6568918808026464,0]

"""### LDA """

# functions 

import spacy
from gensim import corpora
import gensim

spacy.load('en')
from spacy.lang.en import English
parser = English()

def tokenize(text):
    lda_tokens = []
    tokens = parser(text)
    for token in tokens:
        if token.orth_.isspace():
            continue
        elif token.like_url:
            lda_tokens.append('URL')
        elif token.orth_.startswith('@'):
            lda_tokens.append('SCREEN_NAME')
        else:
            lda_tokens.append(token.lower_)
    return lda_tokens

import nltk
nltk.download('wordnet')
from nltk.corpus import wordnet as wn
def get_lemma(word):
    lemma = wn.morphy(word)
    if lemma is None:
        return word
    else:
        return lemma
    
from nltk.stem.wordnet import WordNetLemmatizer
def get_lemma2(word):
    return WordNetLemmatizer().lemmatize(word)

nltk.download('stopwords')
en_stop = set(nltk.corpus.stopwords.words('english'))

def prepare_text_for_lda(text):
    tokens = tokenize(text)
    tokens = [token for token in tokens if len(token) > 4]
    tokens = [token for token in tokens if token not in en_stop]
    tokens = [get_lemma(token) for token in tokens]
    return tokens

#ami 
scores=0
for key in transcripts.keys():
    text_data = []
    for line in nltk.sent_tokenize(transcripts[key]):
        tokens = prepare_text_for_lda(line)
        # print(tokens)
        if len(tokens)>=5:
            #print(tokens)
            text_data.append(tokens)
    dictionary = corpora.Dictionary(text_data)
    corpus = [dictionary.doc2bow(text) for text in text_data]
    #pickle.dump(corpus, open('corpus.pkl', 'wb'))
    #dictionary.save('dictionary.gensim')
    ldamodel = gensim.models.ldamodel.LdaModel(corpus,num_topics=50, id2word=dictionary, passes=15)
    topics = ldamodel.print_topics(num_words=20)
    a=[]
    for topic in topics:
        #print(topic[1].split('+ '))
        s=0
        for i in topic[1].split('+ '):
            s+=float(i[:5])
        a.append(s)
    maxa=max(a)
    a=[i/maxa for i in a if i/maxa>0.5]
    scores+=len(a)
    
print('Average topics AMI: ',scores/len(transcripts))

#icsi

scores=0
for index in range(len(text_list)):
    text_data = []
    for line in nltk.sent_tokenize(''.join(text_list[index])):
        tokens = prepare_text_for_lda(line)
        # print(tokens)
        if len(tokens)>=5:
            #print(tokens)
            text_data.append(tokens)
    dictionary = corpora.Dictionary(text_data)
    corpus = [dictionary.doc2bow(text) for text in text_data]
    #pickle.dump(corpus, open('corpus.pkl', 'wb'))
    #dictionary.save('dictionary.gensim')
    ldamodel = gensim.models.ldamodel.LdaModel(corpus,num_topics=100, id2word=dictionary, passes=15)
    topics = ldamodel.print_topics(num_words=20)
    a=[]
    for topic in topics:
        #print(topic[1].split('+ '))
        s=0
        for i in topic[1].split('+ '):
            s+=float(i[:5])
        a.append(s)
    maxa=max(a)
    a=[i/maxa for i in a if i/maxa>0.5]
    scores+=len(a)

    
print('Average topics ICSI: ',scores/len(text_list))

# automin

scores=0
for key in automin_transcripts.keys():
    text_data = []
    for line in nltk.sent_tokenize(automin_transcripts[key]):
        tokens = prepare_text_for_lda(line)
        # print(tokens)
        if len(tokens)>=5:
            #print(tokens)
            text_data.append(tokens)
    dictionary = corpora.Dictionary(text_data)
    corpus = [dictionary.doc2bow(text) for text in text_data]
    #pickle.dump(corpus, open('corpus.pkl', 'wb'))
    #dictionary.save('dictionary.gensim')
    ldamodel = gensim.models.ldamodel.LdaModel(corpus,num_topics=100, id2word=dictionary, passes=15)
    topics = ldamodel.print_topics(num_words=20)
    a=[]
    for topic in topics:
        #print(topic[1].split('+ '))
        s=0
        for i in topic[1].split('+ '):
            s+=float(i[:5])
        a.append(s)
    maxa=max(a)
    a=[i/maxa for i in a if i/maxa>0.5]
    scores+=len(a)
    
print('Average topics AutoMin: ',scores/len(text_list))

df['topics']=[10.923976608187134,0,0,12.081967213114755,0,8.742690058479532,0]

#df.to_excel('drive/MyDrive/raw_data.xlsx')

"""### Similarity between topics in Transcript and summaries """

def get_jaccard_sim(l1, l2): 
    a = set(l1) 
    b = set(l2)
    c = a.intersection(b)
    return float(len(c)) / (len(a) + len(b) - len(c))

#ami 
similarity=[]
for key in extractive_summary.keys():
    text_data = []
    for line in nltk.sent_tokenize(transcripts[key]):
        tokens = prepare_text_for_lda(line)

        if len(tokens)>=5:
            text_data.append(tokens)
    dictionary = corpora.Dictionary(text_data)
    corpus = [dictionary.doc2bow(text) for text in text_data]

    ldamodel = gensim.models.ldamodel.LdaModel(corpus,num_topics=10, id2word=dictionary, passes=15)
    topics = ldamodel.print_topics(num_words=10)
    
    
    t_topic=[]
    for topic in topics:
        for index in range(1,len(topic[1].split('"')),2):
            t_topic.append(topic[1].split('"')[index])
    
    for line in nltk.sent_tokenize(extractive_summary[key]):
        tokens = prepare_text_for_lda(line)
        if len(tokens)>=5:
            text_data.append(tokens)
    dictionary = corpora.Dictionary(text_data)
    corpus = [dictionary.doc2bow(text) for text in text_data]

    ldamodel = gensim.models.ldamodel.LdaModel(corpus,num_topics=10, id2word=dictionary, passes=15)
    topics = ldamodel.print_topics(num_words=10)
    
    
    s_topic=[]
    for topic in topics:
        for index in range(1,len(topic[1].split('"')),2):
            s_topic.append(topic[1].split('"')[index])
    similarity.append(get_jaccard_sim(t_topic, s_topic))
print('Jaccard similarity between transcript and summary topics: ', statistics.mean(similarity))

#icsi
similarity=[]
for index in range(len(text_list)):
    text_data = []
    for line in nltk.sent_tokenize(''.join(text_list[index])):
        tokens = prepare_text_for_lda(line)

        if len(tokens)>=5:
            text_data.append(tokens)
    dictionary = corpora.Dictionary(text_data)
    corpus = [dictionary.doc2bow(text) for text in text_data]
    ldamodel = gensim.models.ldamodel.LdaModel(corpus,num_topics=100, id2word=dictionary, passes=15)
    topics = ldamodel.print_topics(num_words=20)
    t_topic=[]
    for topic in topics:
        for index in range(1,len(topic[1].split('"')),2):
            t_topic.append(topic[1].split('"')[index])
    
    for line in nltk.sent_tokenize(''.join(ab_sumtext_list[index])):
        tokens = prepare_text_for_lda(line)
        if len(tokens)>=5:

            text_data.append(tokens)
    dictionary = corpora.Dictionary(text_data)
    corpus = [dictionary.doc2bow(text) for text in text_data]
    ldamodel = gensim.models.ldamodel.LdaModel(corpus,num_topics=10, id2word=dictionary, passes=15)
    topics = ldamodel.print_topics(num_words=10)
    s_topic=[]
    for topic in topics:
        for index in range(1,len(topic[1].split('"')),2):
            s_topic.append(topic[1].split('"')[index])
    similarity.append(get_jaccard_sim(t_topic, s_topic))
print('Jaccard similarity between transcript and summary topics: ', statistics.mean(similarity))

#automin

similarity=[]
for key in automin_transcripts.keys():
    text_data = []
    for line in nltk.sent_tokenize(automin_transcripts[key]):
        tokens = prepare_text_for_lda(line)
        if len(tokens)>=5:
            text_data.append(tokens)
    dictionary = corpora.Dictionary(text_data)
    corpus = [dictionary.doc2bow(text) for text in text_data]
    ldamodel = gensim.models.ldamodel.LdaModel(corpus,num_topics=10, id2word=dictionary, passes=15)
    topics = ldamodel.print_topics(num_words=10)
    t_topic=[]
    for topic in topics:
        for index in range(1,len(topic[1].split('"')),2):
            t_topic.append(topic[1].split('"')[index])
    
    text_data=[]
    for key1 in automin_summary[key]:
        for line in nltk.sent_tokenize(automin_summary[key][key1]):
            tokens = prepare_text_for_lda(line)
            if len(tokens)>=5:
                text_data.append(tokens)
    dictionary = corpora.Dictionary(text_data)
    corpus = [dictionary.doc2bow(text) for text in text_data]
    ldamodel = gensim.models.ldamodel.LdaModel(corpus,num_topics=10, id2word=dictionary, passes=15)
    topics = ldamodel.print_topics(num_words=10)
    
    s_topic=[]
    for topic in topics:
        for index in range(1,len(topic[1].split('"')),2):
            s_topic.append(topic[1].split('"')[index])
    similarity.append(get_jaccard_sim(t_topic, s_topic))
print('Jaccard similarity between transcript and summary topics: ', statistics.mean(similarity))

"""## Inter Annotator Agreement"""

from scipy.stats import chisquare
chisq=[]
standard_deviations=[]
for key1 in automin_summary.keys():
    scores=0
    og=[]
    full_dioc={}
    dioc=[]
    for key in automin_summary[key1].keys():
        text_data = []
        a=[]
        for line in nltk.sent_tokenize(automin_summary[key1][key]):
            tokens = prepare_text_for_lda(line)
            # print(tokens)
            if len(tokens)>=5:
                #print(tokens)
                text_data.append(tokens)
        dictionary = corpora.Dictionary(text_data)
        corpus = [dictionary.doc2bow(text) for text in text_data]
        #pickle.dump(corpus, open('corpus.pkl', 'wb'))
        #dictionary.save('dictionary.gensim')
        ldamodel = gensim.models.ldamodel.LdaModel(corpus,num_topics=10, id2word=dictionary, passes=15)
        topics = ldamodel.print_topics(num_words=10)
        topic_list=[]
        topc_dic={}
        for topic in topics:
            #print(topic[1].split('+'))
            for i in topic[1].split('+'):
                a.append(i[7:-1])
                name=i[7:-1]
                if name in dioc:
                    full_dioc[name]+=1
                else:
                    full_dioc[name]=1
                if name in topc_dic:
                    topc_dic[name]+=1
                else:
                    topc_dic[name]=1

            #a.append(topic[1].split('+')[7:-1])
            topic_list.append(a)
        dioc.append(topc_dic)
        og.append(topic_list)
    vals=[]
    for i in range(len(dioc)):
        #print(i)
        x_obs=list(dioc[i].values())
        y_exp=[]
        for key in dioc[i]:
            if key in full_dioc:
                y_exp.append(full_dioc[key])
            else:
                y_exp.append(0)
        vals.append(chisquare(x_obs,y_exp)[1])
    chisq.append(statistics.median(vals))
    if len(vals)>1:
        standard_deviations.append(statistics.stdev(vals))
    else:
        standard_deviations.append(0)

"""# Graphs

### Distribution of small sentences in datasets
"""

ax=sns.kdeplot(df.position_small.loc['ami_transcripts'])
sns.kdeplot(df.position_small.loc['icsi_transcripts'])
sns.kdeplot(df.position_small.loc['automin_transcripts'])
ax.set(xlabel='Position')
plt.legend(['ami', 'icsi', 'MinuteMeet'],bbox_to_anchor=(1.31, 1), loc='upper right')

"""### Distribution of big sentences in datasets """

ax=sns.kdeplot(df.position_big.loc['ami_transcripts'])
sns.kdeplot(df.position_big.loc['icsi_transcripts'])
sns.kdeplot(df.position_big.loc['automin_transcripts'])
ax.set(xlabel='Position')
plt.legend(['ami', 'icsi', 'MinuteMeet'],bbox_to_anchor=(1.31, 1), loc='upper right')

"""### Total sentences """

ax=sns.barplot(x=df.label,y=df.total_sent, hue=df.dataset, palette='Blues')
ax.set(xlabel='Datasets', ylabel='Total sentences')

"""### Total words """

ax=sns.barplot(x=df.label,y=df.total_words, hue=df.dataset, palette='Blues')
ax.set(xlabel='Datasets', ylabel='Total words')

"""### Total refined words  (occurance)"""

sns.barplot(x=df.label,y=df.total_refined_words, hue=df.dataset, palette='Blues')

"""### Total unique refined words  (Vocabulary)"""

ax=sns.barplot(x=df.label,y=df.total_unique_refined_words, hue=df.dataset, palette='Blues')
ax.set(xlabel='Datasets', ylabel='Size of vocabulary')

"""### Frequency of small talk """

ax=sns.barplot(x=df.label,y=df.count_small, hue=df.dataset, palette='Blues')
ax.set(xlabel='Datasets', ylabel='Frequency of small talk')

"""### Frequency of big talk """

ax=sns.barplot(x=df.label,y=df.count_big, hue=df.dataset, palette='Blues')
ax.set(xlabel='Datasets', ylabel='Frequency of big talk')

"""### Percentage of small talk (sentences) """

ax=sns.barplot(x=df.label,y=(df.count_small/df.total_sent)*100, hue=df.dataset, palette='Blues')
ax.set(xlabel='Datasets', ylabel='Percentage of small sentences')

"""### Percentage of continuos small talk"""

ax=sns.barplot(x=df.label, y=df.small_cont_percentage*100, hue=df.dataset, palette='Blues')
ax.set(xlabel='Datasets', ylabel='Percentage of continuous small sentences')

"""### Percentage of big sentences  """

sns.barplot(x=df.label,y=(df.count_big/df.total_sent)*100, hue=df.dataset, palette='Blues')

"""### Average length per sentences"""

ax=sns.barplot(x=df.label,y=(df.total_sent/df.number), hue=df.dataset, palette='Blues')
ax.set(xlabel='Datasets', ylabel='Average length in terms of sentences')

"""### Average length per words"""

sns.barplot(x=df.label,y=(df.total_words/df.number), hue=df.dataset, palette='Blues')
ax.set(xlabel='Datasets', ylabel='Average length in terms of words')

"""### Max sentence length """

ax=sns.barplot(x=df.label, y=df.max_len.apply(sum)/df.max_len.apply(len), hue=df.dataset, palette='Blues')
ax.set(xlabel='Datasets', ylabel='Maximum length of sentences')

"""### Max Sentence Position"""

ax=sns.barplot(x=df.label, y=df.position_max_len.apply(sum)/df.position_max_len.apply(len), hue=df.dataset, palette='Blues')
 ax.set(xlabel='Datasets', ylabel='Position of Maximum length sentence')

"""### T-Test"""

ax=sns.barplot(x=['AMI', 'ICSI'], y=[-1.08813261307985,3.9913150870382608], palette='Blues')
ax.set(xlabel="Datasets", ylabel = "T-test score")

"""### LDA"""

ax=sns.barplot(x=['AMI','ICSI', 'MinuteMeet'], y=[10.923976608187134,12.081967213114755,8.742690058479532], palette='Blues')
ax.set(xlabel="Datasets", ylabel = "Number of topics per document")

"""### Correlation """

ax=sns.barplot(x=['AMI','ICSI', 'MinuteMeet'], y=[0.84792612505478,0.9087136658578838,0.6568918808026464], palette='Blues')
ax.set(xlabel='Datasets', ylabel='Correlation')

"""### Occurance of important sentences """

#ami 

important=[]
for key in extractive_summary.keys():
    text_data = []
    for line in nltk.sent_tokenize(transcripts[key]):
        tokens = prepare_text_for_lda(line)
        # print(tokens)
        if len(tokens)>=5:
            #print(tokens)
            text_data.append(tokens)
    dictionary = corpora.Dictionary(text_data)
    corpus = [dictionary.doc2bow(text) for text in text_data]
    #pickle.dump(corpus, open('corpus.pkl', 'wb'))
    #dictionary.save('dictionary.gensim')
    ldamodel = gensim.models.ldamodel.LdaModel(corpus,num_topics=10, id2word=dictionary, passes=15)
    topics = ldamodel.print_topics(num_words=10)
    
    
    t_topic=[]
    for topic in topics:
        for index in range(1,len(topic[1].split('"')),2):
            t_topic.append(topic[1].split('"')[index])
    
    t_topic=[word for word in t_topic if word not in stopWords]
    scores=[]
    for index,line in enumerate(nltk.sent_tokenize(transcripts[key])):
        temp=nltk.word_tokenize(line)
        temp=[word.lower() for word in temp]
        word_tokens_refined=[x for x in temp if x not in stopWords]
        score=0
        for word in word_tokens_refined:
            if word in t_topic:
                score+=1
        scores.append(score)
    max_score=max(scores)
    scores=[i/max_score for i in scores if i/max_score>0.7]
    
    important.append(len(scores))
statistics.mean(important)

# Gives 4.635036496350365

# icsi 

important=[]
for key in range(len(text_list)):
    text_data = []
    for line in nltk.sent_tokenize(''.join(text_list[key])):
        tokens = prepare_text_for_lda(line)
        # print(tokens)
        if len(tokens)>=5:
            #print(tokens)
            text_data.append(tokens)
    dictionary = corpora.Dictionary(text_data)
    corpus = [dictionary.doc2bow(text) for text in text_data]
    #pickle.dump(corpus, open('corpus.pkl', 'wb'))
    #dictionary.save('dictionary.gensim')
    ldamodel = gensim.models.ldamodel.LdaModel(corpus,num_topics=10, id2word=dictionary, passes=15)
    topics = ldamodel.print_topics(num_words=10)
    
    
    t_topic=[]
    for topic in topics:
        for index in range(1,len(topic[1].split('"')),2):
            t_topic.append(topic[1].split('"')[index])
    
    t_topic=[word for word in t_topic if word not in stopWords]
    scores=[]
    for index,line in enumerate(nltk.sent_tokenize(''.join(text_list[key]))):
        temp=nltk.word_tokenize(line)
        temp=[word.lower() for word in temp]
        word_tokens_refined=[x for x in temp if x not in stopWords]
        score=0
        for word in word_tokens_refined:
            if word in t_topic:
                score+=1
        scores.append(score)
    max_score=max(scores)
    scores=[i/max_score for i in scores if i/max_score>0.7]
    
    important.append(len(scores))
statistics.mean(important)

#automin

important=[]
for key in automin_transcripts.keys():
    text_data = []
    for line in nltk.sent_tokenize(automin_transcripts[key]):
        tokens = prepare_text_for_lda(line)
        # print(tokens)
        if len(tokens)>=5:
            #print(tokens)
            text_data.append(tokens)
    dictionary = corpora.Dictionary(text_data)
    corpus = [dictionary.doc2bow(text) for text in text_data]
    #pickle.dump(corpus, open('corpus.pkl', 'wb'))
    #dictionary.save('dictionary.gensim')
    ldamodel = gensim.models.ldamodel.LdaModel(corpus,num_topics=10, id2word=dictionary, passes=15)
    topics = ldamodel.print_topics(num_words=10)
    
    
    t_topic=[]
    for topic in topics:
        for index in range(1,len(topic[1].split('"')),2):
            t_topic.append(topic[1].split('"')[index])
    
    t_topic=[word for word in t_topic if word not in stopWords]
    scores=[]
    for index,line in enumerate(nltk.sent_tokenize(automin_transcripts[key])):
        temp=nltk.word_tokenize(line)
        temp=[word.lower() for word in temp]
        word_tokens_refined=[x for x in temp if x not in stopWords]
        score=0
        for word in word_tokens_refined:
            if word in t_topic:
                score+=1
        scores.append(score)
    max_score=max(scores)
    scores=[i/max_score for i in scores if i/max_score>0.7]
    
    important.append(len(scores))
statistics.mean(important)

df['imp_sentences_occurance']=[4.635036496350365,0,0,3.19672131147541,0,5.508928571428571,0]

ax=sns.barplot(x=['AMI','ICSI', 'MinuteMeet'], y=[4.635036496350365,3.19672131147541,5.508928571428571], palette='Blues')
ax.set(xlabel="Datasets", ylabel = "Important sentences per document")

"""### Novel summary words"""

ax=sns.barplot(x=['AMI','ICSI', 'MinuteMeet'], y=[0.13883089770354906, 0.014613778705636743,0.41492693110647183], palette='Blues')
ax.set(xlabel="Datasets", ylabel = "Percentage of Novel summary words")

"""### Similarity between topics in Transcript and summaries """

ax=sns.barplot(x=['AMI','ICSI', 'MinuteMeet'], y=[0.5206261130053645, 0.22222174277399082,0.17133001592337524], palette='Blues')
ax.set(xlabel="Datasets", ylabel = "Jaccard similarity")

"""### Perplexity and Entropy"""

ax=sns.barplot(x=['AMI','ICSI', 'MinuteMeet'], y=[37.94819131004812,81.33757646965024,27.970410946993663], palette='Blues')
ax.set(xlabel="Datasets", ylabel = "Perplexity")

ax=sns.barplot(x=['AMI','ICSI', 'MinuteMeet'], y=[5.245959220311832,6.345850099858714,4.805829545227549], palette='Blues')
ax.set(xlabel="Datasets", ylabel ="Entropy")
