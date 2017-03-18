import sys
import time
import telepot
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton
import urllib.request
from bs4 import BeautifulSoup
from selenium import webdriver


def on_chat_message(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    if msg['text'] == u'/학식':
      keyboard = InlineKeyboardMarkup(inline_keyboard=[
                     [InlineKeyboardButton(text=u'1.학생회관', callback_data='HakKwan')],
                     [InlineKeyboardButton(text=u'2. 찬 스카이라운지', callback_data='ChanSky')],
                     [InlineKeyboardButton(text=u'3. 우정당', callback_data= 'WuJung')],
                     [InlineKeyboardButton(text=u'4. 군자관', callback_data= 'KwunJa')],
                 ])
      message = u'<세종대 학식 메뉴>\n1.학생식당\n2.찬 스카이라운지\n3.우정당\n군자관\n'

      bot.sendMessage(chat_id, message, reply_markup=keyboard)

    elif msg['text'] == '/?':
      message = '0. help : /?, /help, /h\n'
      message += '1. 학식 메뉴 : /학식'
      bot.sendMessage(chat_id, message)



def on_callback_query(msg):
    query_id, from_id, query_data = telepot.glance(msg, flavor='callback_query')

    if query_data == 'HakKwan' :
      hakKwanPrint(from_id)

    elif query_data == 'ChanSky' :
      chanPrint(from_id)

    elif query_data == 'WuJung' :
      wuJungPrint(from_id)

    elif query_data == 'KwunJa' :
      kwunJaPrint(from_id, message)

    bot.answerCallbackQuery(query_id, text='Got it')

def makeDictMessage(message, menuDict):
  for key in menuDict:
    message += key
    message += " : "
    message += menuDict[key]
    message += '\n'

  return message

def makeListMessage(message, menuList):
  for each in menuList:
    message += each

  return message

def getFilePath(path, name):
  path.replace("\\", "\\\\")
  path += "\\"
  path += name

  return path

def hakKwanParse():

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

  return menuDict

def hakKwanPrint(from_id):
  menuDict = {}
  menuDict = hakKwanParse()

  message = u"<학생회관 메뉴>\n\n"
  message = makeDictMessage(message, menuDict)
  bot.sendMessage(from_id, message)

def chanParse():
  #for Web Driver
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
    each += '\n\n'
    menuList.append(each)
  menuList.append(menuList[-1])
  del menuList[1::2]

  menuKey = [u"<월>\n", u"<화>\n", u"<수>\n", u"<목>\n", u"<금>\n", u"<석식>\n", u"<영업시간>\n"]

  res = []
  for (m,k) in zip(menuList, menuKey):
    res.append(k)
    m = m.replace(",", "\n")
    res.append(m)
  
  driver.quit()

  return res



def chanPrint(from_id):
  menuList = []
  menuList = chanParse()

  message = u"<찬 스카이라운지 메뉴>\n\n"
  message = makeListMessage(message, menuList)
  bot.sendMessage(from_id, message)



def wuJungParse():
  path = r"/home/ubuntu/chromedriver"
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

  return message

def wuJungPrint(from_id):
  menuList = []
  menuList = wuJungParse()

  message = u"<우정당 메뉴>\n\n"
  message = makeListMessage(message, menuList)
  bot.sendMessage(from_id, message)

def kwunJaPrint(from_id):
  message = u"웹페이지에 메뉴 정보가 없습니다."
  bot.sendMessage(from_id, message)


if __name__ == "__main__":
  #TOKEN = sys.argv[1]  # get token from command-line
  TOKEN = "275249192:AAGCvhDeuRq2BSHQmmUy2hHfGDOVO84qwF0"



  bot = telepot.Bot(TOKEN)
  bot.message_loop({'chat': on_chat_message,
                  'callback_query': on_callback_query})
  print('Listening ...')

  while 1:
      time.sleep(10)
