from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import selenium.common.exceptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.common.exceptions import TimeoutException, WebDriverException
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import time
import random
from keep_alive import keep_alive
from instagrapi import Client
import praw
import re
import requests
import os

class CleverBot:
    def __init__(self):
        global cleverBotActive
        cleverBotActive = False
        print("Creating CleverBot...")
        self.element = None
        options = Options()
        options.add_argument("--headless")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--no-sandbox")
        print("Starting Firefox")
        self.wd = webdriver.Firefox(options=options)
        self.wd.set_page_load_timeout(15)
        print("CleverBot Created")
        cleverBotActive = True

    def init(self):
        global cleverBotActive
        cleverBotActive = False
        print("Starting CleverBot....")
        self.wd.get("https://www.cleverbot.com/")
        print("At CleverBot.com")
        self.fastrack = WebDriverWait(self.wd, 1.5).until(
            ec.visibility_of_element_located((By.XPATH, "/html/body/div[1]/div[2]/div[1]/div/div/form/input")))
        self.wd.find_element_by_xpath("/html/body/div[1]/div[2]/div[1]/div/div/form/input").click()
        self.fastrack = WebDriverWait(self.wd, 1.5).until(
            ec.visibility_of_element_located((By.CSS_SELECTOR, "input.stimulus")))
        self.textbox = self.wd.find_element_by_css_selector("input.stimulus")
        cleverBotActive = True
        print("CleverBot is Now Running")

    def getResponse(self, text):
        global cleverBotActive
        self.textbox.send_keys(text)
        self.textbox.submit()
        time.sleep(0.5)
        self.textField = self.wd.find_element_by_css_selector("#line1 > span.bot")
        WebDriverWait(self.wd, 6).until(lambda wd: len(wd.find_element_by_css_selector("#line1 > span.bot").text) > 1)
        time.sleep(3)
        return self.textField.text

    def close(self):
        global cleverBotActive
        cleverBotActive = False
        self.wd.quit()
        print("Bot Shut Down")

    def reset(self):
        global cleverBotActive
        cleverBotActive = False
        self.wd.refresh()
        self.fastrack = WebDriverWait(self.wd, 1.5).until(
            ec.visibility_of_element_located((By.XPATH, "/html/body/div[1]/div[2]/div[1]/div/div/form/input")))
        self.wd.find_element_by_xpath("/html/body/div[1]/div[2]/div[1]/div/div/form/input").click()
        self.fastrack = WebDriverWait(self.wd, 1.5).until(
            ec.visibility_of_element_located((By.CSS_SELECTOR, "input.stimulus")))
        self.textbox = self.wd.find_element_by_css_selector("input.stimulus")
        cleverBotActive = True
        print("Bot Restarted")

cb = CleverBot()

username = '--YOUR USERNAME--'
password = '--YOUR PASSWORD--'


def path():
    global chrome
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    chrome = webdriver.Chrome()


def url_name(url):
    chrome.get(url)

    # adjust sleep if you want
    time.sleep(3)


def login(_username, your_password):
    # finds the username box
    usern = chrome.find_element_by_name("username")
    # sends the entered username
    usern.send_keys(_username)
    # finds the password box
    passw = chrome.find_element_by_name("password")
    # sends the entered password
    passw.send_keys(your_password)
    # press enter after sending password
    passw.send_keys(Keys.RETURN)
    time.sleep(6)
    # Click Not Now For Notifications
    message = chrome.find_element_by_class_name('mt3GC')
    message.click()
    time.sleep(3)
    goToMessages()

def send_message(_user, _message):
    message = chrome.find_elements_by_css_selector("button[class='wpO6b ZQScA']")[0]
    message.click()
    time.sleep(2)
    message = chrome.find_elements_by_name("queryBox")[0]
    message.send_keys(_user)
    message.send_keys(Keys.RETURN)
    time.sleep(5.5)
    message = chrome.find_elements_by_tag_name("button")[4]
    message.click()
    time.sleep(5)
    message = chrome.find_elements_by_tag_name("button")[3]
    message.click()
    time.sleep(5)
    global mbox
    mbox = chrome.find_elements_by_tag_name('textarea')[0]
    mbox.send_keys(_message)
    mbox.send_keys(Keys.RETURN)


def chatWithCleverBot():
    global receivedMessages
    receivedMessages = chrome.find_elements_by_css_selector("div[class='   CMoMH     _8_yLp  ']")
    cb.init()
    new_message = receivedMessages[len(receivedMessages) - 1].find_element_by_tag_name("div")
    new_message = new_message.find_element_by_tag_name("div")
    new_message = new_message.find_element_by_tag_name("div")
    new_message = new_message.find_element_by_tag_name("span")
    new_message_str = new_message.text
    mbox = chrome.find_elements_by_tag_name('textarea')[0]
    if new_message_str.lower().find("end") != -1:
        goToMessages()
        return
    response = cb.getResponse(new_message_str)
    mbox.send_keys(response)
    mbox.send_keys(Keys.RETURN)
    _range = 200
    for i in range(_range):
        oldReceivedMessages = receivedMessages
        receivedMessages = chrome.find_elements_by_css_selector("div[class='   CMoMH     _8_yLp  ']")
        # mbox.send_keys(len(receivedMessages))
        # mbox.send_keys(Keys.RETURN)
        if (len(oldReceivedMessages) < len(receivedMessages)):
            i = _range
            new_message = receivedMessages[len(receivedMessages) - 1].find_element_by_tag_name("div")
            new_message = new_message.find_element_by_tag_name("div")
            new_message = new_message.find_element_by_tag_name("div")
            new_message = new_message.find_element_by_tag_name("span")
            new_message_str = new_message.text
            if new_message_str.lower().find("end") != -1:
                goToMessages()
                break
            response = cb.getResponse(new_message_str)
            mbox.send_keys(response)
            mbox.send_keys(Keys.RETURN)
        time.sleep(0.1)


def goToMessages():
    # Clicks the messages button
    message = chrome.find_element_by_class_name('xWeGp')
    message.click()
    time.sleep(5)
    chrome.refresh()
    time.sleep(5)


def count():
    for x in range(60):
        mbox.send_keys(x)
        mbox.send_keys(Keys.RETURN)
        time.sleep(1)


def spam():
    l = ['u suck', 'gay', 'lesbian cock', 'penis', 'u uglyyy']
    for x in range(10000):
        mbox.send_keys(random.choice(l))
        mbox.send_keys(Keys.RETURN)
        time.sleep(0.2)


def BeeMovieScriptSpam():
    fileObj = open("Bee Movie Script.txt", "r")
    words = fileObj.read().splitlines()
    fileObj.close()
    for i in range(len(words) - 1):
        mbox.send_keys(words[i])
        mbox.send_keys(Keys.RETURN)
        # time.sleep(0.1)
    mbox.send_keys("I had virtually no rehearsal for that. ")
    mbox.send_keys(Keys.RETURN)
    mbox.send_keys("-------------------")
    mbox.send_keys(Keys.RETURN)
    mbox.send_keys("Yeah, that's the end")
    mbox.send_keys(Keys.RETURN)


def noBrowserCleverBot():
    cb.init()
    while (True):
        text = input("Say something to CleverBot:")
        if text.lower().find("end") != -1:
            break
        response = cb.getResponse(text)
        print(response)
    cb.close()


def lookForMessagesAndRespond():
    while True:
        for i in range(12):
            try:
                global newMessagesIcon
                # Look at the requests for texting
                newMessagesIcon = chrome.find_element_by_css_selector("button[class='sqdOP yWX7d    y3zKF     ']")
            except:
                print("No requests yet")
            else:
                print("New Request OMG!")
                newMessagesIcon.click()
                time.sleep(3)
                # Click On User
                newMessagesArray = chrome.find_elements_by_css_selector(
                    "div[class='                     Igw0E     IwRSH        YBx95      vwCYk                                                                                                               ']")
                newMessagesArray[0].click()
                time.sleep(3)
                # Click Accept
                newMessagesArray = chrome.find_elements_by_tag_name('button')
                newMessagesArray[6].click()
                time.sleep(10)
                chatWithCleverBot()
                goToMessages()
            try:
                # Looks if there are any unaswered messages
                newMessagesIcon = chrome.find_element_by_class_name("KdEwV")
            except:
                print("Doesn't exist")
            else:
                print("New Messages OMG!")
                newMessagesIcon.click()
                time.sleep(3)
                # Click On User
                newMessagesArray = chrome.find_elements_by_css_selector(
                    "div[class='                     Igw0E   rBNOH          YBx95   ybXk5    _4EzTm                      soMvl                                                                                        ']")
                newMessagesArray[len(newMessagesArray) - 1].click()
                time.sleep(3)
                chatWithCleverBot()
                goToMessages()
            time.sleep(5)
        goToMessages()
        time.sleep(5)

keep_alive()
path()
time.sleep(1)
url_name('https://www.instagram.com/accounts/login/')
login(username, password)
lookForMessagesAndRespond()
