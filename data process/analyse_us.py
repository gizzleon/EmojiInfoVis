
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import mannwhitneyu
import json
import csv
import re

us_state_abbrev = { #https://gist.github.com/rogerallen/1583593
    'Alabama': 'AL',
    'Alaska': 'AK',
    'Arizona': 'AZ',
    'Arkansas': 'AR',
    'California': 'CA',
    'Colorado': 'CO',
    'Connecticut': 'CT',
    'Delaware': 'DE',
    'Florida': 'FL',
    'Georgia': 'GA',
    'Hawaii': 'HI',
    'Idaho': 'ID',
    'Illinois': 'IL',
    'Indiana': 'IN',
    'Iowa': 'IA',
    'Kansas': 'KS',
    'Kentucky': 'KY',
    'Louisiana': 'LA',
    'Maine': 'ME',
    'Maryland': 'MD',
    'Massachusetts': 'MA',
    'Michigan': 'MI',
    'Minnesota': 'MN',
    'Mississippi': 'MS',
    'Missouri': 'MO',
    'Montana': 'MT',
    'Nebraska': 'NE',
    'Nevada': 'NV',
    'New Hampshire': 'NH',
    'New Jersey': 'NJ',
    'New Mexico': 'NM',
    'New York': 'NY',
    'North Carolina': 'NC',
    'North Dakota': 'ND',
    'Ohio': 'OH',
    'Oklahoma': 'OK',
    'Oregon': 'OR',
    'Pennsylvania': 'PA',
    'Rhode Island': 'RI',
    'South Carolina': 'SC',
    'South Dakota': 'SD',
    'Tennessee': 'TN',
    'Texas': 'TX',
    'Utah': 'UT',
    'Vermont': 'VT',
    'Virginia': 'VA',
    'Washington': 'WA',
    'West Virginia': 'WV',
    'Wisconsin': 'WI',
    'Wyoming': 'WY',
}

def centerOfBoundingbox(coordinate1, coordinate2):
    lag1 = coordinate1[0]
    lng1 = coordinate1[1]
    lag2 = coordinate2[0]
    lng2 = coordinate2[1]
    return [(lag1+lag2)/2, (lng1+lng2)/2]

if __name__ == '__main__':
    count = 0
    states = {}
    sources = {}
    pattern = r">(.+)<"
    emoji_pattern = "[\U0001F300-\U0001F64F]"

    # count statistics
    with open('US\\filter_us_0.txt', 'r') as f:
        line = f.readline()
        while line:

            tweetJson = json.loads(line)

            # print(tweetJson["place"])
            # print(tweetJson["source"])
            # print(re.findall(pattern, tweetJson["source"])[0])

            source = re.findall(pattern, tweetJson["source"])[0]
            tweetJson["source"] = source

            

            # sources[source].append(tweetJson["coordinate"]) 

            if tweetJson["place"]["place_type"] == "city":
                tweetJson["place"]["state"] = tweetJson["place"]["full_name"][-2:]
            elif tweetJson["place"]["place_type"] == "admin" and tweetJson["place"]["name"] in us_state_abbrev:

                tweetJson["place"]["state"] = us_state_abbrev[tweetJson["place"]["name"]]
            else:
                line = f.readline()
                continue

            if tweetJson["place"]["state"] == 'SA':
                line = f.readline()
                continue
            state = tweetJson["place"]["state"]

            # handle source here
            # if source not in sources:
            #     sources[source] = {}
            # if state not in sources[source]:
            #     sources[source][state] = 0
            # sources[source][state] += 1

            if state not in states:
                states[state] = {}
                # states[state]["total"] = 0

            state = states[state]
            
            emojis = re.findall(emoji_pattern, tweetJson["text"])
            for emoji in emojis:
                # state["total"] += 1
                if emoji in state:
                    state[emoji] += 1
                else:
                    state[emoji] = 1
            line = f.readline()
            # print(count)

    #output formatting
    output = {}

    # for source in sources:
    #     output[source] = []
    #     for state in sources[source]:
    #         entity = {}
    #         entity["state"] = state
    #         entity["count"] = sources[source][state]
    #         output[source].append(entity)

    for state in states:
        output[state] = []
        for emoji in states[state]:
            entity = {}
            entity["letter"] = emoji
            entity["frequency"] = states[state][emoji]
            output[state].append(entity)


    with open("us.json", 'w', encoding='utf-8') as f:
        f.write(json.dumps(output, ensure_ascii=True, indent = 4)) 

    # with open("result.csv", 'w', encoding = 'utf-8') as f:
    #     writer = csv.writer(f)
    #     writer.writerow(["emoji", "amount"])
    #     for emoji in emojis:
    #         writer.writerow([emoji, emojis[emoji]])