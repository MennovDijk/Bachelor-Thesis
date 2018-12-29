import pandas as pd
import numpy as np
import os

#set number of lags
amt_lags = 48 # 12 * 5 = 60 minute total lag.

file = 'Own_Classifier'
tweet_polarity = 'tweet'

#for all files to analyze
for n in range(1,55):
    os.chdir('C:/Users/ikdem/PycharmProjects/Thesis_Analysis/Thesis_Files')
    df = pd.read_excel(file+str(n)+'.xlsx')
    df2 = pd.DataFrame()
    lags = []
    # for the lags set previously
    for lag in range(0,amt_lags+1):
        l1 = []
        l2 = []
        # for the length of the stock price
        for i in range(0, len(df['Stock Price Normalized'])):
            # if there is a stock price change (markets are open) and the lag is not non-existent, append the polarity measure and stock price to a list
            if str(df['Stock Price Normalized'][i]) != '0.0' and i-lag > 0:
                l2.append(float(df['Stock Price Normalized'][i]))
                if tweet_polarity == 'tweet':
                    l1.append(float(df['numTweets Normalized'][i - lag]))
                if tweet_polarity == 'polarity':
                    l1.append(float(df['Polarity Normalized'][i - lag]))
        # calculate the correlation PER LAG and append it to a seperate list
        corr = np.corrcoef(l1, l2)[0, 1]

        lags.append(float(corr))
    # save everything to a seperate excel file that just contains the lags of the corresponding files.
    df2['SP500 lagged correlations'] = lags
    os.chdir('C:/Users/ikdem/PycharmProjects/Thesis_Analysis/Thesis_Files/Correlations_4_hour_lag')
    df2.to_excel(file + str(n) + '_laggedcorrelations_' + tweet_polarity + '.xlsx', sheet_name='sheet1', index=False)


