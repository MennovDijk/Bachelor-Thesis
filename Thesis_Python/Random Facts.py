import pandas as pd
import numpy as np
import os


os.chdir('C:/Users/ikdem/PycharmProjects/Thesis_Analysis/Thesis_Files')

total_tweets = []
greatest_stock_change = 0
greatest_polarity_change = 0

for f in range(7,55):
    df = pd.read_excel('test_textblob_classifier_SP500'+str(f)+'.xlsx')
    df.fillna(value=0, inplace=True)
    for i in range(0,len(df['Total tweets'])):
        total_tweets.append(int(df['Total tweets'][i]))
        if df['Polarity Normalized'][i] < greatest_polarity_change:
            greatest_polarity_change = df['Polarity Normalized'][i]
            time_polarity = df['Time'][i+1]
        if df['Stock Price Normalized'][i] > greatest_stock_change:
            greatest_stock_change = df['Stock Price Normalized'][i]
            time_stock = df['Time'][i+1]


print(sum(total_tweets), sum(total_tweets)/float(55))
print(greatest_polarity_change, time_polarity)
print(greatest_stock_change,  time_stock)