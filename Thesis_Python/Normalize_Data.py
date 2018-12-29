import pandas as pd
import os

def normalize_data(l):
    nl = []
    for i in range(1,len(l)):
        nl.append(((l[i]-l[i-1])/l[i-1]))
    nl.append(0)
    return nl

os.chdir('C:/Users/ikdem/PycharmProjects/Thesis_Analysis/Thesis_Files')

file = 'test_SP500'


for i in range(2,54+1):
    print('Working on file:', i)
    df = pd.read_excel(file+str(i)+'.xlsx')
    pos_neg_list = normalize_data(df['Pos/Neg Sentiment'].tolist())
    df['Polarity Normalized'] = pos_neg_list
    num_tweets_list = normalize_data(df['Total tweets'].tolist())
    df['numTweets Normalized'] = num_tweets_list
    stock_list = normalize_data(df['Stock Price'].tolist())
    df['Stock Price Normalized'] = stock_list
    df.to_excel(file+str(i)+'.xlsx', index=False)
    print('done...')


