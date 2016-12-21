import nltk
import os
import re 


import re
import os

from collections import Counter

#spell correction

#get probability of a word
def tokenize(text): return re.findall(r'\w+', text.lower())

WORDS  = Counter(tokenize(open(os.path.join(os.path.dirname(__file__), os.pardir, 'data', 'big.txt')).read()))

def Prob(word, N= sum(WORDS.values())):
    return WORDS[word]/N
#-------------------
def correction(word):
    return max(candidates(word), key=Prob)

def candidates(word):
    return (known([word]) or known(edit1(word)) or known(edit2(word)) or [word])

def known(words):
    return set(w for w in words if w in WORDS)

# word distances to known words
def edit1(word):
    letters    = 'abcdefghijklmnopqrstuvwxyz'
    splits     = [(word[:i], word[i:])    for i in range(len(word) + 1)]
    deletes    = [L + R[1:]               for L, R in splits if R]
    transposes = [L + R[1] + R[0] + R[2:] for L, R in splits if len(R)>1]
    replaces   = [L + c + R[1:]           for L, R in splits if R for c in letters]
    inserts    = [L + c + R               for L, R in splits for c in letters]
    return set(deletes + transposes + replaces + inserts)

def edit2(word): 
    return (e2 for e1 in edit1(word) for e2 in edit1(e1))


def spell_correct(twt):
    for word in twt.split(' '):
        twt = twt.replace(word.strip(), correction(word)) 
    return twt
#-- test autocorrect 

# phrase = "happw peopse are the unikue onez in the warld"
# print preprocess(phrase)
#output = "happy people are the unique ones in the world" 

def reduce_redundancy(twt):
    pattern = re.compile(r"(.)\1{1,}", re.DOTALL)
    return pattern.sub(r"\1\1", twt)


def pre_process(twt, tolower=True, slangdict={}):
    # replace slangs with original words
    for word in twt.split(' '):
        if word.strip() in slangdict: #if word exists in dictionary
            twt = twt.replace(word.strip(), slangdict[word.strip()])
    if tolower:
        twt = twt.lower()
    twt = re.sub('((www\.[^\s]+)|(https?://[^\s]+))', 'URL', twt)
    twt = re.sub('@[^\s]+', 'AT_USER', twt)
    twt = re.sub('[\s]+', ' ', twt)
    twt = re.sub(r'#([^\s]+)', r'\1', twt)
    twt = twt.strip('\'"')
    twt = twt.strip()
    twt = reduce_redundancy(twt)
    return twt


def get_stopwords():
    stopwords = []

    fp = open(os.path.join(os.path.dirname(__file__), os.pardir, 'data', 'stopwords.txt'), 'r')
    line = fp.readline()
    while line:
        word = line.strip()
        stopwords.append(word)
        line = fp.readline()
    fp.close()
    return stopwords


def get_slang_dict():
    fp = open(os.path.join(o,os.path.dirname(__file__), os.pardir, 'data', 'slangdict.txt'), 'r')
    line = fp.readline()
    slangdict = {}
    while line:
        words = line.split('-')
        if len(words) == 2:
            slangdict.update({words[0].strip(): words[1].strip()})
        line = fp.readline()
    fp.close()
    return slangdict


#   #tokenize tweets
# def tokenize(tweet, slangmap={}): 
#  #replace slangs with plain english 
#  for word in tweet.split(' '): 
#  	if word.strip() in slangmap:
#  		tweet = tweet.replace(word.strip(), slangmap[word.strip()])

#  tweet = tweet.lower()


#  return tweet




#  #use slangdict.txt to create slangmap
# def init_slang_dict(): 
# 	fp = open(os.path.join(os.path.dirname(__file__),os.pardir, 'data', 'slangdict.txt'), 'r')
# 	line = fp.readline()
# 	slangmap = {}
# 	while line:
# 		words = line.split('-')
# 		if len(words) == 2:
# 			slangmap.update({words[0].strip(): words[1].strip()})
# 		line = fp.readline()
# 	fp.close()
# 	return slangmap
