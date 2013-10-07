import oauth2
import sys
import time
import settings

# Build an oauth-signed request using the supplied url 
# Use .to_url() on the return value to get an URL that will authenticate against the 
# Twitter API. Build your URL, then call this function to get the URL that you will 
# send to Twitter. 
def sign_oauth_request(url):
  # Set up consumer and token objects.
  consumer = oauth2.Consumer(key=settings.CONSUMERKEY, 
    secret=settings.CONSUMERSECRET) 
  token = oauth2.Token(key=settings.ACCESSTOKEN, 
    secret=settings.ACCESSTOKENSECRET) 
 
  # Set up oauth parameters 
  params = {} 
  params['oauth_version'] = '1.0' 
  params['oauth_nonce'] = oauth2.generate_nonce() 
  params['oauth_timestamp'] = int(time.time()) 
  params['oauth_token'] = token.key
  params['oauth_consumer_key'] = consumer.key 
 
  # Create and sign the request. 
  request = oauth2.Request(method='GET', url=url, parameters=params) 
  request.sign_request(oauth2.SignatureMethod_HMAC_SHA1(), consumer, token) 
  return request

if __name__ == "__main__":
  print(sign_oauth_request(sys.argv[1]).to_url())
