from selenium import webdriver
import time
from bs4 import BeautifulSoup
import re
import itertools

def getFilePath(path, name):
	path.replace("\\", "\\\\")
	path += "\\"
	path += name

	return path

if __name__ == "__main__":
	path = r"C:\Users\B.B.KIM\Downloads\chromedriver_win32"
	name = r"chromedriver.exe"

	driver_path = getFilePath(path, name)

	url = "http://m.sejong.ac.kr/front/cafeteria.do"
	driver = webdriver.Chrome(executable_path = driver_path)
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
		#print(each)
		if idx % 7 == 0:
			typeList.append(each)

		else:
			dateList.append(each)
		idx += 1
	
	dateList = dateList[:6]

	menuBs = bs.find_all('div', attrs = {'class':'td'})
	menuList = []
	for each in menuBs:
		menu = each.text.strip()
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
	print(message)

	driver.quit()
