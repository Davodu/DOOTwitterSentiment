import nltk
import numpy as np
from nltk.tokenize import TweetTokenizer
from nltk.corpus import sentiwordnet as swn
from sklearn import svm
import pickle
from tqdm import tqdm
from process_twt import *


class SCClassifier(object):
    """
    A SVM Classifier for sentiment analysis

    Attributes:
        NBC: A trained NBClassifier
        stop_words: A list containing stop words
    """

    def __init__(self, name='SCClassifier', nbc=[]):
        self.NBClassifier = nbc
        self.name = name
        self.stop_words = get_stopwords()
        self.slang_dict = get_slang_dict()
        self.senti_score_classifier = []
        self.is_trained = False

    def change_slang(self, twt):
        for word in twt.split(' '):
            if word.strip() in self.slang_dict:
                twt = twt.replace(word.strip(), self.slang_dict[word.strip()])
        return twt

    def is_informative_tag(self, tag):
        if tag[:2] == 'JJ' or tag[:2] == 'RB' or tag[:2] == 'VB' or tag[:2] == 'NN':
            return True

    def get_senti_score(self, pos):
        postype = 0
        score = 0
        if pos[1][:2] == 'JJ':
            postype = 'a'
        elif pos[1][:2] == 'RB':
            postype = 'r'
        elif pos[1][:2] == 'VB':
            postype = 'v'
        elif pos[1][:2] == 'NN':
            postype = 'n'
        synsets = list(swn.senti_synsets(pos[0]))
        for syn in synsets:
            if postype != 0:
                if repr(syn)[-6] == postype:
                    score += syn.pos_score() - syn.neg_score()
        return score

    def get_feature_set(self, twt):
        feature_set = np.zeros((len(twt), 6))
        tknzr = TweetTokenizer()
        pbar = tqdm(total=len(twt))
        for cnt, row in enumerate(twt):
            no_slang_txt = self.change_slang(row)
            processed_twt = preprocess(no_slang_txt)
            text = tknzr.tokenize(processed_twt)
            pos = nltk.pos_tag(text)
            for ptag in pos:
                if self.is_informative_tag(ptag[1]):
                    # feature 1
                    score = self.get_senti_score(ptag)
                    if score > 0:
                        feature_set[cnt, 0] += 1
                    elif score < 0:
                        feature_set[cnt, 1] += 1
                    # feature 2
                    feature_set[cnt, 2] += score
                    # feature 3
                    feature_set[cnt, 3] += 1
            # feature 5
            feature_set[cnt, 4] = float(sum(1 for c in row if c.isupper())) / max(sum(1 for c in row if c.isalpha()), 1)
            feature_set[cnt, 5] = self.NBClassifier.test([row])
            pbar.update(1)
        pbar.close()
        return feature_set

    def train(self, pos_twt, neg_twt):
        target = np.concatenate((np.zeros((len(neg_twt), 1)), np.ones((len(pos_twt), 1))), axis=0)
        feature_set = self.get_feature_set(neg_twt + pos_twt)

        # train svm classifier here
        clf = svm.SVC(probability=True)
        clf.fit(feature_set, target)

        self.senti_score_classifier = clf
        self.is_trained = True

    def test(self, twt):
        if self.is_trained:
            feature_set = self.get_feature_set(twt)
            score = self.senti_score_classifier.predict_proba(feature_set)
            score = score[:, 1]
            return score

    def save(self):
        path = os.path.join(os.path.dirname(__file__), os.pardir, 'data', 'model')
        if not os.path.exists(path):
            os.makedirs(path)
        f = open(os.path.join(path, self.name+'.pickle'), 'wb')
        pickle.dump(self, f)
        f.close()
