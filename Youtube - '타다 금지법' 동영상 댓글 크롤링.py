#!/usr/bin/env python
# coding: utf-8

# ### 유튜브 댓글 크롤링 & 분석(검색어: 타다 금지법)

# In[1]:


import requests
import time
import scrapy

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from scrapy.http import TextResponse
from bs4 import BeautifulSoup


# #### 1) 유튜브 첫 화면에서 '타다금지법' 검색하여, 이번주 업로드된 동영상 제목, url 가져오기
# ####   (as of 3/15)

# In[2]:


options = Options()
options.headless = True
driver = webdriver.Chrome('/home/ubuntu/chromedriver', options=options)
driver.get('https://www.youtube.com/results?search_query=타다 금지법&sp=EgIIAw%253D%253D')

page=driver.page_source
soup = BeautifulSoup(page,'lxml')

all_ = soup.find_all('a','yt-simple-endpoint style-scope ytd-video-renderer')

#제목
titles = [all_[n].text.strip() for n in range(0,len(all_))]
#주소 
links= ["https://www.youtube.com/" + all_[n].get('href') for n in range(0,len(all_))]

titles, links


# #### 2) 동영상 상세 링크 접속하여 댓글 남긴 사람 id, comment 가져오기(우선 sample로 3개)

# In[3]:


comment_data = pd.DataFrame({'제목': [],
                             'user_id': [],
                             '댓글': [],
                             '좋아요 수': []
                             })

for i in range(0, 3):
    start_url = links[i]
    #driver = webdriver.Chrome('/home/ubuntu/chromedriver', options=options)
    driver.get(start_url)
    
    body = driver.find_element_by_tag_name("body")

    num_of_pagedowns = 10
    
    while num_of_pagedowns: 
        body.send_keys(Keys.PAGE_DOWN) 
        time.sleep(2)
        num_of_pagedowns -= 1 
    
    try: 
        driver.find_element_by_xpath('//*[@id="sort-menu"]').click() 
        driver.find_element_by_xpath('//*[@id="menu"]/a[2]/paper-item/paper-item-body/div[text()="최근 날짜순"]').click() 
    
    except Exception as e: 
        pass
    #제목
    title = driver.find_element_by_css_selector('#container > h1 > yt-formatted-string').text
    #사용자 id    
    user_ids = driver.find_elements_by_css_selector('#author-text > span')
    # 댓글
    comments = driver.find_elements_by_css_selector('#content-text')
    #좋아요 수
    like_nums = driver.find_elements_by_css_selector('#vote-count-middle')
    
    datas = []

    for j in range(len(comments)):
        title = title
        comment = comments[j].text
        user_id = user_ids[j].text
        like_num = like_nums[j].text
        
        datas.append({
        "제목" : title,
        "user_id" : user_id,
        "댓글" : comment,
        "좋아요 수" : like_num
         })

    result_data=pd.DataFrame(datas)
    result = result_data[["제목", "user_id", "댓글", "좋아요 수"]]
    comment_data = comment_data.append(result, ignore_index=True)


# In[4]:


comment_data 


# In[6]:


### 데이터프레임 엑셀로 만들기
comment_data.to_csv('comment_data.csv')


# In[7]:


df = pd.read_csv('comment_data.csv')
df.head()


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




