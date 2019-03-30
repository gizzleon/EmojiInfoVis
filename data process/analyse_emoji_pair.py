import json
import csv
import re
import math

class EmojiCounter:
    
    def __init__(self):
        self.total_tweet_count = 0
        self.emoji_tweet_count = {}
        # self.emoji_appear_count = {} # not in use
        self.emoji_pair_count = {}
        self.emoji_pair_PMI = {} #p(x,y)/(p(x)p(y)) no log
        self.output = {}
        self.selected_emoji_list = []

    def countEmoji(self, emoji_1, emoji_2 = None):
        if emoji_1 not in self.emoji_tweet_count:
            self.emoji_tweet_count[emoji_1] = 0
        self.emoji_tweet_count[emoji_1] += 1

        if emoji_2 == None:
            return
        # emoji_2 not None
        if emoji_2 != emoji_1:
            if emoji_2 not in self.emoji_tweet_count:
                self.emoji_tweet_count[emoji_2] = 0
            self.emoji_tweet_count[emoji_2] += 1

        # each pair only show once
        if emoji_1+emoji_2 in self.emoji_pair_count:
            self.emoji_pair_count[emoji_1+emoji_2] += 1
        elif emoji_2+emoji_1 in self.emoji_pair_count:
            self.emoji_pair_count[emoji_2+emoji_1] += 1
        else:
            self.emoji_pair_count[emoji_1+emoji_2] = 1

    def countEmojiList(self, emojis):
        if len(emojis) <= 0:
            return 
        self.total_tweet_count += 1
        if len(emojis) == 1:
            self.countEmoji(emojis[0])
            return

        #eliminate repeated emojis
        emojis_set = list(set(emojis))

        # count the repeate one
        if len(emojis_set) < len(emojis):
            for emoji in emojis_set:
                if emojis.count(emoji) > 1:
                    self.countEmoji(emoji, emoji)
        # count the different pair
        for emoji_1 in emojis_set[:]:
            emojis_set.remove(emoji_1)
            for emoji_2 in emojis_set:
                self.countEmoji(emoji_1, emoji_2)
    
    def generatePMI(self):
        self.emoji_pair_PMI = {}
        for emoji_pair in self.emoji_pair_count:
            emoji_1 = emoji_pair[0]
            emoji_2 = emoji_pair[1]
            # probability of emoji_1 & emoji_2
            p_1 = self.emoji_tweet_count[emoji_1] / self.total_tweet_count
            p_2 = self.emoji_tweet_count[emoji_2] / self.total_tweet_count
            p_1_2 = self.emoji_pair_count[emoji_pair] / self.total_tweet_count
            self.emoji_pair_PMI[emoji_pair] = round(math.log2(p_1_2 / (p_1*p_2)), 2)  # what about P_1&2/(P_1|2)
            # self.emoji_pair_PMI[emoji_pair] = max(0, self.emoji_pair_PMI[emoji_pair])
            # self.emoji_pair_PMI[emoji_pair] = round(p_1_2 / (p_1*p_2), 3)  # what about P_1&2/(P_1|2)

    def mostFrequentlyUsedEmojis(self, emoji_number = -1):
        all_emojis = list(self.emoji_tweet_count)
        if emoji_number >= len(all_emojis) or emoji_number < 0:
            self.selected_emoji_list = all_emojis
        else:
            all_emojis.sort(key = lambda x: self.emoji_tweet_count[x], reverse=True)
            self.selected_emoji_list = all_emojis[0:emoji_number]
        return self.selected_emoji_list

    def emojiPairInList(self, emoji_pair, emoji_list):
        if emoji_pair[0] in emoji_list and emoji_pair[1] in emoji_list:
            return True
        return False 

    def outputFormat(self):
        output = {}
        emoji_pair_data = []
        for emoji1 in self.selected_emoji_list:
            for emoji2 in self.selected_emoji_list:
                data = {}
                data["emoji_1"] = emoji1
                data["emoji_2"] = emoji2
                if emoji1+emoji2 in self.emoji_pair_count:
                    data["count"] = self.emoji_pair_count[emoji1+emoji2]
                    data["PMI"] = self.emoji_pair_PMI[emoji1+emoji2]
                elif emoji2+emoji1 in self.emoji_pair_count:
                    data["count"] = self.emoji_pair_count[emoji2+emoji1]
                    data["PMI"] = self.emoji_pair_PMI[emoji2+emoji1]
                else:
                    data["count"] = 0
                    data["PMI"] = float('-inf')
                emoji_pair_data.append(data.copy())
                #dulplicate
                (data["emoji_1"], data["emoji_2"]) = (data["emoji_2"], data["emoji_1"])
                emoji_pair_data.append(data)
    
        emoji_pair_data.sort(key = lambda x: x["PMI"], reverse=True)
        self.output["emoji_pair"] = emoji_pair_data
        self.output["emoji_list"] = self.selected_emoji_list
        return self.output

if __name__ == '__main__':
    emoji_pattern = "[\U0001F300-\U0001F64F]"

    counter = EmojiCounter()

    # count statistics
    for i in range(0,20):
        with open('emoji\\filter_emoji_{}.txt'.format(i), 'r') as f:
            line = f.readline()
            while line:

                tweetJson = json.loads(line)
                emojis = re.findall(emoji_pattern, tweetJson["text"])
                counter.countEmojiList(emojis)
                line = f.readline()

    counter.generatePMI()
    counter.mostFrequentlyUsedEmojis(25)

    #output formatting
    output = counter.outputFormat()

    with open("emoji_pair.json", 'w', encoding='utf-8') as f:
        f.write(json.dumps(output, ensure_ascii=False, indent = 4)) 

    # with open("result.csv", 'w', encoding = 'utf-8') as f:
    #     writer = csv.writer(f)
    #     writer.writerow(["emoji", "amount"])
    #     for emoji in emojis:
    #         writer.writerow([emoji, emojis[emoji]])