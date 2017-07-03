#!/usr/bin/env python
# -*- coding: utf8 -*-
import requests
import time
from selenium import webdriver
#from selenium.webdriver.common.keys import Keys
import re
from urllib.request import urlopen
from bs4 import BeautifulSoup

import helpers
#print(driver.current_url)
#driver.quit()

ACCESS_TOKEN = 'AbVZ6pBecrXC9afBG9mahRCxS8NuFM2MA50rraBEIg4xUYA_VwAAAAA'

class pinBot():
    def __init__(self):
        self.baseUrl = 'https://in.pinterest.com'
        self.apiUrl = 'https://api.pinterest.com/v1/'

    def search(self,keyword,searchType,scrolls):
        ids = []
        if(searchType=='pin'):
            pinDriver = webdriver.PhantomJS()
            pinDriver.get( self.baseUrl + r'/search/pins/?q=' + keyword )
            #body = pinDriver.find_element_by_tag_name("body")
            pinEls = []
            while scrolls: #scrolls is an int
                #pinEls.extend(pinDriver.find_elements_by_css_selector('.pinImageWrapper'))
                pinEls.extend(pinDriver.execute_script("return document.querySelectorAll('.pinImageWrapper')"))

                # get all pin elements to pinEls
                #pinEls = pinDriver.find_elements_by_css_selector('.pinImageWrapper')
                # take ss
                pinDriver.get_screenshot_as_file('google'+str(scrolls)+'.png')
                # print ids
                for pin in pinEls:
                    print(re.search('\d+',pin.get_attribute('href')).group())
                # scroll last element to top
                pinDriver.execute_script("return arguments[0].scrollIntoView();", pinEls[len(pinEls)-1])

                #pinDriver.execute_script("window.scrollBy(0, document.body.scrollHeight);")
                #print(pinDriver.execute_script("return document.title"))
                #pinDriver.execute_script("return window.scrollTo(0, document.body.scrollHeight);")
                #print(pinEls[len(pinEls)-1])
                #pinDriver.execute_script("window.scrollBy(0, -150);")
                #body.send_keys(Keys.PAGE_DOWN)
                time.sleep(3) # give time to load
                scrolls-=1
                print("******")
            #pinEls = pinDriver.find_elements_by_css_selector('.pinImageWrapper')
            #for pin in pinEls:
            #    print(re.search('\d+',pin.get_attribute('href')).group())
            pinDriver.quit()
            #data = urlopen(self.baseUrl + r'/search/pins/?q=' + keyword ).read()
            #soup = BeautifulSoup(data,"html.parser")
            #pins = soup.find_all("a", {'class':['pinLink','pinImageWrapper']})
            #for pin in pins:
            #	ids.append(re.search('\d+',pin.get('href')).group())
            #return ids
        elif(searchType=='board'):
            data = urlopen(self.baseUrl + r'/search/boards/?q=' + keyword ).read()
            soup = BeautifulSoup(data,"html.parser")
            boards = soup.find_all("a", {'class':['boardLinkWrapper']})
            for board in boards:
            	ids.append(board.get('href'))
            return ids
        else:
            raise "something happened"

    def followUser(self,userId):
        params = [ 'access_token='+ACCESS_TOKEN, 'user='+userId]
        r = requests.post(self.apiUrl+'me/following/users/?'+'&'.join(params))
        print(r.status_code)

    def unfollowUser(self,userId):
        params = [ 'access_token='+ACCESS_TOKEN ]
        r = requests.post(self.apiUrl+'me/following/users/'+userId+'?'+'&'.join(params))
        print(r.status_code)

    def followBoard(self,boardId):
        params = [ 'access_token='+ACCESS_TOKEN, 'board='+boardId]
        r = requests.post(self.apiUrl+'me/following/boards/?'+'&'.join(params))
        print(r.status_code)

    def unfollowBoard(self,boardId):
        params = [ 'access_token='+ACCESS_TOKEN ]
        r = requests.post(self.apiUrl+'me/following/boards/'+boardId+'?'+'&'.join(params))
        print(r.status_code)

    def savePin(self,pinId):
        # save pin method is not implemented yet
        params = [ 'access_token='+ACCESS_TOKEN ]
        r = requests.patch(self.apiUrl+'me/following/users/'+userId+'?'+'&'.join(params))

    def createPost(self,imageUrl):
        pass



"""
Requirements:
    1. search a topic
    2. get 10 results
    3. follow those boards, save those pins(if pins), follow board creators
    4. if already followed, unfollow them and skip.
    repeat this 3 times in a day.
API endpoints provided :
1. fetch user data (not needed)
2. create user follow and board follow
	/v1/me/following/boards/ POST
	/v1/me/following/users/ POST
2. delete user follow and board follow
	/v1/me/following/boards/<board>/
	/v1/me/following/users/ POST
FOLLOW example
https://api.pinterest.com/v1/me/following/users/?access_token=AbVZ6pBecrXC9afBG9mahRCxS8NuFM2MA50rraBEIg4xUYA_VwAAAAA&user=rdturner31
https://api.pinterest.com/v1/me/following/boards/?access_token=AbVZ6pBecrXC9afBG9mahRCxS8NuFM2MA50rraBEIg4xUYA_VwAAAAA&board=janew/happy
UNFOLLOW
https://api.pinterest.com/v1/me/following/users/rdturner31?access_token=AbVZ6pBecrXC9afBG9mahRCxS8NuFM2MA50rraBEIg4xUYA_VwAAAAA

Search urls:
1. boards search: https://in.pinterest.com/search/boards/?q=happy
1. pin search: https://in.pinterest.com/search/pins/?q=cool
"""
