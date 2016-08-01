from selenium import webdriver
import selenium
import SessionInitializer
import shutil

ch = webdriver.Chrome("./chromedriver")

if SessionInitializer.ROOT_URL == "https://scholar-google-ca.proxy.lib.uwaterloo.ca":
    ch.get('https://login.proxy.lib.uwaterloo.ca/login')
    cookies = [{'path': '/', 'domain': '.lib.uwaterloo.ca', 'httpOnly': False, 'name': 'ezproxy', 'secure': False, 'value': '8XEKbAbUoGf9tb4'}, {'path': '/', 'domain': '.uwaterloo.ca', 'httpOnly': False, 'name': '_gat', 'secure': False, 'value': '1', 'expiry': 1470072403}, {'path': '/', 'domain': '.uwaterloo.ca', 'httpOnly': False, 'name': '_ga', 'secure': False, 'value': 'GA1.2.1227558798.1466567220', 'expiry': 1533143803}]

    for cookie in cookies:
        ch.add_cookie(cookie)

def downloadFromWatLib(url, path):
    ch.get(url)

    try:
        #href = ch.find_element_by_link_text('Scholars Portal')
        href = ch.find_element_by_xpath('//a[@href="javascript:openWindow(this, \'basic1\');" and text()="Scholars Portal"]')
    except selenium.common.exceptions.NoSuchElementException:
        print('cannot find scholars portal link on webpage')
        return None

    href.click()

    try:
        pdfxmlTag = ch.find_element_by_xpath("//div[@class='download-btn']/a[text()='PDF Download']")
        pdfxmllink = pdfxmlTag.get_attribute('href')

    except selenium.common.exceptions.NoSuchElementException:
        print('Racer or invalid link only, no scholarsportal returning none...')
        return None

    print(pdfxmllink)

    session = SessionInitializer.getSesh()
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

# downloadFromWatLib('http://sfx.scholarsportal.info.proxy.lib.uwaterloo.ca/waterloo?url_ver=Z39.88-2004&rft.genre=article&rft.issn=2043-6386&rft.date=2014&rft.jtitle=IET%20Wireless%20Sensor%20Systems&rft.atitle=Optimal%20gateway%20selection%20in%20sensor-cloud%20framework%20for%20health%20monitoring&rft.volume=4&rft.issue=2&rft.spage=61&rfr_id=info:sid/OCUL:journals',
#     'test.pdf')