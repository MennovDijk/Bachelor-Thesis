import pandas as pd
import numpy as np
from scipy.stats.morestats import wilcoxon
import os
import matplotlib.pyplot as plt

os.chdir('C:/Users/ikdem/PycharmProjects/Thesis_Analysis/Thesis_Files/Correlations_4_hour_lag')

amt_lags = 48
file = 'Textblob'
tweet_stock = 'polarity'

for lag in range(0,amt_lags+1):
    list_correlations = []
    for f in range(2,55):
        try:
            df = pd.read_excel(file + str(f) +'_laggedcorrelations_' + tweet_stock + '.xlsx')
            list_correlations.append(df['SP500 lagged correlations'][lag])
        except:
            continue
    print(file, tweet_stock, lag * 5, wilcoxon(list_correlations))


# for every lag, look at all the files and append all of the correlations for every lag to a list
# create a list of 0's with len(list_from_above), then wilcoxon(list(correlations), list(zeros) for each lag