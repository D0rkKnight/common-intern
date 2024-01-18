from selenium import webdriver 
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service

service = Service('./drivers/chromedriver.exe')
driver = webdriver.Chrome(service=service)

