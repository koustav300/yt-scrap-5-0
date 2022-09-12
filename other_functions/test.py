


from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import pandas as pd

options=Options()
options.add_argument("start-maximized")

#path to chrome driver
driver = webdriver.Chrome(options=options, executable_path='../chromedriver.exe')
url='https://www.youtube.com/user/krishnaik06/videos'
driver.get(url)

#mainContainer = driver.find_element("id","items")
video_mainContainer = driver.find_elements(By.TAG_NAME, 'ytd-grid-video-renderer')
print(len(video_mainContainer))

all_video_links=[]
for eachVideo in video_mainContainer:
    video_link = eachVideo.find_elements(By.TAG_NAME, 'a')[0].get_attribute("href")
    print(video_link)
    all_video_links.append(video_link)

test_link = all_video_links[3]
#driver.get(test_link)

#----------------------------------------------------------
# importing the module


from youtube_comment_scraper_python import *
youtube.open(test_link)
response=youtube.video_comments()
data=response['body']
df = pd.DataFrame(data)
print(df)


