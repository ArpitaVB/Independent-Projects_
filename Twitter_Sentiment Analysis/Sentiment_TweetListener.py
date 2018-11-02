import tweepy
import socket
import json
from tweepy import OAuthHandler
from tweepy import Stream
from tweepy.streaming import StreamListener
from afinn import Afinn

consumer_key='c0Vq5CO8jWx2Zs0qjLomWjiT4'
consumer_secret='ViiNIcfmmohx1wUSukbXyLw2RwwaMVWdOZ9k7bJAQrtHJYZT04'
access_token ='780368384810639360-9IpTgcFdSKxub5w90LT7gZNiEo2edjK'
access_secret='uZsq22cL48pvWIsFuDw8CbP16rLsgJQWtiChfHV4sfmt4'

class TweetListener(StreamListener):

    def __init__(self, con_socket):
             self.client_socket = con_socket

    def on_data(self, data):
	
        try:
            tweet_jdata = json.loads(data)
            score = afinn.score(tweet_jdata['text'])            
            final_text = " " + score_to_sentiment(score) + " " + tweet_jdata['text']			
            print(tweet_jdata['text'],":",score_to_sentiment(score))
            self.client_socket.send(final_text.encode('utf-8'))            
            return True
        
        except BaseException as e:
              print("Error on_data: %s" % str(e))
        return True

    def on_error(self, status):
        print("on_error", status)
        return True

def score_to_sentiment(score):
    try:
        if score <= -5: return "VERY_NEGATIVE"
        elif (score < 0 and score > -5): return "NEGATIVE"
        elif score == 0: return "NEUTRAL"
        elif score >0 and score <= 5: return "POSITIVE"
        else: return "VERY_POSITIVE"
    
    except TypeError:
        return "NEUTRAL"


if __name__ == "__main__":   
        
    soc = socket.socket()        
    host = "127.0.0.1"    
    port = 6666                
    soc.bind((host, port))
    print("Listening on port: %s" % str(port))

    soc.listen(10)                
    con_socket, ip_socket = soc.accept()
    print("Sending to: %s" % str(ip_socket))

    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_secret)
    
    afinn = Afinn()
    twitter_stream = Stream(auth, TweetListener(con_socket))
    twitter_stream.filter(languages=['en'], track=['BigData'])

