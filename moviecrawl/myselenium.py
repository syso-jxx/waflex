from selenium import webdriver
from urllib.request import urlretrieve
result = []

driver = webdriver.Chrome('chromedriver') #또는 chromedriver.exe
driver.implicitly_wait(15) # 묵시적 대기, 활성화를 최대 15초가지 기다린다.

cnt = 1
for i in range(25, 301, 25):
    cnt += 1
    for j in range(1, 26):
        if i == 275 and j == 9:
            continue
        if i == 275 and j == 25:
            continue
        
        driver.get('https://www.kobis.or.kr/kobis/business/stat/online/onlineFormerBoxRank.do?CSRFToken=5kZIks2cMwh744bDS_YdaGOfYvGn7B_9DyZG58yH4VA&loadEnd=0&searchType=search')
        
        tab = f'//*[@id="content"]/div[6]/ul/li[{cnt}]/a'
        driver.find_element_by_xpath(tab).click() 
        
        xpath = f'//*[@id="table_{i}"]/tbody/tr[{j}]/td[3]/a/span'
        driver.find_element_by_xpath(xpath).click()
        
        xpath2 = '/html/body/div[2]/div[2]/div/div/div[2]/a'
        driver.find_element_by_xpath(xpath2).click()
         
        driver.switch_to.window(driver.window_handles[-1])
         
        img_path = '/html/body/a/img'
        img = driver.find_element_by_xpath(img_path)
 
        result.append(img.get_attribute('src'))

        start = result[-1].rfind('.')
        filetype = result[-1][start:]
        urlretrieve(result[-1], './imgs/{}{}'.format(i + j, filetype))
        
        
# for index, link in enumerate(result):           #리스트에 있는 원소만큼 반복, 인덱스는 index에, 원소들은 link를 통해 접근 가능
#     start = link.rfind('.')         #.을 시작으로
#     filetype = link[start:]      #확장자명을 잘라서 filetype변수에 저장 (ex -> .jpg)
#     urlretrieve(link, './imgs/{}{}'.format(index + 26, filetype))  
     
driver.quit()
