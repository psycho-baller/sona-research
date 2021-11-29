# %%
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options  # for suppressing the browser
from selenium import webdriver

import warnings
from bs4 import BeautifulSoup as bs
import webbrowser

from webdriver_manager.chrome import ChromeDriverManager


options = Options()
options.add_experimental_option('excludeSwitches', ['enable-logging'])
options.add_argument("--headless")
with warnings.catch_warnings():
    warnings.simplefilter('ignore')
    driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
# remove the options argument if u wanna see the browser open and perform the automated process

# %%
url = 'https://ucalgary.sona-systems.com'
user_ID = '<insert User ID here>'
password = '<insert Password here>'

driver.get(url)
driver.find_element(
    By.ID, "ctl00_ContentPlaceHolder1_userid").send_keys(user_ID)
driver.find_element(By.ID, "pw").send_keys(password)
element = driver.find_element(
    By.ID, "ctl00_ContentPlaceHolder1_default_auth_button")
driver.execute_script("arguments[0].click();", element)

WebDriverWait(driver, 10).until(EC.presence_of_element_located(
    (By.ID, "lnkStudySignupLink"))).click()

# %%
html = driver.page_source
home_page = 'https://ucalgary.sona-systems.com/'
soup = bs(html, 'html.parser')
table_row = soup.find('tr').parent.findNextSibling()
study_links = table_row.findAll('a')

links = set()
for link in study_links:
    links.add(f'{home_page}{link.get("href")}')

num_of_links = len(links)
if num_of_links == 0:
    driver.close()
    exit('\nThere are no studies available currently, see u later!')
print(f'\nthere is {num_of_links} available study') if num_of_links == 1 else print(
    f'\nthere are {num_of_links} available studies')

# %%
for link in links:
    driver.get(link)
    link = driver.page_source

    soup2 = bs(link, 'html.parser')
    description = soup2.find(
        'span', {'id': 'ctl00_ContentPlaceHolder1_lblLongDesc'}).get_text(' ')
    print()
    print(description)
    if input("\nIf u wanna participate in this study, press Enter, if not, type any letter then press Enter and you will see the next available if there is any other") == '':
        driver.find_element(
            By.ID, 'ctl00_ContentPlaceHolder1_lnkNonAdmin').click()
        driver.find_element(
            By.ID, 'ctl00_ContentPlaceHolder1_repTimeSlots_ctl00_Submit_Button').click()
        driver.find_element(
            By.ID, 'ctl00_ContentPlaceHolder1_Submit_Button').click()

        if driver.find_element(By.ID, 'ctl00_SystemMessageLabel').text == 'Sign-up Successful':
            if input('\nYou got signed up!, press Enter if u wanna start the research study, otherwise, type any letter then press Enter') == '':
                study_link = driver.find_element(
                    By.ID, 'ctl00_ContentPlaceHolder1_lnkWebsite').get_attribute('href')
                driver.close()
                print('\nEnjoy!')
                webbrowser.open(study_link)
            else:
                driver.close()
                print(
                    '\nYou should recieve an email anytime now with the research link, have a woderful day')
        else:
            print(
                "Either there's a problem with the code or the sign up was unsucessful, probably the former lol, plz lmk if u got this error")
