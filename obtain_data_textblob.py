from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from textblob import TextBlob
from apscheduler.schedulers.background import BackgroundScheduler
import sched, json, time, googlefinance, re, rq, yahoo_finance
import _pickle as cPickle
import pandas as pd
import sys


interval = float(input('Interval to store/print data? (minutes)'))
run_time = float(input('Time to run the program? (hours)'))

# Twitter API keys
consumer_key = 'CONSUMER_KEY'
consumer_secret = 'CONSUMER_SECRET'
access_token = 'ACCESS_TOKEN'
access_token_secret = 'ACCESS_TOKEN_SECRET'

printScheduler = BackgroundScheduler()

def analyse_tweet_textblob_classifier(text):
    pos_neg = ''
    if TextBlob(text).sentiment[0] > 0.3 and TextBlob(text).sentiment[1] > 0.5:
        pos_neg = 'pos'
    elif TextBlob(text).sentiment[0] < 0.3 and TextBlob(text).sentiment[1] > 0.5:
        pos_neg = 'neg'
    else:
        pos_neg = 'neut'
    return pos_neg


def get_stock_price(stock):
    data = json.loads(json.dumps(googlefinance.getQuotes(stock)))
    return data[0].get('LastTradePrice').replace(',','')

timeStop = time.time() + 60*60*run_time

class StdOutListener(StreamListener):
    def __init__(self):
        self.posCount = 1
        self.negCount = 1
        self.tweetsCounted = []
        self.stockData = []
        self.tweetData = []

    def on_data(self, data):
        data = json.loads(data)
        if time.time() < timeStop:
            try:
                if 'rt' not in data['text'].lower() and data['user']['followers_count'] > 50 and data['user'][
                    'lang'] == 'en' and 'youtube' not in data['text'].lower():
                    result = re.sub(r"http\S+", "", data['text'])
                    # print(result, analyse_tweet_textblob_classifier(result))
                    if analyse_tweet_textblob_classifier(result) == 'pos':
                        self.posCount += 1
                        self.tweetsCounted += 1
                    if analyse_tweet_textblob_classifier(result) == 'neg':
                        self.negCount += 1
                        self.tweetsCounted += 1
            except:
                pass
            return True
        else:
            printScheduler.shutdown()
            return False

    def on_error(self, status):
        print(status)

    def returns_data(self):
        return self.stockData, self.tweetData, self.tweetsCounted

    def reset(self):
        self.wordsCounted = 0
        self.negCount = 1
        self.posCount = 1

    def prints_data(self):
        print(self.posCount, self.negCount)
        self.stockData.append(float(get_stock_price('INDEXSP:.INX')))
        self.tweetData.append(float(self.posCount/self.negCount))
        self.tweetsCounted.append(int(self.posCount + self.negCount))
        self.reset()
        # print(len(self.stockData), len(self.tweetData))
        # print('I added data and performed a reset')
        # except:
         # print('I only did a reset')
          # self.reset()
        # self.data.append((self.posCount / self.negCount, yahoo_finance.Share('^GSPC').get_price()))
        # print((self.posCount / self.negCount), yahoo_finance.Share('^GSPC').get_price())

if __name__ == '__main__':

    #This handles Twitter authentification and the connection to Twitter Streaming API
    l = StdOutListener()
    printScheduler.add_job( l.prints_data, 'interval', seconds=(60*interval) )
    printScheduler.start()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    while time.time() < timeStop:
        time.sleep(1)
        try:
            stream = Stream(auth, l)
            stream.filter(track=['trump'], stall_warnings=True)
        except:
            e = sys.exc_info()[0]
            print('error', e)


df = pd.DataFrame({'Stock Price': l.returns_data()[0], 'Pos/Neg Sentiment': l.returns_data()[1], 'Total tweets': l.returns_data()[2]})
df.to_excel('test_textblob_classifier.xlsx', sheet_name='sheet1', index=False)
print('done')

