#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import selenium


# In[ ]:


import requests


# In[ ]:


from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager


# In[ ]:


import os


# In[ ]:


import time


# In[ ]:


import bs4


# In[ ]:


#creating a directory to save images
folder_name = 'images'
if not os.path.isdir(folder_name):
    os.makedirs(folder_name)

def download_image(url, folder_name, num):

    # write image to file
    reponse = requests.get(url)
    if reponse.status_code==200:
        with open(os.path.join(folder_name, str(num)+".jpg"), 'wb') as file:
            file.write(reponse.content)


# In[ ]:


print("What do you want do search for on google image ? ")
search_term = input("")
print("Link for ",search_term, "below :")
new_url = "https://www.google.com/search?q=tomato+leaf&sxsrf=APq-WBuDSmcqKzcKsRizpkNif0iljBU3sQ:1647872794888&source=lnms&tbm=isch&sa=X&ved=2ahUKEwja3MvEtNf2AhULzIUKHazXD4EQ_AUoAXoECAIQAw&biw=1536&bih=722&dpr=1.25"
search_term = search_term.split(" ")
url= "https://www.google.com/search?q="
for i in range(len(search_term)):
    if(i!=len(search_term)-1):
        url = url + search_term[i] + "+"
    else:
        url = url + search_term[i] + "&sxsrf=APq-WBuDSmcqKzcKsRizpkNif0iljBU3sQ:1647872794888&source=lnms&tbm=isch&sa=X&ved=2ahUKEwja3MvEtNf2AhULzIUKHazXD4EQ_AUoAXoECAIQAw&biw=1536&bih=722&dpr=1.25"
print(url)


# In[ ]:


chromePath=r'C:\chromedriver.exe'
driver=webdriver.Chrome(chromePath)

# new_url = "https://www.google.com/search?q=tomato+leaf&sxsrf=APq-WBuDSmcqKzcKsRizpkNif0iljBU3sQ:1647872794888&source=lnms&tbm=isch&sa=X&ved=2ahUKEwja3MvEtNf2AhULzIUKHazXD4EQ_AUoAXoECAIQAw&biw=1536&bih=722&dpr=1.25"
new_url = url
driver.get(new_url)

SCROLL_PAUSE_TIME = 3

# Get scroll height
last_height = driver.execute_script("return document.body.scrollHeight")

while True:
    # Scroll down to bottom
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    # Wait to load page
    time.sleep(SCROLL_PAUSE_TIME)

    # Calculate new scroll height and compare with last scroll height
    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        break
    last_height = new_height

page_html = driver.page_source
pageSoup = bs4.BeautifulSoup(page_html, 'html.parser')
containers = pageSoup.findAll('div', {'class':"isv-r PNCib MSM1fd BUooTd"} )

print("round 1: Found ",len(containers),"images")
print("checking if there is more....")
    
if driver.find_element_by_xpath('/html/body/div[2]/c-wiz/div[4]/div[1]/div/div/div/div[1]/div[2]/div[2]/input'):
    print ("There is more images ! Wait...")
    button = driver.find_element_by_xpath('/html/body/div[2]/c-wiz/div[4]/div[1]/div/div/div/div[1]/div[2]/div[2]/input')
    button.click()
else:
    print("No more images :(")
    driver.execute_script("window.scrollTo(0, 0);")

while True:
    # Scroll down to bottom
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    # Wait to load page
    time.sleep(SCROLL_PAUSE_TIME)

    # Calculate new scroll height and compare with last scroll height
    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        break
    last_height = new_height

page_html = driver.page_source
pageSoup = bs4.BeautifulSoup(page_html, 'html.parser')
containers = pageSoup.findAll('div', {'class':"isv-r PNCib MSM1fd BUooTd"} )

print("round 2 : Found ",len(containers),"images")
print("checking if there is more....")

if driver.find_element_by_xpath('/html/body/div[2]/c-wiz/div[4]/div[1]/div/div/div/div[1]/div[2]/div[1]/div[2]/div[1]/div'):
    print("No more images")
    driver.execute_script("window.scrollTo(0, 0);")
elif driver.find_element_by_xpath('/html/body/div[2]/c-wiz/div[4]/div[1]/div/div/div/div[1]/div[2]/div[2]/input'):
    print ("There is more images ! Wait...")
    button = driver.find_element_by_xpath('/html/body/div[2]/c-wiz/div[4]/div[1]/div/div/div/div[1]/div[2]/div[2]/input')
    button.click()
else:
    print("error")
    driver.execute_script("window.scrollTo(0, 0);")
    
print("click for download all",len(containers),"images")
a = input("waiting for click")

page_html = driver.page_source
pageSoup = bs4.BeautifulSoup(page_html, 'html.parser')
containers = pageSoup.findAll('div', {'class':"isv-r PNCib MSM1fd BUooTd"} )

print(len(containers))

len_containers = len(containers)

for i in range(1, len_containers+1):
    if i % 25 == 0:
        continue

    xPath = """//*[@id="islrg"]/div[1]/div[%s]"""%(i)

    previewImageXPath = """//*[@id="islrg"]/div[1]/div[%s]/a[1]/div[1]/img"""%(i)
    previewImageElement = driver.find_element_by_xpath(previewImageXPath)
    previewImageURL = previewImageElement.get_attribute("src")
    #print("preview URL", previewImageURL)


    #print(xPath)


    driver.find_element_by_xpath(xPath).click()
    #time.sleep(3)

    #//*[@id="islrg"]/div[1]/div[16]/a[1]/div[1]/img

    #input('waawgawg another wait')

    # page = driver.page_source
    # soup = bs4.BeautifulSoup(page, 'html.parser')
    # ImgTags = soup.findAll('img', {'class': 'n3VNCb', 'jsname': 'HiaYvf', 'data-noaft': '1'})
    # print("number of the ROI tags", len(ImgTags))
    # link = ImgTags[1].get('src')
    # #print(len(ImgTags))
    # #print(link)
    #
    # n=0
    # for tag in ImgTags:
    #     print(n, tag)
    #     n+=1
    # print(len(ImgTags))

    #/html/body/div[2]/c-wiz/div[3]/div[2]/div[3]/div/div/div[3]/div[2]/c-wiz/div/div[1]/div[1]/div[2]/div[1]/a/img

    #It's all about the wait

    timeStarted = time.time()
    while True:

        imageElement = driver.find_element_by_xpath("""//*[@id="Sva75c"]/div/div/div[3]/div[2]/c-wiz/div/div[1]/div[1]/div[2]/div[1]/a/img""")
        imageURL= imageElement.get_attribute('src')

        if imageURL != previewImageURL:
            #print("actual URL", imageURL)
            break

        else:
            #making a timeout if the full res image can't be loaded
            currentTime = time.time()

            if currentTime - timeStarted > 10:
                print("Timeout! Will download a lower resolution image and move onto the next one")
                break


    #Downloading image
    try:
        download_image(imageURL, folder_name, i)
        print("Downloaded element %s out of %s total. URL: %s" % (i, len_containers + 1, imageURL))
    except:
        print("Couldn't download an image %s, continuing downloading the next one"%(i))

    #//*[@id="Sva75c"]/div/div/div[3]/div[2]/c-wiz/div/div[1]/div[1]/div[2]/div[1]/a/img
    #//*[@id="Sva75c"]/div/div/div[3]/div[2]/c-wiz/div/div[1]/div[1]/div[2]/div[1]/a/img


# In[ ]:




