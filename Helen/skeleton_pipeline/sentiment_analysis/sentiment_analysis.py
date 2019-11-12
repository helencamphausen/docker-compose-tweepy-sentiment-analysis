from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

from pymongo import MongoClient

import pandas as pd

"""

The Compound score is a metric that calculates the sum of all the lexicon ratings which 
have been normalized between -1(most extreme negative) and +1 (most extreme positive). 
In the case above, lexicon ratings for andsupercool are 2.9and respectively1.3. 
The compound score turns out to be 0.75 , denoting a very high positive sentiment.

"""

## Connect to Mongodb
## client = MongoClient('mongodb')
## db=client.twitter
## trump_tweets

client = MongoClient('monogodb')
db = client.twitter
collection = db.trump_tweets
result = collection.find({},{"created_at": "$created_at","text": "$text"})

pd.DataFrane(list(result))


## change from single text to list of strings

analyser = SentimentIntensityAnalyzer()

def sentiment_analyzer_scores(sentence):
    score = analyser.polarity_scores(sentence)
    print("{:-<40} {}".format(sentence, str(score)))

text = "The phone is super cool."

sentiment_analyzer_scores(text)