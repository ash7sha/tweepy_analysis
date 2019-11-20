from tweepy import OAuthHandler
from tweepy import Stream
from tweepy.streaming import StreamListener

import twitter_credentials


# Twitter authenticator class ###

class TwitterAuthenticator():

    def twitter_authenticate(self):
        auth = OAuthHandler(twitter_credentials.CONSUMER_KEY, twitter_credentials.CONSUMER_KEY_SECRET)
        auth.set_access_token(twitter_credentials.ACCESS_TOKEN, twitter_credentials.ACCESS_TOKEN_SECRET)
        return auth


class TwitterStreamer():
    '''
    This class processes stream of tweets based on hash tag list, authentication of tweeter
    app is also happening here, for now!
    '''
    def __init__(self):
        self.twitter_auth = TwitterAuthenticator

    def stream_tweets(self, fetched_tweets_file, hash_tag_list):
        listener = StdOutListener(fetched_tweets_file)
        auth = self.twitter_auth.twitter_authenticate(self)
        stream = Stream(auth, listener)
        stream.filter(track=hash_tag_list)


class StdOutListener(StreamListener):
    '''
    This class is standard listener class, this has on-data and on-error even handlers for handling the tweets
    '''

    def __int__(self, fetched_tweets_file):
        self.fetched_tweets_file = fetched_tweets_file

    def on_data(self, data):
        try:
            with open(fetched_tweets_file, 'a') as tf:
                tf.write(data)
        except BaseException as e:
            print("Error..", e)
        return True

    def on_error(self, status):
        print(status)


if __name__ == '__main__':
    hash_tag_list = ['DelhiAirQuality', 'DelhiAirPollution', 'DelhiNCRPollution', 'delhipollution']
    fetched_tweets_file = 'tweets.json'

    twitter_streamer = TwitterStreamer()
    twitter_streamer.stream_tweets(hash_tag_list, fetched_tweets_file)
