#BusSchedule.py
#Name: Meg Aerni
#Date: 10.13.2025
#Assignment: Homework 2

import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By


def loadURL(url):
  """
  This function loads a given URL and returns the text
  that is displayed on the site. It does not return the
  raw HTML code but only the code that is visible on the page.
  """
  chrome_options = Options()
  chrome_options.add_argument('--no-sandbox')
  chrome_options.add_argument('--disable-dev-shm-usage')
  chrome_options.add_argument("--headless");
  driver = webdriver.Chrome(options=chrome_options)
  driver.get(url)
  content=driver.find_element(By.XPATH, "/html/body").text
  driver.quit()

  return content

def loadTestPage():
  """
  This function returns the contents of our test page.
  This is done to avoid unnecessary calls to the site
  for our testing.
  """
  page = open("testPage.txt", 'r')
  contents = page.read()
  page.close()

  return contents

validTimes = []

#function that analyzes a word to determine whether that word is a time
def isItaTime(word):
  word = word.strip()
  if len(word) < 5:
    return False
  if ":" not in word:
    return False
  if "PM" not in word and "AM" not in word:
    return False
  else:
    validTimes.append(word)

#function that filters through all words in the page to determine which are times
def retrieveTimes():
  c1 = loadTestPage() #loads the test page
  wordContents = c1.split()
  for word in wordContents:
    isItaTime(word)
  return validTimes

#this function calculates the given time in minutes
def getCurrentTime(time):
  currentTime = 0
  time = time.replace("AM", "").replace("PM", "").strip()
  parts = time.split(":")
  hour = int(parts[0])
  minute = int(parts[1])
  currentTime = currentTime + (hour * 60)
  currentTime = currentTime + (minute)
  print(currentTime)

#def getHours(time):

def main():
  busStopNum = "2269"
  routeNum = "11"
  direction = "EAST"
  url = "https://myride.ometro.com/Schedule?stopCode=" +busStopNum +"&routeNumber=" +routeNum +"&directionName=" +direction
  c1 = loadURL(url) #loads the web page
  print(c1)
  r1 = retrieveTimes()
  now = datetime.datetime.now()
  currentHour = (now.hour - 5) % 12
  currentMinute = now.minute
  print (currentHour, currentMinute)
  print(validTimes)
  #r2 = getCurrentTime(validTimes)
  #print(r2)
  

main()
