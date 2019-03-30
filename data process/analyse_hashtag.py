import json
import csv
import re


class HashtagCounter:
    
    def __init__(self, time_interval = 20*60):
        self.total_tweet_count = 0
        self.emoji_tweet_count = {}
        # self.emoji_appear_count = {} # not in use
        self.hashtag_count = {}
        self.output = {}
        self.hashtag_list = []
        self.time_interval = time_interval
        self.hashtag_time = {}
        self.hashtag_emoji_time = {}
        self.time_bins = []
        self.hashtag_emoji_count = {}

    def countHashtag(self, hashtags):
        for hashtag in hashtags:
            hashtag_text = hashtag["text"]
            if hashtag_text not in self.hashtag_count:
                self.hashtag_count[hashtag_text] = 0
            self.hashtag_count[hashtag_text] += 1

    def countOverTime(self, hashtags, text, timestamp_ms):

        emojis = re.findall(emoji_pattern, tweetJson["text"])
        time_bin = int(timestamp_ms) // 1000 // self.time_interval
        if time_bin not in self.time_bins:
            self.time_bins.append(time_bin)

        for hashtag in hashtags:
            hashtag = hashtag["text"]
            if hashtag not in self.hashtag_time:
                self.hashtag_time[hashtag] = {}
                self.hashtag_emoji_time[hashtag] = {}
                self.hashtag_emoji_count[hashtag] = {}

            if time_bin not in self.hashtag_time[hashtag]:
                self.hashtag_time[hashtag][time_bin] = 0
            self.hashtag_time[hashtag][time_bin] += 1

            for emoji in set(emojis):
                if emoji not in self.hashtag_emoji_time[hashtag]:
                    self.hashtag_emoji_time[hashtag][emoji] = {}
                    self.hashtag_emoji_count[hashtag][emoji] = 0
                if time_bin not in self.hashtag_emoji_time[hashtag][emoji]:
                    self.hashtag_emoji_time[hashtag][emoji][time_bin] = 0
                self.hashtag_emoji_time[hashtag][emoji][time_bin] += 1
                self.hashtag_emoji_count[hashtag][emoji] += 1

    def selectHashtags(self, keep = 20):
        self.hashtag_list = list(self.hashtag_count)
        self.hashtag_list.sort(key = lambda x : self.hashtag_count[x], reverse = True)
        self.hashtag_list = self.hashtag_list[0:keep]

    def outputFormat(self):
        output = {}
        

        hashtag_time = {}
        for hashtag in self.hashtag_list:
            hashtag_time[hashtag] = []
            for time_bin in self.time_bins:
                entity = {}
                entity["time"] = time_bin*1000*self.time_interval
                if time_bin not in self.hashtag_time[hashtag]:
                    entity["count"] = 0
                else:
                    entity["count"] = self.hashtag_time[hashtag][time_bin]
                hashtag_time[hashtag].append(entity)
        output["hashtag_time"] = hashtag_time

        hashtag_emoji_time = {}
        for hashtag in self.hashtag_list:
            hashtag_emoji_time[hashtag] = {}
            for emoji in self.hashtag_emoji_time[hashtag]:
                hashtag_emoji_time[hashtag][emoji] = []
                for time_bin in self.time_bins:
                    entity = {}
                    entity["time"] = time_bin*1000*self.time_interval
                    if time_bin not in self.hashtag_emoji_time[hashtag][emoji]:
                        entity["count"] = 0
                        entity["proportion"] = 0
                    else:
                        entity["count"] = self.hashtag_emoji_time[hashtag][emoji][time_bin]
                        entity["proportion"] = entity["count"]/self.hashtag_time[hashtag][time_bin]
                    hashtag_emoji_time[hashtag][emoji].append(entity)
        output["hashtag_emoji_time"] = hashtag_emoji_time

        hashtag_emoji_count = {}
        for hashtag in self.hashtag_list:
            hashtag_emoji_count[hashtag] = []
            for emoji in self.hashtag_emoji_count[hashtag]:
                entity = {}
                entity["emoji"] = emoji
                entity["count"] = self.hashtag_emoji_count[hashtag][emoji]
                hashtag_emoji_count[hashtag].append(entity)
        output["hashtag_emoji_count"] = hashtag_emoji_count

        hashtags = []
        for hashtag in self.hashtag_list:
            entity = {}
            entity["hashtag"] = hashtag
            entity["count"] = self.hashtag_count[hashtag]
            hashtags.append(entity)
        output["hashtags"] = hashtags


        self.output = output

        return output

if __name__ == '__main__':
    states = {}
    hashtags = {}
    emoji_pattern = "[\U0001F300-\U0001F64F]"
    emoji_to_keep = 10 #keep how many emojis per source
    counter = HashtagCounter(time_interval = 30*60) #10 mins

    # count statistics
    for i in range(0, 25):
        with open("hashtag\\filter_hashtag_{}.txt".format(i), 'r') as f:
            line = f.readline()
            while line:

                tweetJson = json.loads(line)

                counter.countHashtag(tweetJson["hashtags"])
                counter.countOverTime(tweetJson["hashtags"], tweetJson["text"], tweetJson["timestamp_ms"])


                line = f.readline()
    counter.selectHashtags(20)
    counter.outputFormat()
    with open("hashtag.json", 'w', encoding='utf-8') as f:
        f.write(json.dumps(counter.output, ensure_ascii=False, indent = 4)) 

    # with open("result.csv", 'w', encoding = 'utf-8') as f:
    #     writer = csv.writer(f)
    #     writer.writerow(["emoji", "amount"])
    #     for emoji in emojis:
    #         writer.writerow([emoji, emojis[emoji]])