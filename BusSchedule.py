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
  This is done to avoid unnecessary calls to the site for our testing.
  """
  page = open("testPage.txt", 'r')
  contents = page.read()
  page.close()

  return contents


#function that analyzes a word to determine whether that word is a time
def isItaTime(word):
  word = word.strip()
  if len(word) < 5:
    return False
  elif ":" not in word:
    return False
  elif "PM" not in word and "AM" not in word:
    return False
  else:
    return True

#function that filters through all words in the page to determine which are times
def retrieveTimes(loadedURL):
  validTimes = []
  contentLoad = loadedURL #recalls the loaded contents from the web page
  wordContents = contentLoad.split()
  for word in wordContents:
    if isItaTime(word) == True:
      validTimes.append(word)
  return validTimes

#this function calculates the given time in minutes
def getCurrentTime(time):
  minutesForNow = 0
  time = time.strip().upper().rstrip(",.;:!?)[]}")
  isPM = time.endswith("PM")
  isAM = time.endswith("AM")
  time = time.replace("AM", "").replace("PM", "").strip()
  parts = time.split(":")
  hour = int(parts[0])
  minute = int(parts[1])
  if isAM:
    if hour == 12:
      hour = 0
  elif isPM:
    if hour != 12:
      hour += 12
  minutesForNow = minutesForNow + (hour * 60)
  minutesForNow = minutesForNow + (minute)
  return minutesForNow

#this function gets the current time
def whatTimeIsIt():
  now = datetime.datetime.now()
  currentHour24 = (now.hour - 5) % 24
  currentMinute = now.minute
  suffix = "AM" if currentHour24 < 12 else "PM"
  currentHour12 = currentHour24 % 12
  if currentHour12 == 0:
    currentHour12 = 12
  currentHourMin = "%d:%02d%s" % (currentHour12, currentMinute, suffix)
  return(currentHourMin)

#this function searches the list of times (displayed in minutes) to determine which is next
def getNextTime1(listOfTimes, currentTimeInMin):
  convertedTimes = []
  for spot in listOfTimes:
    timeInMin = getCurrentTime(spot)
    convertedTimes.append(timeInMin)
  nextTime1 = None
  for spot in convertedTimes:
    if spot >= currentTimeInMin:
      if nextTime1 is None or spot < nextTime1:
        nextTime1 = spot
  if nextTime1 is None:
    nextTime1 = min(convertedTimes) + 24*60
  return nextTime1

#this function searches for the second next time
def getNextTime2(listOfTimes, firstNextTime):
  newListOfTimes = copy.listOfTimes()
  newListOfTimes = newListOfTimes.drop[firstNextTime]
  currentTimeInMin = whatTimeIsIt()
  nextTime2 = getNextTime1(newListOfTimes, currentTimeInMin)
  return nextTime2

#this function converts the calculated next times into a user-friendly display time
def recalculateTime(nextTime):
  newHour24 = (nextTime)//60
  newMin = (nextTime) % 60
  suffix = "AM" if newHour24 < 12 else "PM"
  newHour12 = newHour24 % 12
  if newHour12 == 0:
    newHour12 = 12
  newTime = ("%d:%d%s" %(newHour12, newMin, suffix))
  return newTime


def main():
  busStopNum = "2269"
  routeNum = "11"
  direction = "EAST"
  url = "https://myride.ometro.com/Schedule?stopCode=" +busStopNum +"&routeNumber=" +routeNum +"&directionName=" +direction
  loadedURL = loadURL(url) #loads the web page
  listOfTimes = retrieveTimes(loadedURL)
  currentTime = whatTimeIsIt()
  currentTimeInMin = getCurrentTime(currentTime)
  firstNextTime = getNextTime1(listOfTimes, currentTimeInMin)
  newListOfTimes = list(listOfTimes)
  newListOfTimes.remove(firstNextTime)
  secondNextTime = getNextTime1(newListOfTimes, currentTimeInMin)
  recalFirstNextTime = recalculateTime(firstNextTime)
  recalSecondNextTime = recalculateTime(secondNextTime)

  print(currentTime)
  print(listOfTimes)
  print(currentTimeInMin)
  print(firstNextTime)
  print(recalFirstNextTime)
  print("It is %s currently. The next two busses will arrive at %s and %s." %(currentTime, recalFirstNextTime, recalSecondNextTime))
  

main()
