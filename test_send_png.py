import tweepy

# Authorize and post
keys = [line.rstrip('\n') for line in open('keys.txt')]
consumer_key = keys[0]
consumer_secret = keys[1]
access_key = keys[2]
access_secret = keys[3]

# Using tweepy
tweet_endpoint = 'https://api.twitter.com/1.1/statuses/update.json'
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_key, access_secret)
api = tweepy.API(auth)
resp = api.update_with_media('test_macaroni.png', status='testing tweepylypng macarooni')
print resp


'''
use this:
lilypond --png -dbackend=eps test_macaroni.ly
to create the png
'''