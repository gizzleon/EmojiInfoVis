
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import mannwhitneyu
import json
import csv
import re



if __name__ == '__main__':
    count = 0
    states = {}
    sources = {}
    source_pattern = r">(.+)<"
    emoji_pattern = "[\U0001F300-\U0001F64F]"
    emoji_to_keep = 10 #keep how many emojis per source

    # count statistics
    with open('US\\filter_us_0.txt', 'r') as f:
        line = f.readline()
        while line:

            tweetJson = json.loads(line)

            # print(tweetJson["place"])
            # print(tweetJson["source"])
            # print(re.findall(pattern, tweetJson["source"])[0])

            source = re.findall(source_pattern, tweetJson["source"])[0]
            tweetJson["source"] = source

            if source not in sources:
                sources[source] = {}
                # sources[source] = []

            emojis = re.findall(emoji_pattern, tweetJson["text"])
            
            for emoji in emojis:
                if emoji not in sources[source]:
                    sources[source][emoji] = 0
                sources[source][emoji] += 1

            


            # state = tweetJson["place"]["state"]
            # if state not in states:
            #     states[state] = {}
            #     states[state]["total"] = 0

            # state = states[state]


            # for emoji in tweetJson["emojis"]:
            #     state["total"] += 1
            #     if emoji in state:
            #         state[emoji] += 1
            #     else:
            #         state[emoji] = 1
            line = f.readline()
            count += 1
            # print(count)
    print(count)
    #output formatting
    output = {}
    for source in sources:
        output[source] = []
        for emoji in sources[source]:
            entity = {}
            entity["letter"] = emoji
            entity["frequency"] = sources[source][emoji]
            output[source].append(entity)
            # count += entity["frequency"]
        # print(source, count)
        
        #sort
        # output[source].sort(key = lambda x: x["frequency"], reverse = True)
        
        # only keep certain number of emojis
        # count_abandoned = 0
        # if len(output[source]) < emoji_to_keep:
        #     continue
        # threshold = output[source][emoji_to_keep - 1]["frequency"] #last emoji to keep
        # for entity in output[source][:]:
        #     if entity["frequency"] < threshold:
        #         count_abandoned += entity["frequency"]
        #         # print(count)
        #         output[source].remove(entity)
        # output[source].append({"letter":"other", "frequency":count_abandoned})


    with open("source.json", 'w', encoding='utf-8') as f:
        f.write(json.dumps(output, ensure_ascii=True, indent = 4)) 

    # with open("result.csv", 'w', encoding = 'utf-8') as f:
    #     writer = csv.writer(f)
    #     writer.writerow(["emoji", "amount"])
    #     for emoji in emojis:
    #         writer.writerow([emoji, emojis[emoji]])