import pandas as pd
import numpy as np
import os

amt_lags = 48
amt_files = 53

os.chdir('C:/Users/ikdem/PycharmProjects/Thesis_Analysis/Thesis_Files/Correlations_4_hour_lag')

file = 'Own_Classifier'
tweet_polarity = 'tweet'

df = pd.DataFrame()

df['File number'] = [i for i in range(1,amt_files+1)]


for lag in range(0,amt_lags+1):
    company_correlation = []
    for f in range(1,amt_files+1):
        cdf = pd.read_excel(file + str(f) + '_laggedcorrelations_' + tweet_polarity + '.xlsx')
        try:
            company_correlation.append(cdf['SP500 lagged correlations'][lag])
        except:
            company_correlation.append(0)
    df[str(lag*5)] = company_correlation

os.chdir('C:/Users/ikdem/PycharmProjects/Thesis_Analysis/Thesis_Files/Correlations_4_hour_lag/Combined_Data')
df.to_excel('Correlation Overview Graphing ' + file + ' ' +  tweet_polarity + '.xlsx', sheet_name='sheet1', index=False)
# for each lag, check all of the files and append them to a list
# then