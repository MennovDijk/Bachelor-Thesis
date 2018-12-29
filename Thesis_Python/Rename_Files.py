import os
import pandas as pd

os.chdir('C:/Users/ikdem/PycharmProjects/Thesis_Analysis/Thesis_Files/Correlations_4_hour_lag')


for i in range(32,54):
    df = pd.read_excel('Textblob' + str(i) + '_laggedcorrelations_polarity' + '.xlsx')
    df.to_excel('Textblob' + str(i-1) + '_laggedcorrelations_polarity' + '.xlsx', index=False)