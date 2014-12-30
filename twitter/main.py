import tweepy
# import oauth2 as oauth
import requests
from bs4 import BeautifulSoup
import re
import json
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

#BrainyQuote quote of the day
print 'Getting BrainyQuote of the day...'
bq_endpoint = 'http://www.brainyquote.com/quotes_of_the_day.html'
bq_req = requests.get(bq_endpoint)
bq_resp = bq_req.text
bq_soup = BeautifulSoup(bq_resp)
bq_text = bq_soup.select('.bqQuoteLink')[0].get_text()
print bq_text

# Wikipedia content generation
print 'Getting Wikipedia content...'
wiki_endpoint = 'http://en.wikipedia.org/wiki/Special:Random'
wiki_req = requests.get(wiki_endpoint)
wiki_resp = wiki_req.text
wiki_soup = BeautifulSoup(wiki_resp)

# # Wiki parsing: opening sentence
# wiki_text = soup.p.get_text()
# wiki_text = re.sub(r'\[.*?\]', '', wiki_text) #remove references and pronunciation
# wiki_text = re.sub(r'\(.*?\)', '', wiki_text) #remove references and pronunciation
# wiki_text = re.sub(r'\s+', ' ', wiki_text)
# print wiki_text

# prepositions = 'aboard|about|above|across|after|against|along|amid|among|anti|around|as|at|before|behind|below|beneath|beside|besides|between|beyond|but|by|concerning|considering|despite|down|during|except|excepting|excluding|following|for|from|in|inside|into|like|minus|near|of|off|on|onto|opposite|outside|over|past|per|plus|regarding|round|save|since|than|through|to|toward|towards|under|underneath|unlike|until|up|upon|versus|via|with|within|without'
# relative_pronouns = 'that|when|which|whichever|whichsoever|who|whoever|whosoever|whom|whomever|whomsoever|whose|whosesoever whatever|whatsoever'
# conjunctions = 'and|but|or|nor|for|yet|so|after|although|as|as if|as long as|as much as|as soon as|as though|because|before|even|even if|even though|if|if only|if when|if then|inasmuch|in order that|just as|lest|now|now since|now that|now when|once|provided|provided that|rather than|since|so that|supposing|than|that|though|til|unless|until|when|whenever|where|whereas|where if|wherever|whether|which|while|who|whoever|why'
# punctuation = '\.\s|\,\s|\;\s|\:\s'
# re_delimiters = re.compile('|'.join([punctuation, prepositions, relative_pronouns, conjunctions]))
# wiki_text_arr = re.split(re_delimiters, wiki_text)

# Wiki parsing: title
wiki_text = wiki_soup.select('#firstHeading')[0].get_text()
# wiki_text = 'Temmins bay, oblivion (hoot), cardinal'
wiki_text = re.sub(r'\s*\(.*?\)', '', wiki_text) # Crash (film)
wiki_text = re.sub(r',.*', '', wiki_text) # Beijing, China
wiki_text = wiki_text.replace('List of', '') # List of Americans
# wiki_text = wiki_text.capitalize()
print wiki_text 

# Tweet params
print 'Sending to Twitter...'
tweet_endpoint = 'https://api.twitter.com/1.1/statuses/update.json'
# tweet_content = '"Today is the greatest day I\'ve ever known" - ' + wiki_text
tweet_content = '"' + bq_text + '" - ' + wiki_text
print tweet_content

# Authorize and post
print 'Authorize and post...'
keys = [line.rstrip('\n') for line in open('keys.txt')]
consumer_key = keys[0]
consumer_secret = keys[1]
access_key = keys[2]
access_secret = keys[3]

# # Using OAuth
# print 'OAuth...'
# consumer = oauth.Consumer(key=consumer_key, secret=consumer_secret)
# access_token = oauth.Token(key=access_key, secret=access_secret)
# client = oauth.Client(consumer, access_token)
# resp, data = client.request(tweet_endpoint, 'POST', tweet_content)
# tr = json.loads(data)
# print tr

# Using tweepy
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_key, access_secret)
api = tweepy.API(auth)
resp = api.update_status(tweet_content)
print resp

