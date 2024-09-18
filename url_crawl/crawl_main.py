from selenium import webdriver
from bs4 import BeautifulSoup as bs
import pandas as pd
from selenium.webdriver.common.keys import Keys

meta = pd.read_csv('datasets/movies_small2.csv', encoding='euc-kr')
 
movies = []
url_result = []
 
for i in meta['영화명']:
    front = i.split('(')[0]
    movies.append(front)
    
for movie in movies:
    keyword = movie + ' 예고편'
    url = f'https://www.youtube.com/results?search_query={keyword}'
      
    driver = webdriver.Chrome('./chromedriver.exe')
    driver.get(url)
    soup = bs(driver.page_source, 'html.parser')
    driver.close()
      
    video_url = soup.select('a#video-title')
     
    url_list = []
      
    for i in video_url:
        url_list.append(f"https://www.youtube.com{i.get('href')}")
         
    url_result.append(url_list[0])
    print(len(movies))                    
    print(len(url_result))                    
      
    youtubeDic = {
        '주소': url_result
    }
      
    youtubeDf = pd.DataFrame(youtubeDic)
      
    youtubeDf.to_csv('datasets/url.csv', encoding='', index=False)