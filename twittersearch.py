#!/usr/bin/python2
import oauthsign
import sys
import urllib
import urllib2
import json

def search_tweets(query):
  url = 'https://api.twitter.com/1.1/search/tweets.json?%s' % urllib.urlencode({'q':query, 'lang':'en'})
  signedurl = oauthsign.sign_oauth_request(url).to_url()
  request = urllib2.urlopen(signedurl)
  decoded_response = json.loads(request.read())
  return decoded_response

def pretty_print_tweets(input):
  for status in input['statuses']:
    print('@%s - %s' % (status['user']['screen_name'], status['text']))

if __name__ == "__main__":
  pretty_print_tweets(search_tweets(sys.argv[1]))
