import selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import Firefox
import requests
import bs4 as BeautifulSoup
import json
import re
import string
import time
import platform
from collections import defaultdict

# Prepare webdriver
# @returns Firefox webdriver
def prepare_driver(target):
    driver = webdriver.Firefox()
    driver.get(target)
    element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "ss")))
    return driver

# Funtion to search for a list of hotels in a specific area
def search_hotels(driver, location):
    """ Finds the sb-searchbox__input class and fills it with the location and search """
    # Finds the input field and fill it
    input_search_field = driver.find_element_by_xpath("//*[@id='ss']")
    input_search_field.send_keys(location)

    # Finds the search button and clicks it
    input_submit_button = driver.find_element_by_class_name("sb-searchbox__button")
    input_submit_button.click()

    # Wait until search is complete
    element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "sr_property_block_main_row")))
    print('Hotels list found, search is beginning...')

# Function to scrap hotels details
def scrap_hotels(driver, max_count):
    """ Fetch details of each hotels from the list of hotels """
    # Initialise empty lists for hotels data and urls
    hotels_urls = list()
    hotels_data = list()


    # Loop over the class name to find multiple elements in that page
    # @returns List of urls
    for hotel in driver.find_elements_by_class_name('sr-hotel__title'):
        url = hotel.find_element_by_class_name("hotel_name_link").get_attribute("href")
        hotels_urls.append(url)
    time.sleep(5)

    # If count of hotels required is more than available in a single page, open the next page
    # and append the details of hotels url to the list
    check = 1
    while(check == True):
        # Initial counter to check to limit scrapingof hotels in a single page
        counter = max_count - len(hotels_urls)
        if max_count > len(hotels_urls):
            # Find the Next page button button and click it
            driver.find_element_by_class_name('paging-next').click()
            time.sleep(3)
            # Looping over and appending the hotels to the list hotels_url <= max_xount
            for hotel in driver.find_elements_by_class_name('sr-hotel__title'):
                if counter <= 0:
                    check = -1
                    break
                else:
                    counter -= 1
                    new_url = hotel.find_element_by_class_name("hotel_name_link").get_attribute("href")
                    hotels_urls.append(new_url)
        else:
            check = -1
    print(len(hotels_urls), "Hotel URL's scrapped successfully!")

    break_counter = 0
    # Once urls are fetched, loop over and fetch details of each hotel with that specific url
    for i in range(0, len(hotels_urls), 1):
        print('Scraping details of Hotel: ', i)
        url_data = scrape_hotel_details(driver, hotels_urls[i])
        # Check if we received any data for the url, and append it to the hotels_data list
        if url_data != 0:
            hotels_data.append(url_data)
            break_counter += 1

        else:
            print("No data received for the given url")

        if break_counter == 20:
            break

    # Return the final hotels data list items
    return hotels_data


# Function to fetch Hotel details; reviews, name, location
def scrape_hotel_details(driver, hotel_url):
    """ Opens a hotel page, and scraps the data """

    # If driver is null, fetch new web driver value
    if driver == None:
        driver = prepare_driver(hotel_url)
    driver.get(hotel_url)
    time.sleep(5)

    try:
        # Initialise a details dictionary
        hotel_details = dict()

        # Fetch the name of the hotel
        hotel_details['name'] = driver.find_element_by_class_name('hp__hotel-name').text

        # Fetch the location of the hotel
        try:
            hotel_details['location'] = driver.find_element_by_class_name('hp_address_subtitle').text
        except:
            hotel_details['location'] = ''

        # Fetch hotel ratings

        # try:
        #     hotel_details['rating'] = driver.find_element_by_class_name('bui-review-score__badge').text
        # except:
        #     try:
        #         hotel_details['rating'] = driver.find_element_by_class_name('bui-review-score--end').find_element_by_class_name('bui-review-score__badge').text
        #     except:
        #         hotel_details['rating'] = ""

        # Fetch hotel ratings breakdown list
        hotel_details['breakdown_list'] = dict()

        # Get new webdriver link
        new_link = hotel_url[:len(hotel_url) - 44]
        new_url = new_link + "#tab-reviews"
        # print(new_url)
        driver.get(new_url)
        time.sleep(10)

        # Looping over the hotel hotel_ratings list to append each list item
        for rating in driver.find_elements_by_class_name('c-score-bar'):
            hotel_details['breakdown_list'][rating.find_element_by_class_name('c-score-bar__title').text] = rating.find_element_by_class_name('c-score-bar__score').text


        try:
            hotel_details['rating'] = driver.find_element_by_class_name('reviews_panel_header_score').find_element_by_class_name('review-score-widget').find_element_by_class_name('review-score-badge').text
        except:
            hotel_details['rating'] = ""

        # Fetch reviewer comments
        final = get_hotel_reviews(driver, 100)

        # Append the comments to the list
        hotel_details['comments'] = final
        # print(hotel_details)
        return hotel_details

    except:
        return 0

# Function to scrap hotel reviews details
def get_hotel_reviews(driver, max_review_count):
    """ Fetch hotel review comments, date of review and reviewer's score """

    # List with all the reviews details dictionaries to return
    reviews_list = list()

    # Counter element
    check = 1

    # Loop over each list item, create a dictionary of details and append it to the list
    for review in driver.find_elements_by_class_name('review_list_new_item_block'):
        # Initialise the reviews comment dictionary with reviews details
        reviews_dict = dict()
        counter = max_review_count - len(reviews_list)

        if max_review_count:
            j = 0
            # Fetch reviewer's name
            try:
                reviews_dict['name'] = review.find_element_by_class_name('bui-avatar-block__title').text
            except:
                reviews_dict['name'] = ""

            # Fetch reviewer's date of posting review
            try:
                temp_date = review.find_element_by_class_name('c-review-block__date').text
                reviews_dict['date'] = temp_date[10:]
            except:
                reviews_dict['date'] = ""

            # Fetch reviewer's score given
            try:
                reviews_dict['score'] = review.find_element_by_class_name('bui-review-score__badge').text
            except:
                reviews_dict['score'] = ""

            # Fetch reviewers comment
            reviews_dict['comments'] = review.find_element_by_class_name('c-review-block__title').text

            reviews_list.append(reviews_dict)


    while(check == True):
        counter = max_review_count - len(reviews_list)

        if max_review_count > len(reviews_list):
            # Find the next page button and click it
            driver.find_element_by_class_name('pagenext').click()
            time.sleep(3)

            # Loop over each list item, create a dictionary of details and append it to the list
            for review in driver.find_elements_by_class_name('review_list_new_item_block'):
                # Initialise reviews details dictionory
                reviews_dict = dict()
                counter = max_review_count - len(reviews_list)

                if counter <= 0:
                    check = -1
                    break

                else:
                    # Decrement the counter value
                    counter -= 1
                    # Fetch reviewer's name
                    try:
                        reviews_dict['name'] = review.find_element_by_class_name('bui-avatar-block__title').text
                    except:
                        reviews_dict['name'] = ""

                    # Fetch reviewer's date of posting review
                    try:
                        temp_date = review.find_element_by_class_name('c-review-block__date').text
                        reviews_dict['date'] = temp_date[10:]
                    except:
                        reviews_dict['date'] = ""

                    # Fetch reviewer's score given
                    try:
                        reviews_dict['score'] = review.find_element_by_class_name('bui-review-score__badge').text
                    except:
                        reviews_dict['score'] = ""

                    # Fetch reviewers comment
                    reviews_dict['comments'] = review.find_element_by_class_name('c-review-block__title').text
                    reviews_list.append(reviews_dict)
        else:
            check = -1

    # Return the final list
    # print(len(reviews_list))
    return reviews_list


if __name__ == '__main__':
    # take location input to fetch hotel reviews
    location = input('Enter location: ')
    # amount = int(input('Enter the number of hotels to be searched: '))
    try:
        pf = platform.system()
        # Set the initial target path
        target = "https://booking.com"
        # Set up webdriver
        driver = prepare_driver(target)
        # Call the function to search for hotels list's
        search_hotels(driver, location)
        # Call the function to scrape the details of the above fetched hotels
        final_hotels_data = scrap_hotels(driver, 200)
        final_hotels_data = json.dumps(final_hotels_data, indent=4)
        print(final_hotels_data)
        # Store the values in a file
        with open('hotel3.json', 'w') as f:
            f.write(final_hotels_data)
    finally:
        driver.quit()
