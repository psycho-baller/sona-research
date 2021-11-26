# %%
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.firefox.options import Options  # for suppressing the browser
import warnings

from bs4 import BeautifulSoup as bs

Options = Options()
Options.add_argument("--headless")
with warnings.catch_warnings():
    warnings.simplefilter('ignore')
    driver = webdriver.Firefox(
        executable_path=r'C:\firefox_driver\geckodriver.exe')  # ,options=Options


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

try:
    if table_row.find('span', {'id': 'ctl00_ContentPlaceHolder1_lblNoStudies'}).text == 'No studies are available at this time.':
        print('There are currently no studies, come back next time')
except(AttributeError):
    print("THERE'S A STUDY UP!")
    study_links = table_row.findAll(
        'a', {'id': 'ctl00_ContentPlaceHolder1_repStudentStudies_ctl15_HyperlinkStudentStudyInfo'})

    links = []
    for link in study_links:
        links.append(f'{home_page}{link.get("href")}')

    num_of_links = links.__len__()
    print(f'there is {num_of_links} avalaible study') if num_of_links == 1 else print(
        f'there are {num_of_links} avalaible studies')

    # print(links)


# %%
for link in links:
    driver.get(link)
    link = driver.page_source
    #s = requests.Session()
    #link = s.get(link).content

    soup2 = bs(link, 'html.parser')
    description = soup2.find(
        'span', {'id': 'ctl00_ContentPlaceHolder1_lblLongDesc'}).get_text(' ')
    print(description)
    if input("\nIf u wanna participate in this study, press Enter, if not, type any letter then press Enter and you will see the next avalable if there is any other") == '':
        driver.find_element(
            By.ID, 'ctl00_ContentPlaceHolder1_lnkNonAdmin').click()
        driver.find_element(
            By.ID, 'ctl00_ContentPlaceHolder1_repTimeSlots_ctl00_Submit_Button').click()
    else:
        pass
