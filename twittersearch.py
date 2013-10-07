#!/usr/bin/python2
import oauthsign
import sys
import urllib
import urllib2
import urlparse
import json

def search_tweets(query,count=10):
  url = 'https://api.twitter.com/1.1/search/tweets.json?%s' % urllib.urlencode({'q':query, 'lang':'en', 'count':min(count,100)})
  signedurl = oauthsign.sign_oauth_request(url).to_url()
  try:
    request = urllib2.urlopen(signedurl)
  except urllib2.URLError:
    print('Could not contact twitter.')
    return []
  try:
    decoded_response = json.loads(request.read())
  except ValueError:
    print('Bad data received. Check your tokens.')
    return []
  output = decoded_response['statuses']
  for i in range(0,(count-1)/100):
    url = decoded_response['search_metadata']['next_results']
    if (i == ((count-1)/100)-1):
      decoded = urlparse.parse_qs(url)
      decoded['count'] = [str(count%100)]
      url = '?' + urllib.urlencode(decoded, 1)
    url = 'https://api.twitter.com/1.1/search/tweets.json' + url
    signedurl = oauthsign.sign_oauth_request(url).to_url()
    try:
      request = urllib2.urlopen(signedurl)
    except urllib2.URLError:
      print('Could not retrieve all tweets.')
      return output
    try:
      decoded_response = json.loads(request.read())
    except ValueError:
      print('Bad data received.')
      return output
    output += decoded_response['statuses']
  return output

def pretty_print_tweets(input):
  for status in input:
    print('@%s - %s' % (status['user']['screen_name'], status['text']))
    print('------------------')
  print('%d tweets printed.' % len(input))

if __name__ == "__main__":
  count = 15
  if len(sys.argv) > 1:
    if len(sys.argv) > 2:
      count = int(sys.argv[2])
    pretty_print_tweets(search_tweets(sys.argv[1],count))
  else:
    print('No query specified')
