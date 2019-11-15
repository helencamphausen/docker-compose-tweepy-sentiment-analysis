# Project-Data-Pipeline

The main goal of this project was to try out a docker-compose pipeline combined with an ETL process.

The pipeline|ETL process works as followed:

1) Collecting tweets via tweepy 
2) Loading tweets into MongoDB
3) Extracting data from MongoDB and running a sentiment analysis with vaderSentiment
4) Loading data into postgresdb
5) Writing a flask app to show my dataframe outputs as html
