#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 13 12:36:03 2018

@author: shailesh
"""
import re
import tweepy
from tweepy import OAuthHandler
from textblob import TextBlob


class TwitterClient(object):
    'generic twitter class for sentiment analysis'
    def __init__(self):
        'class constructor or initialization method'
        # keys and tokens from the twitter dev console
        consumer_key = ''
        consumer_secret =''
        access_token = ''
        access_token_secret = ''
        
        # attempt authemtication
        try:
            # create OAuthHandler object
            self.auth = OAuthHandler(consumer_key, consumer_secret)
            #set access token and secret
            self.auth.set_access_token(access_token, access_token_secret)
            # create tweepy API object to fetch tweets
            self.api = tweepy.API(self.auth)
        except:
            print('Error: Authentication Failed')
    
    # clean tweets
    """ def clean_tweet(self,tweet):
        print('hello world')
        print(word_tokenize(tweet[0]))
        #return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())
    """                                
    # sentiment analysis
    def get_tweet_sentiment(self, tweet):
        analysis = TextBlob(tweet)
        if analysis.sentiment.polarity > 0:
            return 'positive'
        elif analysis.sentiment.polarity == 0:
            return 'neutral'
        else:
            return 'negative'
    
    def get_tweets(self, query, count = 10):
          # empty list to store parsed tweets
            tweets = []
            try:
                # call twitter api to fetch tweets
                fetched_tweets = self.api.search(q = query, count = count)
    
                # parsing tweets one by one
                for tweet in fetched_tweets:
                    # empty dictionary to store required params of a tweet
                    parsed_tweet = {}
    
                    # saving text of tweet
                    parsed_tweet['text'] = tweet.text
                    # saving sentiment of tweet
                    parsed_tweet['sentiment'] = self.get_tweet_sentiment(tweet.text)
    
                    # appending parsed tweet to tweets list
                    if tweet.retweet_count > 0:
                        # if tweet has retweets, ensure that it is appended only once
                        if parsed_tweet not in tweets:
                            tweets.append(parsed_tweet)
                    else:
                        tweets.append(parsed_tweet)
    
                # return parsed tweets
                return tweets
    
            except tweepy.TweepError as e:
                # print error (if any)
                print("Error : " + str(e))
           
            
def main():
     # creating object of TwitterClient Class
    api = TwitterClient()
    # calling function to get tweets
    tweets = api.get_tweets(query = 'Donald Trump', count = 200)
    #c_tweets = api.clean_tweet(tweets)
    print(tweets)
    
    #calculate percentage of positive, negative and neutral tweets
    # positive
    ptweets = [tweet for tweet in tweets if tweet['sentiment'] == 'positive']
    
    # calculate positive tweets percentage
    print('Positive Tweets {}'.format((100*len(ptweets)/len(tweets))))
    #negative tweets
    ntweets = [tweet for tweet in tweets if tweet['sentiment'] == 'negative']
    print('Negative Tweets {}'.format((100*len(ntweets)/len(tweets))))
    # neutral tweets
    #print('Neutral Tweets {}'.format(100*len(tweets - ptweets - ntweets)/len(tweets)))
    print('Neutral Tweets {}'.format(100*(len(tweets)-(len(ptweets)+len(ntweets)))/len(tweets)))
if __name__ == "__main__":
    # calling a main function
    main()
        
        
