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

#Fetching the link to the json data
# Path(__file__).parent.absolute() 
current_path = str(Path().absolute())
link_to_data = current_path + "/data/bangkok.json"

#Reading json/csv file with all the data 
with open(link_to_data) as f:
  data_content = json.loads(f.read())
for j in range(len(data_content)):
    sums = 0
    for i in range(1, 101, 1):
        # print(data_content[0]['reviews']['R' + str(i)]['content'])
        # print('\n\n')
        current_review = data_content[j]['reviews']['R' + str(i)]['content']
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
        sums += abs(total)
    print("Final Rating of the hotel: ", round(sums/10, 3))