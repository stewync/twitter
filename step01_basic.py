# -*- coding: utf-8 -*-
"""
Created on Wed Mar 22 21:51:45 2017

#Reference/Source: Prof. Gene Lee's codes from Dropbox code files.

"""
##Reference/Source: Prof. Gene Lee's codes from Dropbox code files.


from twython import TwythonStreamer
import sys
import json

tweets = []

class MyStreamer(TwythonStreamer):
    '''our own subclass of TwythonStremer'''

    # overriding
    def on_success(self, data):
        if 'lang' in data and data['lang'] == 'en':
            if "trump" in data['text'].lower():  #EDIT
                tweets.append(data['text'])
                print 'Received tweet #', len(tweets), data['text']

        if len(tweets) >= 10000:
            self.store_json()
            self.disconnect()

    # overriding
    def on_error(self, status_code, data):
        print status_code, data
        self.disconnect()

    def store_json(self):
        with open('tweet_stream_{}_{}.json'.format(keyword, len(tweets)), 'w') as f:
            json.dump(tweets, f, indent=4)


if __name__ == '__main__':

    with open('caston_credentials_twitter.json', 'r') as f:
        credentials = json.load(f)

    # create your own app to get consumer key and secret
    CONSUMER_KEY = credentials['CONSUMER_KEY']
    CONSUMER_SECRET = credentials['CONSUMER_SECRET']
    ACCESS_TOKEN = credentials['ACCESS_TOKEN']
    ACCESS_TOKEN_SECRET = credentials['ACCESS_TOKEN_SECRET']

    stream = MyStreamer(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

    if len(sys.argv) > 1:
        keyword = sys.argv[1]
    else:
        keyword = 'trump'

    try: 
        stream.statuses.filter(track=keyword) 
    except:
         stream.store_json()
