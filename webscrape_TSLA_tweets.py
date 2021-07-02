import csv
from getpass import getpass
from time import sleep
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver import Chrome

#logging into twitter via google chrome
driver = Chrome()
driver.get('https://twitter.com/login')
driver.implicitly_wait(10)

username = driver.find_element_by_xpath('//input[@name="session[username_or_email]"]')
username.send_keys('    ') #insert your username here!

#i think twitter is blocking selenium here -- we will see
#my_password = getpass()
password = driver.find_element_by_xpath('//input[@name="session[password]"]')
password.send_keys('    ') #insert your password here
password.send_keys(Keys.RETURN)

#finding search bar
search_input = driver.find_element_by_xpath('//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div[2]/div/div[2]/div/div/div/div[1]/div/div/div/form/div[1]/div/label/div[2]/div/input')
search_input.send_keys('$TSLA') #change later to x in list of popular stock o whateva
search_input.send_keys(Keys.RETURN)

sleep(2) #small delay -- more humanlike
#going to latest - rn commented out. want to be at 'Top'
#driver.find_element_by_link_text('Latest').click()


'''
#testing on a single object first

#collecting tweets on page + getting an instance
tweets = driver.find_elements_by_xpath('//div[@data-testid="tweet"]')
tweet = tweets[0] 

#username
usr = tweet.find_element_by_xpath('./div[2]/div[1]//span').text
print(usr)

#twitter-handle
hndl = tweet.find_element_by_xpath('.//span[contains(text(), "@")]').text
print(hndl)

#when tweet was posted
date = tweet.find_element_by_xpath('.//time').get_attribute('datetime')
print(date)

#content
content = tweet.find_element_by_xpath('.//div[2]/div[2]/div[1]').text
print(content)

#reply count
replies = tweet.find_element_by_xpath('.//div[@data-testid="reply"]').text
print(replies)

#retweet count
retweets = tweet.find_element_by_xpath('.//div[@data-testid="retweet"]').text
print(retweets)

#like count
likes = tweet.find_element_by_xpath('.//div[@data-testid="like"]').text
print(likes)
'''

def get_tweet_data(tweet):
    usr = tweet.find_element_by_xpath('./div[2]/div[1]//span').text
    hndl = tweet.find_element_by_xpath('.//span[contains(text(), "@")]').text
    #sponsored tweets don't have post date -- must handle this
    try:
        date = tweet.find_element_by_xpath('.//time').get_attribute('datetime')
    except NoSuchElementException:
        return
    replyingTo = tweet.find_element_by_xpath('.//div[2]/div[2]/div[1]').text
    cntnt = tweet.find_element_by_xpath('.//div[@data-testid="reply"]').text
    retweets = tweet.find_element_by_xpath('.//div[@data-testid="retweet"]').text
    likes = tweet.find_element_by_xpath('.//div[@data-testid="like"]').text

    tweet = (usr, hndl, date, replyingTo, cntnt, retweets, likes)
    return tweet

#print(get_tweet_data(tweet))

tweet_data = []
tweet_ids = set()
last_position = driver.execute_script("return window.pageYOffset;")
scrolling = True

while scrolling:
    tweets = driver.find_elements_by_xpath('//div[@data-testid="tweet"]')
    for tweet in tweets[-15:]:
        data = get_tweet_data(tweet)
        if data:
            tweet_id = ''.join(data)
            if tweet_id not in tweet_ids:
                tweet_ids.add(tweet_id)
                tweet_data.append(data)

    scroll_attempt = 0
    while True:
        #checking scroll position
        driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
        sleep(1)
        curr_position = driver.execute_script("return window.pageYOffset;")
        if last_position == curr_position:
            scroll_attempt += 1

            #end of scroll region
            if scroll_attempt >= 3:
                scrolling = False
                break
            else:
                sleep(2) #try again
        else:
            last_position = curr_position
            break

#saving the tweet data
    with open('tsla_tweets.csv', 'w', newline='', encoding='utf-8') as f:
        header = ['Username', 'Handle', 'Timestamp', 'Comments', 'Likes', 'Retweets', 'Text']
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(tweet_data)
