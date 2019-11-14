from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

from pymongo import MongoClient

import pandas as pd
import sqlalchemy
from sqlalchemy import create_engine
import time 

"""

The Compound score is a metric that calculates the sum of all the lexicon ratings which 
have been normalized between -1(most extreme negative) and +1 (most extreme positive). 
In the case above, lexicon ratings for andsupercool are 2.9and respectively1.3. 
The compound score turns out to be 0.75 , denoting a very high positive sentiment.

"""

USERNAME = 'postgres'
PASSWORD = 'postgres'
HOST = 'postgresdb'
PORT = '5432'
DBNAME = 'twitter'

client = MongoClient('mongodb')
db=client.twitter
mongodb='mongodb'


client = MongoClient(mongodb)
db = client.twitter
collection = db.trump_tweets
print('connect_mongo_done')
    

#def load_into_mongo(df):
#    """ create mongo database and collection"""
#    json = df.to_dict(), index = False 
#    db.trump_sentiments.insert(json)


def extract_mongodb(collection):
    result = collection.find({},{"created_at": "$created_at","location": "$location","text": "$text","followers":"$followers"})
    print('extract_mongo_done')
    result_list = list(result)
    return result_list

def create_df(result_list):
    df = pd.DataFrame(result_list)
    df['clean_text'] = df['text'].replace('!!!!','!!!',regex=True)
    print('create_df_done')
    return df

def compound_sentiment(df):
    text_list = list(df['clean_text'])
    analyser = SentimentIntensityAnalyzer()
    compound=[]
    for i in text_list:
        score = analyser.polarity_scores(i)
        compound_score = score['compound']
        compound.append(compound_score)
    df['commpound_sentiment_score'] = compound
    #df['created_at']= pd.to_datetime(df['created_at'])
    df.to_csv('test_sentiment.csv')
    #load_into_mongo(df)
    print('compound_score_added_done')
    return df

def load_sql(df):
    conn_string = f'postgres://{USERNAME}:{PASSWORD}@{HOST}:{PORT}/{DBNAME}'
    twitter_db = create_engine(conn_string)
    df.drop(df.columns[0], axis=1).to_sql('trump_tweets', twitter_db, index=False, if_exists="append", dtype = {'created_at' : sqlalchemy.DateTime()})
    print('Done_loaded_to_sql')

# , dtype={'created_at': datetime()}
    
while True:
    result_list = extract_mongodb(db.trump_tweets)
    df = create_df(result_list)
    df = compound_sentiment(df)
    load_sql(df)
    time.sleep(60)

