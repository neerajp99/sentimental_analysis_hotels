from collections import defaultdict, Counter
import json
import string
from pathlib import Path
import os
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import pandas as pd
import numpy as np
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import statistics
import csv


#Fetching the link to the json data
# Path(__file__).parent.absolute()
current_path = str(Path().absolute())
link_to_data = current_path + "/data/singapore.json"

# Final and initial score array
checkout_array = list()
checkout_hotel_details_array = list()

#Reading json/csv file with all the data
with open(link_to_data) as f:
	data_content = json.loads(f.read())
for j in range(len(data_content)):
    sums = 0
    temp_list = list()
    for k in data_content[j]['reviews']:
        # print(data_content[0]['reviews']['R' + str(i)]['content'])
        # print('\n\n')
        current_review = data_content[j]['reviews'][k]['content']
        # Convert any uppercase letter to lowercase
        current_review = current_review.lower()
        # Remove any special character from the review comments
        review_comments = current_review.translate(str.maketrans('', '', string.punctuation))
        # Create tokenize words
        tokenized_reviews = word_tokenize(review_comments, "english")
        #Removing the stop words from the comments
        final_review_comments = list()
        # Loop over the tokenized reviews, and append the non stop words
        for word in tokenized_reviews:
            if word not in stopwords.words('english'):
                final_review_comments.append(word)
        # Function to count the sentiments of the given reviews for the hotel
        def analyse_sentiment(sentiment_text):
            score = SentimentIntensityAnalyzer().polarity_scores(sentiment_text)
            negative = score['neg']
            positive = score['pos']
            neutral = score['neu']
            compound = score['compound']
            # print(score)
            return compound

        total = analyse_sentiment(review_comments)
        # print(abs(total))
        # sums += abs(total)
        # Append the compound
        temp_list.append(abs(total))

    # print(temp_list)
    # print(data_content[j]['score'])
    # print(statistics.median(temp_list) * 10)
    checkout_array.append([float(data_content[j]['score']), statistics.median(temp_list) * 10])
    checkout_hotel_details_array.append([ statistics.median(temp_list) * 10, data_content[j]['name'], data_content[j]['location']])

    # print("Final Rating of the hotel: ", sums/len(data_content[j]['reviews']))
print( checkout_hotel_details_array)
print('\n\n')
checkout_hotel_details_array.sort()
print(checkout_hotel_details_array)

# Saving the top 10 hotels data to json
kuala_lumpur_hotel_final = json.dumps(checkout_hotel_details_array[: 10], indent = 4)
with open ('singapore_details.json', 'w') as f:
    f.write(kuala_lumpur_hotel_final)
# Saving the top 10 hotels data to csv
with open('singapore_details.csv', 'w', newline='') as myfile:
    header_names = ["V1", "V2"]
    wr = csv.writer(myfile)
    wr.writerows(checkout_hotel_details_array[: 10])

# Saving the polarity score data to a json file
bangkok_final = json.dumps(checkout_array, indent = 4)
with open ('kuala_lumpur.json', 'w') as f:
    f.write(bangkok_final)
# Saving the polarity score data to a csv file
with open('kuala_lumpur.csv', 'w', newline='') as myfile:
    header_names = ["V1", "V2"]
    wr = csv.writer(myfile)
    wr.writerows(checkout_array)

# data = np.array(checkout_array)
# np.savetxt("bangkok_final.csv", data, delimiter=",")
