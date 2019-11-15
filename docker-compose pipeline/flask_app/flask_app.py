#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 15 10:49:00 2019

@author: hcamphausen
"""

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
            with foo as (
                SELECT
                date_trunc('hour', created_at) as date_created,
                text,
                commpound_sentiment_score,
                CASE when commpound_sentiment_score>=0.05 then 1 else 0 end as positive_flag
                from trump_tweets_excl_dup)

                SELECT
                distinct date_created,
                count(text) as total_unique_tweets,
                avg(commpound_sentiment_score) as average_score
                FROM foo
                GROUP BY 1
                ORDER BY 1 asc
            """

    result_1 = twitter_db.execute(QUERY_1)
    df_1 = pd.DataFrame(list(result_1), columns = result_1.keys())
    print('first_query_done')
    return df_1

def top_worst_tweets():

    QUERY_top = """
        with base_all as (

            SELECT
                distinct trump_tweets_excl_dup.clean_text,
                created_at,
                location,
                commpound_sentiment_score
            FROM trump_tweets_excl_dup
            ORDER BY commpound_sentiment_score desc
            limit 10
            )

            SELECT
                date_trunc('hour', created_at) as created_hour,
                clean_text,
                location,
                commpound_sentiment_score
            FROM base_all

            """

    result_top = twitter_db.execute(QUERY_top)
    df_top = pd.DataFrame(list(result_top), columns = result_top.keys())
    html_top = df_top.to_html()
    dict_top = df_top.to_dict('dict')
    print('QUERY_top_done')

    QUERY_flop = """
       with base_all as (

            SELECT
                distinct trump_tweets_excl_dup.clean_text,
                created_at,
                location,
                commpound_sentiment_score
            FROM trump_tweets_excl_dup
            ORDER BY commpound_sentiment_score asc
            limit 10
            )

            SELECT
                date_trunc('hour', created_at) as created_hour,
                clean_text,
                location,
                commpound_sentiment_score
            FROM base_all

            """

    result_flop = twitter_db.execute(QUERY_flop)
    df_flop = pd.DataFrame(list(result_flop), columns = result_flop.keys())
    html_flop = df_flop.to_html()
    dict_flop = df_flop.to_dict('dict')
    print('QUERY_flop_done')

    html_total = html_top + html_flop
    return html_total
#html_top, html_flop
#dict_top, dict_flop,
#df_top, df_flop


app = Flask(__name__)

@app.route('/')
def home():
    #df_1 = first_query()
    html_total = top_worst_tweets()

    return html_total
#html_top, html_flop
#, df_top, df_flop
#'<h1>Hello from Flask this is Helens first Flask App</h1>'

app.run(host='0.0.0.0', debug=True)
