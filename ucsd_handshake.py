# selenium stup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.service import Service

# to find links
from bs4 import BeautifulSoup
import json
import urllib.request
import re

import time # to sleep
import yaml
import os

def main():
    # Retrieve secrets from secrets.yaml
    with open('secrets.yaml') as f:
        secrets = yaml.load(f, Loader=yaml.FullLoader)
        
    service = Service('./drivers/chromedriver.exe')
    driver = webdriver.Chrome(service=service)
    
    driver.set_window_size(1920, 1080)

    driver.get('https://ucsd.joinhandshake.com/stu/postings?page=1&per_page=25&sort_direction=desc&sort_column=default&job.job_types%5B%5D=3')

    # Get SSO button by sso-button class
    sso_button = driver.find_element(By.CLASS_NAME, 'sso-button')

    # Click SSO button
    sso_button.click()
    print("Logging in...")
    
    # Log into tritonlink
    sso_login(driver, secrets)
    
    # Get style cards
    style_cards = get_style_cards(driver)
    
    jobnames = [card.get_attribute('aria-label') for card in style_cards]
    print(jobnames)
    
    for i in range(len(style_cards)):
        card = get_style_cards(driver)[i] # Refresh card list
        card.click()
        
        time.sleep(1)
        print(driver.current_url)
        
        process_card(driver)
        time.sleep(1)
    
    print("Done!")

def get_style_cards(driver):
    return driver.find_elements(By.CLASS_NAME, 'style__card___\+\+2p5')

def process_card(driver):
    
    # Get apply button by data-hook
    apply_button = driver.find_element(By.XPATH, "//button[@data-hook='apply-button']")
    apply_button_label = apply_button.get_attribute('aria-label')
    
    # Only apply if the button is not external
    if apply_button_label == 'Apply':
        apply_button.click()
        time.sleep(1)
        
        # Get apply modal from datahook
        apply_modal = driver.find_element(By.XPATH, "//div[@data-hook='apply-modal']")
        
        # Find button that says "Upload New"
        upload_resume_input = apply_modal.find_element(By.XPATH, "//input[@name='s3-upload-input']")
        upload_resume_input.send_keys(os.getcwd()+"/resume.pdf")
        
        print("Applied!")
        
        # upload_resume_button = apply_modal.find_element_by_xpath("//button[contains(text(), 'Upload New')]")
        # upload_resume_button.click()
    
    
    pass

# Tritonlink login
def sso_login(driver, secrets):
    username=driver.find_element(By.ID, 'ssousername')
    password=driver.find_element(By.ID, 'ssopassword')

    username.send_keys(secrets['ucsd_username'])
    password.send_keys(secrets['ucsd_password'])

    login_button = driver.find_element(By.CLASS_NAME, 'sso-button')
    login_button.click()
    
    # DUO
    # Wait until url is no longer a5.ucsd.edu
    while True:
        try:
            WebDriverWait(driver, 1).until(EC.url_contains("a5.ucsd.edu"))
        except TimeoutException:
            break

    return True

if __name__ == '__main__':
    main()