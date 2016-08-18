from selenium import webdriver
import selenium
import SessionInitializer
import shutil

ch = webdriver.Chrome("./chromedriver")

if SessionInitializer.ROOT_URL == "https://scholar-google-ca.proxy.lib.uwaterloo.ca":
    ch.get('https://login.proxy.lib.uwaterloo.ca/login')
    cookies = [{'value': 'GnvMwRNRyR7ik5T', 'secure': False, 'domain': '.lib.uwaterloo.ca', 'name': 'ezproxy', 'path': '/', 'httpOnly': False}, {'value': '1', 'secure': False, 'expiry': 1471476498, 'name': '_gat', 'path': '/', 'domain': '.uwaterloo.ca', 'httpOnly': False}, {'value': 'GA1.2.1227558798.1466567220', 'secure': False, 'expiry': 1534547898, 'name': '_ga', 'path': '/', 'domain': '.uwaterloo.ca', 'httpOnly': False}]

    for cookie in cookies:
        ch.add_cookie(cookie)

def downloadScholarPortal(href, path):
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

    print('ERROR: watlib pdf scholarsportal was not downloaded correctly')
    return None


def downloadSpringerOpen(path):
    try:
        pdfTag = ch.find_element_by_xpath("//p[@class='u-marginBtmM']/a[text()='Download PDF']")
        pdfLink = pdfTag.get_attribute('href')
    except selenium.common.exceptions.NoSuchElementException:
        print('Springer open link has no PDF, returning None...')
        return None

    print(pdfLink)
    session = SessionInitializer.getSesh()
    r = session.get(pdfLink, stream=True)

    if r.status_code == 200:
        with open(path, 'wb') as f:
            r.raw.decode_content = True
            shutil.copyfileobj(r.raw, f)
        return 1

    print('ERROR: watlib pdf springeropen was not downloaded correctly')
    return None


def downloadMdpi(path):
    try:
        pdfTag = ch.find_element_by_xpath("//li/a[text()='Full-Text PDF']")
        pdfLink = pdfTag.get_attribute('href')
    except selenium.common.exceptions.NoSuchElementException:
        print('MDPI link has no PDF, returning None...')
        return None

    print(pdfLink)
    session = SessionInitializer.getSesh()
    r = session.get(pdfLink, stream=True)

    if r.status_code == 200:
        with open(path, 'wb') as f:
            r.raw.decode_content = True
            shutil.copyfileobj(r.raw, f)
        return 1

    print('ERROR: watlib pdf MDPI was not downloaded correctly')
    return None



def downloadDOAJ(href, path):
    href.click()
    if 'springeropen' in ch.current_url:
        return downloadSpringerOpen(path)
    elif 'mdpi.com' in ch.current_url:
        return downloadMdpi(path)
    else:
        return None


def downloadFromWatLib(url, path):
    ch.get(url)

    # Multi object waterloo page comes up sometimes - just go to the first one
    if 'multi.cgi?' in ch.current_url:
        link1 = ch.find_element_by_xpath("//h2[@class='exlHeadingTextDisplay']/a").get_attribute('href')
        ch.get(link1)

    try:
        #href = ch.find_element_by_link_text('Scholars Portal')
        #href = ch.find_element_by_xpath('//a[@href="javascript:openWindow(this, \'basic1\');" and text()="Scholars Portal"]')
        href = ch.find_element_by_xpath('//a[@href="javascript:openWindow(this, \'basic1\');"]')
        source = href.text
    except selenium.common.exceptions.NoSuchElementException:
        print('cannot find any link on webpage')
    except Exception as e:
        print('Couldn\'t find any text in source ' + str(e))

    if source == 'Scholars Portal':
        return downloadScholarPortal(href, path)
    elif source == 'DOAJ Directory of Open Access Journals':
        return downloadDOAJ(href, path)
    else:
        return None


# # MANUAL LOGIN
# lname = ch.find_element_by_name('pass')
# lname.send_keys('jie')
# barcode = ch.find_element_by_name('user')
# barcode.send_keys('21187005749502')
# form = ch.find_element_by_xpath('//input[@value = "Login"]')
# form.click()
# print(ch.get_cookies())
