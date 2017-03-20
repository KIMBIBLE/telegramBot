# -*- coding: utf-8 -*-

import sys
import time
import telepot
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton
import requests
from bs4 import BeautifulSoup
from selenium import webdriver


if __name__ == "__main__":
  #for Web Driver
  url = "http://m.sejong.ac.kr/front/cafeteria.do"
  driver = webdriver.PhantomJS(service_args=['--ssl-protocol=any'])
  driver.get(url)
  driver.execute_script("selectedCafeteria(2)") 

  htmlSource = driver.page_source
  bs = BeautifulSoup(htmlSource, 'html.parser')
  type = bs.find_all('strong')
  
  get = bs.find_all('div', attrs = {'class':'th'})

  #print(date)
  typeList = []
  dateList = []

  idx = 0
  for each in get:
    each = each.text.strip()
    if idx % 7 == 0:
      typeList.append('\n\n'+each + '\n')

    else:
      dateList.append(each)
    idx += 1
  
  dateList = dateList[:6]

  menuBs = bs.find_all('div', attrs = {'class':'td'})
  menuList = []
  for each in menuBs:
    menu = '\n' + each.text.strip() + '\n'
    menuList.append(menu)

  mList = [menuList[i:i+6] for i in range(0, len(menuList), 6)]
  
  dList = []
  for i in range(5):
    dList.extend(dateList) 

  row = [a + b for a, b in zip(dList, menuList)]
  
  rList = [row[i:i+6] for i in range(0, len(row), 6)]

  res = list(zip(typeList, rList))

  message = []
  for i in res:
    for j in i:
      message += j

  driver.quit()

  print(message)
