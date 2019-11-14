#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 14 14:10:19 2019

@author: hcamphausen
"""

from flask import Flask
from sqlalchemy import create_engine
import pandas as pd


USERNAME = 'postgres'
PASSWORD = 'postgres'
HOST = 'postgresdb'
PORT = '5432'
DBNAME = 'twitter'

conn_string = f'postgres://{USERNAME}:{PASSWORD}@{HOST}:{PORT}/{DBNAME}'
twitter_db = create_engine(conn_string)
#table name : trump_tweets
print('connection_postgres_done')

def first_query():
    
    QUERY_1 = """
            SELECT * FROM trump_tweets limit 10;
            
            """
#        
#   with base_all as (
#    
#            SELECT 
#                *,
#                CASE when commpound_sentiment_score>=0.05 then 1 else 0 end as positive_flag
#            FROM trump_tweets)
#    
#    SELECT 
#        date_trunc('hour', created_at) as hour,
#        avg(commpound_sentiment_score) as avg_compound_score,
#        sum(positive_flag) as total_positive_tweets,
#        (sum(positive_flag))/(count(created_at)) as share_positive_tweets
#    FROM base_all
#    GROUP BY 1
            
    result_1 = twitter_db.execute(QUERY_1)
    df_1 = pd.DataFrame(list(result_1), columns = result_1.keys())
    print('first_query_done')
    return df_1

def top_worst_tweets():
    
    QUERY_top = """
    with base_all as (
    
            SELECT 
                *
            FROM trump_tweets
            ORDER BY commpound_sentiment_score desc
            LIMIT 10)
    
    SELECT 
        date_trunc(hour, created_at) as hour,
        clean_text,
        location,
        commpound_sentiment_score
    FROM base_all
            
            """
        
    result_top = twitter_db.execute(QUERY_top)
    df_top = pd.DataFrame(list(result_top), columns = result_top.keys())
    print('QUERY_top_done')
    
    QUERY_flop = """
    with base_all as (
    
            SELECT 
                *
            FROM trump_tweets
            ORDER BY commpound_sentiment_score asc
            LIMIT 10)
    
    SELECT 
        date_trunc(hour, created_at) as hour,
        clean_text,
        location,
        commpound_sentiment_score
    FROM base_all
            
            """
        
    result_flop = twitter_db.execute(QUERY_flop)
    df_flop = pd.DataFrame(list(result_flop), columns = result_flop.keys())
    print('QUERY_flop_done')
       
    return df_top, df_flop


app = Flask(__name__)

@app.route('/')
def home():
    df_1 = first_query()
    #df_top, df_flop = top_worst_tweets()
    
    return df_1
#, df_top, df_flop
#'<h1>Hello from Flask this is Helens first Flask App</h1>'

app.run(host='0.0.0.0', debug=True)

