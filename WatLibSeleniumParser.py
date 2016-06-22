from selenium import webdriver
import selenium
import sys
import offCampusLogin
import shutil

ch = webdriver.Chrome("./chromedriver")
ch.get('https://login.proxy.lib.uwaterloo.ca/login')
cookies = [{'value': 'cBPpTkeDD01KUA3', 'name': 'ezproxy', 'httpOnly': False, 'domain': '.lib.uwaterloo.ca', 'secure': False, 'path': '/'}, {'value': '1', 'name': '_gat', 'httpOnly': False, 'expiry': 1466567819, 'domain': '.uwaterloo.ca', 'secure': False, 'path': '/'}, {'value': 'GA1.2.1227558798.1466567220', 'name': '_ga', 'httpOnly': False, 'expiry': 1529639219, 'domain': '.uwaterloo.ca', 'secure': False, 'path': '/'}]
for cookie in cookies:
    ch.add_cookie(cookie)

def downloadFromWatLib(url, path):
    ch.get(url)

    try:
        href = ch.find_element_by_link_text('Scholars Portal')
    except selenium.common.exceptions.NoSuchElementException as e:
        print('cannot find scholars portal link' + str(e))

    href.click()

    pdfxmllink = ch.find_element_by_xpath("//div[@class='download-btn']/a").get_attribute('href')

    print(pdfxmllink)

    session = offCampusLogin.getSesh()
    r = session.get(pdfxmllink, stream=True)

    if r.status_code == 200:
        with open(path, 'wb') as f:
            r.raw.decode_content = True
            shutil.copyfileobj(r.raw, f)




# MANUAL LOGIN
# lname = ch.find_element_by_name('pass')
# lname.send_keys('jie')
# barcode = ch.find_element_by_name('user')
# barcode.send_keys('21187005749502')
# form = ch.find_element_by_xpath('//input[@value = "Login"]')
# form.click()



# print(ch.get_cookies())
