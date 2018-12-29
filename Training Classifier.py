from nltk.classify import NaiveBayesClassifier
from nltk.corpus import twitter_samples
from textblob import classifiers
from nltk.sentiment import SentimentAnalyzer
from nltk.sentiment.util import *
from os import getcwd, path
from nltk.corpus import subjectivity
import _pickle as cPickle
import numpy as np
import time


negative_file = twitter_samples.strings("negative_tweets.json")
trainer = [(x, 'neg') for x in negative_file[:2500]]
print('done')
positive_file = twitter_samples.strings("positive_tweets.json")
trainer.extend([(x, 'pos') for x in positive_file[:2500]])
print('done')

t1 = time.time()
cl = classifiers.NaiveBayesClassifier(trainer)
print(time.time() - t1)

with open('test_classifier.pkl', 'wb') as f:
    cPickle.dump(cl, f)
f.close()

