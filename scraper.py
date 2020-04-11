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

target = "https://booking.com"
# Prepare webdriver
# @returns Firefox webdriver
def prepare_driver(pf):

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

    # Once urls are fetched, loop over and fetch details of each hotel with that specific url
    for i in range(0, len(hotels_urls), 1):
        url_data = scrape_hotel_details(driver, hotels_urls[i])
        # Check if we received any data for the url, and append it to the hotels_data list
        if len(url_data) != 0:
            hotels_data.append(url_data)
        else:
            print("No data received for the given url")

    # Return the final hotels data list items
    return hotels_data


# Function to fetch Hotel details; reviews, name, location
def scrape_hotel_details(driver, hotel_url):
    """ Opens a hotel page, and scraps the data """
    return [1,2]



if __name__ == '__main__':
    # take location input to fetch hotel reviews
    location = input('Enter location: ')
    try:
        pf = platform.system()
        driver = prepare_driver(pf)
        search_hotels(driver, location)
        scrap_hotels(driver, 70)
    finally:
        driver.quit()
