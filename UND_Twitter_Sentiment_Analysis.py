# -*- coding: utf-8 -*-
"""
Created on Tue Sep  5 13:03:24 2017

@author: Sam

Stuff that should be added later:
-Do a better job filtering out tweets by university accounts
-Configure it to run on a time interval 
-Find a way to plot sentiment and track it compared to big events such 
as sports games and major university announcements
-It looks like retweets are appearing in the output, which might be okay. It should be ensured 
that retweets are not being double counted
"""

import re
import tweepy 
from tweepy import OAuthHandler
from textblob import TextBlob

class TwitterClient(object):
    '''
    generic class for sentiment analysis of tweets about UND
    '''
    def __init__(self):
        '''
        Class constructor
        '''
        consumer_key = 'HNfIQQzFU2IKtwfQiTVBSWb3g'
        consumer_secret = '8FDWZL3EkVQkkM1xITk49yeZg8VMaNb54kCPNpiDNi5unFhGoN'
        owner_account = 'DataCollectBot' #tied to my @und.edu email
        owner_ID = '905875980224524288'
        access_token = '905875980224524288-Mt2El4Ui4J0dyA1AewM9s2pFIluTVeg'
        access_token_secret = 'wh2gEc8ElyXrR9SmqLZfDHMFRiEgnFLlj1QlYsROiMgF5'
        #authenticating...
        try:
            #creating OAuthHandler
            self.auth = OAuthHandler(consumer_key, consumer_secret)
            #set access token and secret
            self.auth.set_access_token(access_token, access_token_secret)
            #creating tweepy object to get tweets
            self.api = tweepy.API(self.auth)
        except:
            print("Authentication Failed. Sorry buddy")
        
    #def clean_tweet(self, tweet):
        '''
        cleaning text by getting rid of links, special characters and
        regex
        '''
     #   return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])
     #                             |(\w+:\/\/\S+)", " ", tweet).split())
        
    def get_tweet_sentiment(self, tweet):
        '''
        classifying sentiment of tweets passed to this
        function via textblob
        '''
        #creating textblob object for text of passed tweet
        analysis = TextBlob(tweet)
        #set sentiment
        if analysis.sentiment.polarity > 0:
            return 'positive'
        elif analysis.sentiment.polarity == 0:
            return 'neutral'
        else:
            return 'negative'
    
    def get_tweets(self, query, count = 10):
        '''
        main function for getting/parsing tweets
        '''
        tweets = []
        
        try:
            #calling twitter api to fetch tweets
            fetched_tweets = self.api.search(q = query, count = count)
            #parsing tweets individually
            for tweet in fetched_tweets:
                #emptying dict to store reqs params of a tweet
                parsed_tweet = {}
                
                #saving text of tweet
                parsed_tweet['text'] = tweet.text
                parsed_tweet['sentiment'] = self.get_tweet_sentiment(tweet.text)
                
                #appending parsed tweet to list of tweets
                if tweet.retweet_count > 0:
                    #if it's been retweeted make sure it's not double-appended
                    if parsed_tweet not in tweets:
                        tweets.append(parsed_tweet)
                    else:
                        tweets.append(parsed_tweet)
            #returning parsed tweets
            return tweets
        except tweepy.TweepError as e:
            print("Error: " + str(e))
            
    
def main():
   #creating an object of TwitterClient class
   api = TwitterClient()
   #getting tweets
   tweets = api.get_tweets(query = 'University of North Dakota', count = 200)
   print(tweets)
   
   #picking positive tweets
   ptweets = [tweet for tweet in tweets if tweet['sentiment'] == 'positive']
   #percent of negative tweets
   print("Percentage of tweets that are positive: {} %".format(100*len(ptweets)/len(tweets)))
   #picking negative tweets from tweets
   ntweets = [tweet for tweet in tweets if tweet['sentiment'] == 'negative']
   #percent of negative tweets
   print("Percentage of tweets that are negative: {} %".format(100*len(ntweets)/len(tweets)))
   #percent of neutral tweets
   #print("Percentage of tweets that are neutral: {} %".format(100*len(tweets - ntweets -ptweets)/len(tweets)))
   #printing first 10 positive tweets
   
   '''
   print("/n/nPositive tweets:")
   for tweet in ptweets[:10]:
       print(tweet['text'])  
       #printing first 10 negative tweets
       print("/n/nNegative tweets:")
       for tweet in ntweets[:10]:
           print(tweet['text'])
           '''
   
if __name__ == "__main__":
   #calling main function
   main()


