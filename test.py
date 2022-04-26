# https://us.battle.net/login/en/challenge/d613a883-3c69-4b1c-84d8-2038e3a3f8f1/choose?ref=/login/en/account-unlock&app=oauth
import selenium
import pyautogui as pg
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
driver = webdriver.Chrome("chromedriver.exe")
driver.maximize_window()

if __name__ == '__main__':
    print("x")
