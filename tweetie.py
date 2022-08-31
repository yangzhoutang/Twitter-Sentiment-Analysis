import sys
import tweepy
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import json


def loadkeys(filename):
    """"
    load twitter api keys/tokens from CSV file with form
    consumer_key, consumer_secret, access_token, access_token_secret
    """
    with open(filename) as f:
        items = f.readline().strip().split(', ')
        return items


def authenticate(twitter_auth_filename):
    """
    Given a file name containing the Twitter keys and tokens,
    create and return a tweepy API object.
    """
    fouritems=loadkeys(twitter_auth_filename)
    consumer_key=fouritems[0]
    consumer_secret=fouritems[1]
    access_token=fouritems[2]
    access_token_secret=fouritems[3]
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth, wait_on_rate_limit=True)
    return api
    


def fetch_tweets(api, name):
    """
    Given a tweepy API object and the screen name of the Twitter user,
    create a list of tweets where each tweet is a dictionary with the
    following keys:

       id: tweet ID
       created: tweet creation date
       retweeted: number of retweets
       text: text of the tweet
       hashtags: list of hashtags mentioned in the tweet
       urls: list of URLs mentioned in the tweet
       mentions: list of screen names mentioned in the tweet
       score: the "compound" polarity score from vader's polarity_scores()

    Return a dictionary containing keys-value pairs:

       user: user's screen name
       count: number of tweets
       tweets: list of tweets, each tweet is a dictionary

    For efficiency, create a single Vader SentimentIntensityAnalyzer()
    per call to this function, not per tweet.
    """
    status_list = api.user_timeline(screen_name=name,count=100)
    sid = SentimentIntensityAnalyzer()
    returndict={}
    tweetlst=[]
    for status in status_list:
        tweetdict={'mentions':[]}
        json_str = json.dumps(status._json)
        json_dict=json.loads(json_str)
        tweetdict['created_at']=json_dict['created_at']
        tweetdict['id']=json_dict['id']
        tweetdict['retweeted']=json_dict['retweet_count']
        tweetdict['text']=json_dict['text']
        tweetdict['hashtags']=json_dict['entities']['hashtags']
        tweetdict['urls']=json_dict['entities']['urls']
        mentionlst=[]
        for i in json_dict['entities']['user_mentions']:
            mentionlst.append(i['screen_name'])
        tweetdict['mentions'].append(mentionlst)
        tweetdict['score']=sid.polarity_scores(json_dict['text'])['compound']
        tweetlst.append(tweetdict)
    returndict['user']=name
    returndict['tweets']=tweetlst
    returndict['count']=len(tweetlst)
    return tweetlst[:100]


def fetch_following(api,name):
    """
    Given a tweepy API object and the screen name of the Twitter user,
    return a a list of dictionaries containing the followed user info
    with keys-value pairs:

       name: real name
       screen_name: Twitter screen name
       followers: number of followers
       created: created date (no time info)
       image: the URL of the profile's image

    To collect data: get the list of User objects back from friends();
    get a maximum of 100 results. Pull the appropriate values from
    the User objects and put them into a dictionary for each friend.
    """
    all_follower=[]
    for i in api.get_friends(screen_name=name, count=100):
        each_follower={}
        timestring=''
        json_str = json.dumps(i._json)
        json_dict=json.loads(json_str)
        each_follower['name']=json_dict['name']
        each_follower['screen_name']=json_dict['screen_name']
        each_follower['followers']=json_dict['followers_count']
        timelist=json_dict['created_at'].split(' ')
        if timelist[1]=='Jan':
            timelist[1]='01'
        if timelist[1]=='Feb':
            timelist[1]='02'
        if timelist[1]=='Mar':
            timelist[1]='03'
        if timelist[1]=='Apr':
            timelist[1]='04'
        if timelist[1]=='May':
            timelist[1]='05'
        if timelist[1]=='Jun':
            timelist[1]='06'
        if timelist[1]=='Jul':
            timelist[1]='07'
        if timelist[1]=='Aug':
            timelist[1]='08'
        if timelist[1]=='Sep':
            timelist[1]='09'
        if timelist[1]=='Oct':
            timelist[1]='10'
        if timelist[1]=='Nov':
            timelist[1]='11'
        if timelist[1]=='Dec':
            timelist[1]='12'
        timestring=timelist[5]+'-'+timelist[1]+'-'+timelist[2]        
        each_follower['created']=timestring
        each_follower['image']=json_dict['profile_image_url']
        all_follower.append(each_follower)
    return all_follower
    
