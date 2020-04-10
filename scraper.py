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

# Prepare webdriver
# @returns Firefox webdriver
def prepare_driver():
    driver = webdriver.Firefox()
    driver.get("https://booking.com")
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
    print('Hotels list found, search is beginning..')


if __name__ == "__main__":
    """ Explicit Waits for selenium webdriver """
    # take location input to fetch hotel reviews
    location = input('Enter location: ')
    try:
        driver = prepare_driver()
        search_hotels(driver, location)
    finally:
        driver.quit()
