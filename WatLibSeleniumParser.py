from selenium import webdriver
import selenium
import sys
import offCampusLogin
import shutil

ch = webdriver.Chrome("./chromedriver")
ch.get('https://login.proxy.lib.uwaterloo.ca/login')
cookies = [{'domain': '.lib.uwaterloo.ca', 'path': '/', 'secure': False, 'value': 'NJdM75GDpxyStXr', 'name': 'ezproxy', 'httpOnly': False}, {'domain': '.uwaterloo.ca', 'path': '/', 'secure': False, 'expiry': 1466049181, 'value': '1', 'name': '_gat', 'httpOnly': False}, {'domain': '.uwaterloo.ca', 'path': '/', 'secure': False, 'expiry': 1529120581, 'value': 'GA1.2.867031542.1466048582', 'name': '_ga', 'httpOnly': False}]
for cookie in cookies:
	ch.add_cookie(cookie)

ch.get('http://sfx.scholarsportal.info.proxy.lib.uwaterloo.ca/waterloo?sid=google&auinit=P&aulast=Rawat&atitle=Wireless+sensor+networks:+a+survey+on+recent+developments+and+potential+synergies&id=doi:10.1007/s11227-013-1021-9&title=The+Journal+of+Supercomputing&volume=68&issue=1&date=2014&spage=1&issn=0920-8542')

try:
	href = ch.find_element_by_link_text('Scholars Portal')
except selenium.common.exceptions.NoSuchElementException as e:
	print('cannot find scholars portal link')
	sys.exit()

href.click()

pdfxmllink = ch.find_element_by_xpath("//div[@class='download-btn']/a").get_attribute('href')

print(pdfxmllink)


session = offCampusLogin.getSesh()
r = session.get(pdfxmllink, stream=True)

if r.status_code == 200:
    with open('ankai.pdf', 'wb') as f:
        r.raw.decode_content = True
        shutil.copyfileobj(r.raw, f)




## MANUAL LOGIN
# lname = ch.find_element_by_name('pass')
# lname.send_keys('jie')
# barcode = ch.find_element_by_name('user')
# barcode.send_keys('21187005749502')
# form = ch.find_element_by_xpath('//input[@value = "Login"]')
# form.click()



# print(ch.get_cookies())
