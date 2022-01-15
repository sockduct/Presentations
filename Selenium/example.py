# Note:  Poorly structured code - merely to illustrate basic Selenium usage!!!

# Selenium WebDriver:
from selenium import webdriver

# For 4.x:
from selenium.webdriver.chrome.service import Service

# Automated browser driver selection and download:
from webdriver_manager.chrome import ChromeDriverManager

# Create driver instance:
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

# Adjust as necessary:
WAIT_TIME = 3

# Add implicit wait time - allow time for everything to load on page:
driver.implicitly_wait(WAIT_TIME)

TEST_URL = 'app.example.com'
ACCESS_USERNAME = 'accessuser'
ACCESS_PASSWORD = 'accesspass'

# Initial access login:
driver.get(f'https://{ACCESS_USERNAME}:{ACCESS_PASSWORD}@{TEST_URL}')

# To support By.<name> in find_element:
from selenium.webdriver.common.by import By

# Site login credentials:
SITE_USERNAME = 'test@example.com'
SITE_PASSWORD = 'testpass'

# App - user login:
driver.find_element(By.ID, 'email').send_keys(SITE_USERNAME)
driver.find_element(By.ID, 'password').send_keys(SITE_PASSWORD)
driver.find_element(By.XPATH, '//*[@class="login-button"]/button').click()

# Select June, 2021 Calendar:
driver.find_element(By.CLASS_NAME, 'select_month').click()
driver.find_element(By.XPATH,
    '//select[@class="select_month form-control month_dp"]/option[@value="06"]').click()
driver.find_element(By.ID, 'calendar-year-dp').click()
driver.find_element(By.XPATH,
    '//select[@id="calendar-year-dp"]/option[@value="2021"]').click()

# Select June 15, 2021 Meeting:
driver.find_element(By.LINK_TEXT, 'Committee Meeting').click()

# To support Selenium 4 relative locators:
from selenium.webdriver.support.relative_locator import locate_with

# Find PDF URL for Meeting:
agenda_text = driver.find_element(By.XPATH,
    '//td/div[contains(text(), '
    '"Notice - June 15 2021 Planning Committee.pdf")]')
pdf_url = driver.find_element(locate_with(By.TAG_NAME, 'a').
            to_right_of(agenda_text)).get_attribute('href')

# To retrieve and parse PDF:
from io import BytesIO
from urllib import request
from PyPDF2 import PdfFileReader

# Download PDF to a byte stream:
with request.urlopen(pdf_url) as resp:
    pdf_stream = BytesIO(resp.read())

# Parse PDF:
pdf_doc = PdfFileReader(pdf_stream)
pdf_page = pdf_doc.getPage(0)
pdf_text = pdf_page.extractText().replace('\n', '').lower()

# Define Document Checks and Validate PDF:
page_checks = ['public notice regarding', 'june 15, 2021, 10:00 a.m. meeting '
               'of the planning committee of the company board of directors']
if any(page_check not in pdf_text for page_check in page_checks):
    print('Wrong Document...Dooooh!')
else:
    print('Hooray - all tests pass!!!')
