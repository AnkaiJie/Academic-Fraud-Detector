from selenium import webdriver
import selenium
import sys
import offCampusLogin
import shutil
import time

ch = webdriver.Chrome("./chromedriver")
ch.get('https://login.proxy.lib.uwaterloo.ca/login')
cookies = [{'domain': '.lib.uwaterloo.ca', 'path': '/', 'httpOnly': False, 'secure': False, 'value': '4ruzfvMwNZ5eGMV', 'name': 'ezproxy'}, {'domain': '.uwaterloo.ca', 'expiry': 1466735554, 'path': '/', 'httpOnly': False, 'secure': False, 'value': '1', 'name': '_gat'}, {'domain': '.uwaterloo.ca', 'expiry': 1529806954, 'path': '/', 'httpOnly': False, 'secure': False, 'value': 'GA1.2.1227558798.1466567220', 'name': '_ga'}]

for cookie in cookies:
    ch.add_cookie(cookie)

def downloadFromWatLib(url, path):
    ch.get(url)

    try:
        #href = ch.find_element_by_link_text('Scholars Portal')
        href = ch.find_element_by_xpath('//a[@href="javascript:openWindow(this, \'basic1\');" and text()="Scholars Portal"]')
    except selenium.common.exceptions.NoSuchElementException as e:
        print('cannot find scholars portal link' + str(e))
        return None

    href.click()

    try:
        pdfxmllink = ch.find_element_by_xpath("//div[@class='download-btn']/a").get_attribute('href')
    except selenium.common.exceptions.NoSuchElementException:
        print('Racer link only, no scholarsportal returning none...')
        return None
        
    print(pdfxmllink)

    session = offCampusLogin.getSesh()
    r = session.get(pdfxmllink, stream=True)

    if r.status_code == 200:
        with open(path, 'wb') as f:
            r.raw.decode_content = True
            shutil.copyfileobj(r.raw, f)
        return 1

    print('ERROR: watlib pdf was not downloaded correctly')
    return None



# MANUAL LOGIN
# lname = ch.find_element_by_name('pass')
# lname.send_keys('jie')
# barcode = ch.find_element_by_name('user')
# barcode.send_keys('21187005749502')
# form = ch.find_element_by_xpath('//input[@value = "Login"]')
# form.click()



# print(ch.get_cookies())
