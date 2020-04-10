import selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import Firefox
import requests
import bs4
import json
import re
import string
import time

target = "https://booking.com"
# Prepare webdriver
# @returns Firefox webdriver
def prepare_driver():
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

    for hotel in driver.find_elements_by_class_name('sr-hotel__title'):
        url = hotel.find_element_by_class_name("hotel_name_link").get_attribute("href")
        hotels_urls.append(url)
    print(hotels_urls)


if __name__ == '__main__':
    # take location input to fetch hotel reviews
    location = input('Enter location: ')
    try:
        driver = prepare_driver()
        search_hotels(driver, location)
        scrap_hotels(driver, 20)
    finally:
        driver.quit()
