from nltk.twitter import Query, credsfromfile
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter
import datetime as dt
import os
import pickle
import sys
sys.path.append("../dotsa")
from twitter_senti_analyzer import senti_score_time

# settings
oauth = credsfromfile()
client = Query(**oauth)
twtNum = 1000
startTime = [2016, 11, 8, 12, 0]
step = 30
step_num = 48

path = os.path.join(os.path.dirname(__file__), os.pardir, 'data', 'model')
f = open(os.path.join(path, 'NBClassifier.pickle'), 'r')
NBC = pickle.load(f)

origin = dt.datetime(startTime[0], startTime[1], startTime[2], startTime[3], startTime[4])
dates = []
for i in range(step_num):
    next_val = origin + dt.timedelta(minutes=step*i)
    dates.append(next_val)

hilary_score = senti_score_time('hilary clinton', client, NBC, twtNum, startTime, step, step_num, 1)
trump_score = senti_score_time('donald trump', client, NBC, twtNum, startTime, step, step_num, 1)

hilary_mean = np.mean(hilary_score, axis=0)
hilary_upper = hilary_mean + np.std(hilary_score, axis=0)*0.1
hilary_lower = hilary_mean - np.std(hilary_score, axis=0)*0.1

trump_mean = np.mean(trump_score, axis=0)
trump_upper = trump_mean + np.std(trump_score, axis=0)*0.1
trump_lower = trump_mean - np.std(trump_score, axis=0)*0.1

fig, ax = plt.subplots()
plt.xticks(rotation=70)
plt.plot(dates, np.mean(hilary_score, axis=0), color='blue', linewidth=2, label='Hilary Clinton')
plt.plot(dates, np.mean(trump_score, axis=0), color='red', linewidth=2, label='Donald Trump')

ax.fill_between(dates, hilary_lower, hilary_upper, facecolor='yellow', alpha=0.5)
ax.fill_between(dates, trump_lower, trump_upper, facecolor='yellow', alpha=0.5)

ax.xaxis.set_major_formatter(DateFormatter('%d %H:%M'))
plt.xlabel('days')
plt.ylabel('score')
plt.title('Sentiment Score of Candidates')
plt.legend(loc="lower left")
plt.grid(True)
plt.show()
