import twitter
import oauth2 as oauth
import cgi
import urllib

class TwitterUtility:
  def __init__(self, consumer_key,consumer_secret,request_token_url,authenticate_url,access_token_url):
    self.request_token_url = request_token_url
    self.authenticate_url = authenticate_url
    self.access_token_url = access_token_url
    self.consumer = oauth.Consumer(key=consumer_key, secret=consumer_secret)
    self.api = None
    self.request_token = None
    self.access_token = None
    
    
  def get_request_token(self,callback_url):
    if self.request_token is None:
      client = oauth.Client(self.consumer)  
      resp, content = client.request(self.request_token_url, 'POST',body=urllib.urlencode({'oauth_callback':callback_url}))
      if resp['status'] != '200':
        raise Exception("Invalid response %s." % resp['status'])
        return None,None
      request_token = dict(cgi.parse_qsl(content))
      self.request_token = request_token

    url ='%s?oauth_token=%s' % (self.authenticate_url,  self.request_token['oauth_token'])
    return url, self.request_token
    
  
  def get_access_token(self,oauth_token,oauth_verifier):
    if self.access_token is None:
      token = oauth.Token(oauth_token, oauth_verifier)
      client = oauth.Client(self.consumer, token)
      resp, content = client.request(self.access_token_url, "POST", body="oauth_verifier=%s" % oauth_verifier)
      if resp['status'] != '200':
        raise Exception("Invalid response %s." % resp['status'])
        return None
      self.access_token = dict(cgi.parse_qsl(content))
    
    return self.access_token

  def get_api(self,request_token,access_token):
    if self.api is None:
      self.request_token = request_token
      self.access_token = access_token
      self.api = twitter.Api(base_url="https://api.twitter.com/1.1",
                  consumer_key=self.consumer.key,
                  consumer_secret=self.consumer.secret, 
                  access_token_key=self.access_token['oauth_token'], 
                  access_token_secret=self.access_token['oauth_token_secret']) 

    return self.api