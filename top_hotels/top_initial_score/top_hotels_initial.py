import json
import string
from pathlib import Path
import os
import pandas as pd
import statistics
import csv

#Fetching the link to the json data
# Path(__file__).parent.absolute()
current_path = str(Path().absolute())
link_to_data = current_path + "link to the file"

# Final and initial score array
checkout_hotel_initial_details_array = list()

#Reading json/csv file with all the data
with open(link_to_data) as f:
	data_content = json.loads(f.read())
for i in range(len(data_content)):
    checkout_hotel_initial_details_array.append([data_content[i]['score'], data_content[i]['name'], data_content[i]['location']])


print( checkout_hotel_initial_details_array)
print('\n\n')
checkout_hotel_initial_details_array.sort()
print(checkout_hotel_initial_details_array)

# Saving the top 10 hotels data to json
singapore_hotel_final = json.dumps(checkout_hotel_initial_details_array[: 10], indent = 4)
with open ('singapore_initial_details.json', 'w') as f:
    f.write(kuala_lumpur_hotel_final)
# Saving the top 10 hotels data to csv
with open('singapore_initial_details.csv', 'w', newline='') as myfile:
    header_names = ["V1", "V2"]
    wr = csv.writer(myfile)
    wr.writerows(checkout_hotel_initial_details_array[: 10])
