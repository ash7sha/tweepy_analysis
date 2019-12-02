import re

from tweepy import API, OAuthHandler
from tweepy import Cursor

from ash7sha_Twitter import twitter_credentials
from ash7sha_Twitter.tweepy_streamer import TwitterAuthenticator
from textblob import TextBlob

import numpy as np
import pandas as pd


class TwitterClient():

    def __init__(self, twitter_user=None):
        TA = TwitterAuthenticator()
        self.auth = TA.twitter_authenticate()
        self.twitter_client = API(self.auth)
        self.twitter_user = twitter_user

    def get_twitter_client_api(self):
        return self.twitter_client

    def get_user_timeline_tweets(self, num_tweets):
        tweets = []
        for tweet in Cursor(self.twitter_client.user_timeline, id=self.twitter_user).items(num_tweets):
            tweets.append(tweet)
            return tweets


class TweetAnalyzer():
    """
    This class is responsible for analyzing all the tweets, creating dataframes as per the column required from tweets.
    Later this data will be persisted in chosen DB, to-do for me.
    """

    def tweets_to_data_frames(self, tweets):

        df = pd.DataFrame(data=[tweet.text for tweet in tweets], columns=['TText'])
        df['id'] = np.array([tweet.id for tweet in tweets])
        df['len'] = np.array([len(tweet.text) for tweet in tweets])
        df['date'] = np.array([tweet.created_at for tweet in tweets])
        df['source'] = np.array([tweet.source for tweet in tweets])
        df['likes'] = np.array([tweet.favorite_count for tweet in tweets])
        df['retweets'] = np.array([tweet.retweet_count for tweet in tweets])
        return df

    def clean_tweets(self, tweet):
        """This will cleanse the tweet text, remove any emojis text """
        if(tweet):
            text = tweet.encode('ascii', 'ignore').decode('ascii')
            return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())
        else:
            return None

    def analyze_sentiment(self, tweet):
        analysis = TextBlob(self.clean_tweets(tweet))

        if analysis.sentiment.polarity > 0:
            return 1
        elif analysis.sentiment.polarity == 0:
            return 0
        else:
            return -1

if __name__ == '__main__':
    twitter_client = TwitterClient()
    api = twitter_client.get_twitter_client_api()

    tweets = api.user_timeline(screen_name='mfuloria', count='200')
    tweets_analyzer = TweetAnalyzer()
    #df = tweets_analyzer.tweets_to_data_frames(tweets)
    #print(df.head(10))
    #print(dir(tweets[0]))
    # print(tweets_analyzer.tweets_to_data_frames(tweets))
    df = tweets_analyzer.tweets_to_data_frames(tweets)
    df['sentiment'] = np.array([tweets_analyzer.analyze_sentiment(tweet) for tweet in df['TText']])

    print(df.head(100))
