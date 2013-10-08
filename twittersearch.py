#!/usr/bin/python2
import oauthsign
import sys
import urllib
import urllib2
import urlparse
import json

#Fetches JSON from specified url and decodes it,
#raising appropriate exceptions when errors are
#encountered.
def fetch_and_decode(url):
  signedurl = oauthsign.sign_oauth_request(url).to_url() #sign the url with oauthy goodness
  try:
    request = urllib2.urlopen(signedurl) #grab some data
  except urllib2.URLError as detail:
    raise Exception('Could not contact twitter (%s)' % detail) #twitter's not cooperating? or maybe your connection sucks
  try:
    decoded_response = json.loads(request.read()) #press x to json. let's make this json more usable here
  except ValueError:
    raise Exception('Bad data received. Check your tokens.') #bad json? maybe not even json? whatever, have an error
  return decoded_response

#Searches twitter for tweets matching a particular
#query string. An optional count parameter is
#available and will continue to query twitter
#until there are no more tweets matching the query
#or until the count is reached.
def search_tweets(query,count=15):
  baseurl = 'https://api.twitter.com/1.1/search/tweets.json' #here's where the tweets live
  url = baseurl + '?%s' % urllib.urlencode({'q':query, 'lang':'en', 'count':min(count,100)}) #build a query
  search_object = fetch_and_decode(url) #fetch some tweets
  output = search_object['statuses'] #make a tidy little pile of tweets
  for i in range(0,(count-1)/100): #don't have enough tweets? no problem! let's keep going.
    if len(search_object['statuses']) < 100: #twitter ran out of tweets...
      return output
    url = search_object['search_metadata']['next_results'] #where are the next batch of tweets?
    if count%100 > 0 and i == ((count-1)/100)-1: #reduce the count if we don't want 100 more.
      decoded = urlparse.parse_qs(url)
      decoded['count'] = [str(count%100)]
      url = '?' + urllib.urlencode(decoded, 1)
    search_object = fetch_and_decode(baseurl + url) #get them tweets
    output += search_object['statuses'] #toss 'em on the pile
  return output

#Prints provided tweets in a more human-readable format.
def pretty_print_tweets(input):
  for status in input:
    print('@%s - %s' % (status['user']['screen_name'], status['text'])) #print name and tweet
    print('------------------') #a line separator to make multiline tweets easier to read
  print('%d tweets printed.' % len(input)) #print number of tweets printed

if __name__ == "__main__":
  count = 15 #default number of tweets to fetch
  if len(sys.argv) > 1: #did the user supply a query? they better have
    if len(sys.argv) > 2: #did the user supply a count? it's okay if they didn't
      count = int(sys.argv[2]) #yep, let's use that instead of 15
    try:
      pretty_print_tweets(search_tweets(sys.argv[1],count)) #fetch and print some tweets
    except Exception as detail:
      print('Failed to print tweets: %s' % detail) #uh oh.
  else:
    print('No query specified') #c'mon user, I'm not searching for nothing
