import urllib.request
from bs4 import BeautifulSoup

def hakGanParse():

	url = "http://m.sejong.ac.kr/front/cafeteria.do"
	req = urllib.request.Request(url)
	data = urllib.request.urlopen(req).read()

	bs = BeautifulSoup(data, 'html.parser')
	menu = bs.find_all('div', attrs = {'class':'th'})

	menuList = []
	for each in menu:
		menuList.append(each.text)

	price = bs.find_all('div', attrs = {'class':'td'})
	priceList = []
	for each in price:
		priceList.append(each.text)

	menuDict = {}
	menuDict = dict(zip(menuList, priceList))
