import csv
from getpass import getpass
from time import sleep
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver import Chrome

#getting info from user
yourUsername = input('Please enter your username\n')
yourPassword = input('Please enter your password\n')
yourTweet = input('What would you like to tweet today?\n')

#logging into twitter via google chrome
driver = Chrome()
driver.get('https://twitter.com/login')

username = driver.find_element_by_xpath('//input[@name="session[username_or_email]"]')
username.send_keys(yourUsername)

password = driver.find_element_by_xpath('//input[@name="session[password]"]')
password.send_keys(yourPassword)
password.send_keys(Keys.RETURN)

carteBlanche = driver.find_element_by_xpath('//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div/div/div[2]/div/div[2]/div[1]/div/div/div/div[2]/div[1]/div/div/div/div/div/div/div/div/label/div[1]/div/div/div/div/div[2]/div/div/div/div')
carteBlanche.send_keys(yourTweet)
sleep(2)
submit_button = driver.find_element_by_xpath('/html/body/div/div/div/div[2]/main/div/div/div/div/div/div[2]/div/div[2]/div[1]/div/div/div/div[2]/div[3]/div/div/div[2]/div[3]')
submit_button.send_keys(Keys.RETURN)