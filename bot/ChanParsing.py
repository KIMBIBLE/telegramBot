from selenium import webdriver
import time
from bs4 import BeautifulSoup

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
	driver.execute_script("selectedCafeteria(1)")	

	htmlSource = driver.page_source
	bs = BeautifulSoup(htmlSource, 'html.parser')
	menu = bs.find_all('div', attrs = {'class':'td'})
	
	menuList = []
	for each in menu:
		each = each.text.strip()
		each.replace(',', '\n')

		menuList.append(each)
	menuList.append(menuList[-1])
	del menuList[1::2]

	menuKey = [u"<월>\n", u"<화>\n", u"<수>\n", u"<목>\n", u"<금>\n", u"<석식>\n", u"<영업시간>\n"]

	res = []
	for (m,k) in zip(menuList, menuKey):
		res.append(k)
		m = m.replace(",", "\n")
		print(m)
		res.append(m)
		
#	print(res)

#	menuDict = dict(zip(menuList, menuKey))
#	print(menuDict)

	#pageToClick = bs.find_all('a', attrs = {'class' : 'onclick'})
	#pageToClick = bs.find_all('a')
	#print(pageToClick)
#	print(bs.find_all('a', attrs = {"class":"onclick"}))
#	pageList = []

#	time.sleep(3)
	#driver.execute_script("document.selectedCafeteria(1).click()")
	#print(html)
	#htmlSource = driver.page_source
	#bs = BeautifulSoup(htmlSource, 'html.parser')
	#print(bs)

	driver.quit()
