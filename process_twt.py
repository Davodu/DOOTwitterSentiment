# -*- coding: utf-8 -*-

import re
import os
from collections import Counter
import views

# -------------------

#get probability of a word
def tokenize(text): return re.findall(r'\w+', text.lower())

WORDS  = Counter(tokenize(open(os.path.join(os.path.dirname(__file__), 'static/sentiWebApp','big.txt')).read()))
# WORDS = Counter(tokenize(open('/sentiWebApp/static/sentiWebApp/big.txt').read()))

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
        twt = twt.replace("[^a-zA-Z]","")
        twt = twt.replace(word.strip(), correction(word)) 
    return twt
#-- test autocorrect 


# phrase = "happw peopse are the unikue onez in the warld"
# print preprocess(phrase)
#output = "happy people are the unique ones in the world" 
def reduce_redundancy(twt):
    pattern = re.compile(r"(.)\1{1,}", re.DOTALL)
    return pattern.sub(r"\1\1", twt)

#--------------------------------Decode Emoticons ----------------------#
def emoji_to_text(twt):
    sad_emoticons = {":-(", ":(", ":-|", ";-(", ";-<", "|-{", '😒','😓','😔','😖',\
                    '😞','😟','😠','😡','😢','😣','😤','😥','😦','😧','😨','😩','😪',\
                    '😫','😬','😭','😾','😿','😰','😱','🙀'}
                    
    happy_emoticons = {":-)", ":)", ":o)", ":-}", ";-}", ":->", ";-)" ,'😀','😁','😂','😃','😄',\
                      '😅','😆','😇','😈','😉','😊','😋','😌','😍','😎','😏','😗','😘','😙','😚',\
                     '😛','😜','😝','😸','😹','😺','😻','😼','😽'}

    for word in twt.split(' '): 
        if word.strip() in sad_emoticons: 
            twt = twt.replace(word, 'sad')
        if word.strip() in happy_emoticons:
            twt = twt.replace(word,'happy')
    return twt


def preprocess(twt, tolower=True, slangdict={}):
    #if string contains "preprocess: " , then preprocess, else just send out same string
    if "Preprocessed: " in twt:
        # replace slangs with original words
        for word in twt.split(' '):
            if word.strip() in slangdict:
                twt = twt.replace(word.strip(), slangdict[word.strip()])
        # if tolower:
        #     twt = twt.lower()
        twt = re.sub('((www\.[^\s]+)|(https?://[^\s]+))', 'URL', twt)
        twt = re.sub('@[^\s]+', 'AT_USER', twt)
        twt = re.sub('[\s]+', ' ', twt)
        twt = re.sub(r'#([^\s]+)', r'\1', twt)
        twt = re.sub('[\s]((not)|(no))', '-not', twt)
        twt = re.sub('\'m', 'm', twt)
        twt = re.sub('\'t', 't', twt)
        twt = re.sub('\'s', '', twt)
        twt = twt.strip('\'"')
        twt = twt.strip()
        twt = reduce_redundancy(twt)
        twt = emoji_to_text(twt)
        twt = spell_correct(twt)
    else:
        # twt = views.evaluate_twt(twt)
        twt = twt
    return twt



def get_stopwords():
    stopwords = []

    fp = open(open(os.path.join(os.path.dirname(__file__), 'static/sentiWebApp','stopwords.txt')).read())
    line = fp.readline()
    while line:
        word = line.strip()
        stopwords.append(word)
        line = fp.readline()
    fp.close()
    return stopwords


def get_slang_dict():
    fp = open(open(os.path.join(os.path.dirname(__file__), 'static/sentiWebApp','slangdict.txt')).read())
    line = fp.readline()
    slangdict = {}
    while line:
        words = line.split('-')
        if len(words) == 2:
            slangdict.update({words[0].strip(): words[1].strip()})
        line = fp.readline()
    fp.close()
    return slangdict

    
#------------------------------Test------------------------------------------------------#
# twt = "preprocess: " + "eep smile...😊😊 #bismillah (at cemara residence) [pic] — https://t.co/y8bh8clydg\
# rt @salvesayson: do not think about the past. accept the present. think for the future, and face \
# tomorrow with a sweet and beautiful smile.…\
# rt @aldubmaidenpex: a: love not too :)  close\
# m: stay still &amp; smile love\
# a: its stiff not applicable este still :-( :( :-| ;-(  :-) :) :o) :-} ;-"

# print preprocess(twt, slangdict={})



