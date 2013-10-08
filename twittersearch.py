#!/usr/bin/python2
import oauthsign
import sys
import urllib
import urllib2
import urlparse
import json

def fetch_and_decode(url):
  signedurl = oauthsign.sign_oauth_request(url).to_url()
  try:
    request = urllib2.urlopen(signedurl)
  except urllib2.URLError as detail:
    raise Exception('Could not contact twitter (%s)' % detail)
  try:
    decoded_response = json.loads(request.read())
  except ValueError:
    raise Exception('Bad data received. Check your tokens.')
  return decoded_response

def search_tweets(query,count=10):
  baseurl = 'https://api.twitter.com/1.1/search/tweets.json'
  url = baseurl + '?%s' % urllib.urlencode({'q':query, 'lang':'en', 'count':min(count,100)})
  search_object = fetch_and_decode(url)
  output = search_object['statuses']
  for i in range(0,(count-1)/100):
    if len(search_object['statuses']) < 100:
      return output
    url = search_object['search_metadata']['next_results']
    if count%100 > 0 and i == ((count-1)/100)-1:
      decoded = urlparse.parse_qs(url)
      decoded['count'] = [str(count%100)]
      url = '?' + urllib.urlencode(decoded, 1)
    search_object = fetch_and_decode(baseurl + url)
    output += search_object['statuses']
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
    try:
      pretty_print_tweets(search_tweets(sys.argv[1],count))
    except Exception as detail:
      print('Failed to print tweets: %s' % detail)
  else:
    print('No query specified')
