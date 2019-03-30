from __future__ import absolute_import, print_function



from tweepy.streaming import StreamListener

from tweepy import OAuthHandler

from tweepy import Stream

import time

import json

import re

from us_abbr import us_state_abbrev #https://gist.github.com/rogerallen/1583593


# your token here
consumer_key=""

consumer_secret=""


access_token=""

access_token_secret=""



class FileOutListener(StreamListener):

    def __init__(self, ):
        super().__init__()
        self.tweetCount = 0
        self.file = None
        self.startTime = 0
        self.runningTime = 0
        self.emoji_pattern = None
        self.tweetCount_ca = 0
        self.tweetCount_nv = 0
        self.output = []
        self.buffer_us = []
        self.count_us = 0
        self.buffer_emojis = []
        self.count_emojis = 0
        self.buffer_hashtags = []
        self.count_hashtags = 0
        self.buffer_size = 500
        self.tweets_per_file = 10000
        self.stop = False
    
    def on_data(self, data):

        # self.file.write(data)
        # process the data
        tweetJson = json.loads(data)

        if "delete" in tweetJson:
            return True
        self.tweetCount += 1

        #filter - in us
        if tweetJson["place"] != None and tweetJson["place"]["country_code"] == "US":
            customTweetJson = formatData(tweetJson) #customized json format for smaller size
            customTweetData = json.dumps(customTweetJson)+'\n' #in "str" type
            self.buffer_us.append(customTweetData)
            self.count_us += 1
            if self.bufferToFile(self.buffer_us, self.count_us, "filter_us", 50) == True:
                self.buffer_us = []
        #filter - contains emojis
        emojis = re.findall(self.emoji_pattern, tweetJson["text"])
        if len(emojis) != 0:
            customTweetJson = formatData(tweetJson) #customized json format for smaller size
            customTweetData = json.dumps(customTweetJson)+'\n' #in "str" type
            self.buffer_emojis.append(customTweetData)
            self.count_emojis += 1
            if self.bufferToFile(self.buffer_emojis, self.count_emojis, "filter_emoji", 1000) == True:
                self.buffer_emojis = []
        #filter - contains hashtags
        hashtags = tweetJson["entities"]["hashtags"]
        if len(hashtags) != 0:
            customTweetJson = formatData(tweetJson) #customized json format for smaller size
            customTweetData = json.dumps(customTweetJson)+'\n' #in "str" type
            self.buffer_hashtags.append(customTweetData)
            self.count_hashtags += 1
            if self.bufferToFile(self.buffer_hashtags, self.count_hashtags, "filter_hashtag", 1000) == True:
                self.buffer_hashtags = []
            print("emoji: %d, us: %d, hashtags: %d" % (self.count_emojis, self.count_us, self.count_hashtags))
        
        #stop condition
        if self.count_us >= 100000:
            self.stop = True
            self.bufferToFile(self.buffer_us, self.count_us, "filter_us", ignore_buffer_size = True)
            self.bufferToFile(self.buffer_emojis, self.count_emojis, "filter_emoji", ignore_buffer_size = True)
            self.bufferToFile(self.buffer_hashtags, self.count_hashtags, "filter_hashtag", ignore_buffer_size = True)
            return False
        
        return True


    def on_error(self, status):
        print(status)
        print("error")

    def bufferToFile(self, buffer, count, fileNameInit, buffer_size = 500, ignore_buffer_size = False):
        if len(buffer) >= buffer_size or ignore_buffer_size == True:
            fileName = "{}_{}.txt".format(fileNameInit, count//self.tweets_per_file)
            with open(fileName, "a") as f:
                for tweet in buffer:
                    f.write(tweet)
            return True
        return False

def formatData(tweetJson):
    outTweetJson = {}
    outTweetJson["id"] = tweetJson["id"]
    outTweetJson["place"] = tweetJson["place"]
    # outTweetJson["place"]["state"] = tweetJson["place"]["full_name"][-2:] #us only
    outTweetJson["geo"] = tweetJson["geo"]
    outTweetJson["lang"] = tweetJson["lang"]
    outTweetJson["text"] = tweetJson["text"]
    outTweetJson["hashtags"] = tweetJson["entities"]["hashtags"]
    outTweetJson["mentioned_users"] = tweetJson["entities"]["user_mentions"]
    outTweetJson["timestamp_ms"] = tweetJson["timestamp_ms"]
    outTweetJson["source"] = tweetJson["source"]

    userJson = tweetJson["user"]
    outTweetJson["user"] = {}
    outTweetJson["user"]["name"] = userJson["name"]
    outTweetJson["user"]["screen_name"] = userJson["screen_name"]
    outTweetJson["user"]["location"] = userJson["location"]
    outTweetJson["user"]["lang"] = userJson["lang"]
    return outTweetJson


if __name__ == '__main__':

    l = FileOutListener()

    auth = OAuthHandler(consumer_key, consumer_secret)

    auth.set_access_token(access_token, access_token_secret)

    #time
    l.startTime = time.time()
    l.runningTime = 1*60 # 2 hours
    print(time.asctime())

    #pattern
    l.emoji_pattern = "[\U0001F300-\U0001F64F]"

    stream = Stream(auth, l)

    while l.stop == False:
        try:
            stream.sample()
        except Exception as ex:
            print(ex)
            print('error')