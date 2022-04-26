# Author: @nas4547
# Overwatch 2 Beta Signup

import selenium
import pyautogui as pg
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

emailCount = 0
passwordCount = 0
listEmails = []
listPasswords = []
listSQ = []
averageTime = []
credentials = {}
emailsWithKeys = {}
counter = 0
driver = webdriver.Chrome("chromedriver.exe")


def readEmails():
    with open('emails.txt', 'r') as e:
        global emailCount
        global listEmails
        temp = e.readlines()
        for email in temp:
            time.sleep(0.03)
            emailCount += 1
            listEmails.append(str.strip(email))
        e.close()


def readPasswords():
    with open('passwords.txt', 'r') as p:
        global passwordCount
        global listPasswords
        temp = p.readlines()
        for password in temp:
            time.sleep(0.03)
            passwordCount += 1
            listPasswords.append(str.strip(password))
        p.close()


def readSQ():
    with open('secret.txt', 'r') as a:
        global listSQ
        temp = a.readlines()
        for answer in temp:
            time.sleep(0.03)
            listSQ.append(str.strip(answer))


def convert():
    global credentials
    global emailsWithKeys
    for e in listEmails:
        for p in listPasswords:
            credentials[e] = p
            listPasswords.remove(p)
            break
    for x in listEmails:
        for a in listSQ:
            emailsWithKeys[x] = a
            listSQ.remove(a)
            break


def runScript():
    print("Running script")
    driver.maximize_window()
    totalTime = 0
    for email in credentials:
        start = time.time()
        login(email, credentials[email])
        end = time.time()
        print("(" + str(round(end-start, 2)) + "s) " + "Successfully signed up Account #" + str(counter) + " with email " + str(email))
        averageTime.append(end-start)

        # Writing account details to file
        registered = open('registered.txt', 'a')
        registered.write(str(email) + " | " + str(credentials[email]) + "\n")
    for x in averageTime:
        totalTime += x
    print("Script complete!\n\tAverage completion time: " + str(round(x/emailCount)) + "s\n\tAccounts registered: " + str(emailCount))


def login(email, password):
    driver.get("https://playoverwatch.com/en-us/beta/")
    time.sleep(1)
    global counter
    try:
        # Click the login button on the opt-in page.
        loginButton = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "/html/body/nav[2]/div[2]/div[2]/div/a[1]"))).click()

        # Enter the email on the log-in page.
        emailField = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, "/html/body/div/div/div/div[2]/div/form/div[1]/div[2]/div/input")))
        emailField.clear()
        emailField.send_keys(str(email))

        # Enter the password on the log-in page.
        passwordField = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, "/html/body/div/div/div/div[2]/div/form/div[1]/div[3]/div/div/input")))
        passwordField.clear()
        passwordField.send_keys(str(password))

        # Continue to log-in
        loginButton2 = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "/html/body/div/div/div/div[2]/div/form/div[2]/button"))).click()

        ##############################################################################
        # THE SCRIPT MAY GET TRIPPED UP BY CAPTCHA AT THIS STAGE                     #
        # THE FOLLOWING BLOCK IS IMPLEMENTED TO ANSWER A SECURITY QUESTION IF NEEDED #
        ##############################################################################
        time.sleep(2)
        if "Security Check" in driver.page_source:
            toggle = WebDriverWait(driver, 10).until(EC.element_to_be_clickable(
                (By.XPATH, "/html/body/div/div/div/div/form/div[1]/div/div/div/span[2]"))).click()
            secretQuestion = WebDriverWait(driver, 10).until(EC.presence_of_element_located(
                (By.XPATH, "/html/body/div/div/div/div/form/div[1]/div/div/div/div/div[2]"))).click()
            submit = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "/html/body/div/div/div/div/form/div[2]/button"))).click()
            answer = WebDriverWait(driver, 10).until(EC.element_to_be_clickable(
                (By.XPATH, "/html/body/div/div/div/div/div/form/div[1]/div/div/input"))).send_keys(
                str(emailsWithKeys[email]))
            time.sleep(11)
            submitCaptcha = WebDriverWait(driver, 1).until(EC.presence_of_element_located((By.XPATH, "/html/body/div/div/div/div/div/form/div[3]/button"))).click()

            # Captcha / security question should be solved by now.
            time.sleep(4)
            pg.click(346, 681)  # clicks the orange opt-in button
            time.sleep(2)
            pg.click(950, 574)  # clicks the blue sign up button
            counter += 1
            driver.get("https://playoverwatch.com/logout")
            time.sleep(1.5)
        else:
            time.sleep(4)
            pg.click(346, 681)  # clicks the orange opt-in button
            time.sleep(2)
            pg.click(950, 574)  # clicks the blue sign up button
            counter += 1
            driver.get("https://playoverwatch.com/logout")
            time.sleep(1.5)
    except NoSuchElementException:
        print("Element not found")


if __name__ == '__main__':
    print("=====================================")
    print("=  Overwatch 2 Beta Sign-up Script  =")
    print("=              nas4547              =")
    print("=====================================")
    print("Attempting to read login credentials from file...")
    readEmails()
    readPasswords()
    readSQ()
    if emailCount != passwordCount or emailCount == 0:
        print("Could not read login credentials! Check emails.txt and passwords.txt")
        driver.close()
        quit()
    else:
        print("Successfully read " + str(emailCount) + " email/password combinations.")
        convert()
        time.sleep(1);
        runScript()
