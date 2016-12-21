import nltk,sys,os
import numpy as np
import pickle
from process_twt import *




class NBClassifier(object):
    """
    A Naive Bayes Classifier for sentiment analysis
    Attributes:
        feature_list: A list containing informative words
        stop_words: A list containing stop words
        is_trained: An indicator of whether classifier is trained
        NBClassifier: Classifier
    """

    def __init__(self, name='NBClassifier'):
        self.feature_list = []
        self.stop_words = get_stopwords()
        self.slang_dict = get_slang_dict()
        self.is_trained = False
        self.NBClassifier = []
        self.name = name

    def get_feature_vector(self, twt):
        feature_vector = []
        # split tweet into words
        words = twt.split()
        for w in words:
            # strip punctuation
            w = w.strip('\'"?,.')
            # check if the word stats with an alphabet
            val = re.search(r"^[a-zA-Z][a-zA-Z0-9]*$", w)
            # ignore if it is a stop word
            if w in self.stop_words or val is None:
                continue
            else:
                feature_vector.append(w.lower())
        return feature_vector

    def extract_features(self, twt):
        twt_words = set(twt)
        features = {}
        for word in self.feature_list:
            features['contains(%s)' % word] = (word in twt_words)
        return features
    
    def train(self, pos_twt, neg_twt):
        tweets = []
        for row in pos_twt:
            sentiment = 'positive'
            processed_twt = preprocess(row, slangdict=self.slang_dict)
            feature_vector = self.get_feature_vector(processed_twt)
            self.feature_list.extend(feature_vector)
            tweets.append((feature_vector, sentiment))
        for row in neg_twt:
            sentiment = 'negative'
            processed_twt = preprocess(row, slangdict=self.slang_dict)
            feature_vector = self.get_feature_vector(processed_twt)
            self.feature_list.extend(feature_vector)
            tweets.append((feature_vector, sentiment))
        # remove duplicates in feature list
        self.feature_list = list(set(self.feature_list))

        # train classifier
        training_set = nltk.classify.util.apply_features(self.extract_features, tweets)
        self.NBClassifier = nltk.NaiveBayesClassifier.train(training_set)
        self.is_trained = True

    def test(self, twt):
        if self.is_trained:
            score = np.zeros((len(twt), 1))
            for cnt, row in enumerate(twt):
                row = preprocess(row)
                score[cnt] = (self.NBClassifier.prob_classify(self.extract_features(
                    self.get_feature_vector(row)))).prob('positive')
            return score

    def informative_features(self, num=10):
        if self.is_trained:
            return self.NBClassifier.show_most_informative_features(num)
        else:
            return ['Error: Classifier has not been trained']

    def save(self):
        path = os.path.join(os.path.dirname(__file__), os.pardir, 'data', 'model')
        if not os.path.exists(path):
            os.makedirs(path)
        f = open(os.path.join(path, self.name+'.pickle'), 'wb')
        pickle.dump(self, f)
        f.close()
















