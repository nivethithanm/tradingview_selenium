import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions

chrome_options = ChromeOptions()
chrome_options.add_argument("--user-data-dir=selenium")
# ADD CHROMEDRIVER PATH
driver = webdriver.Chrome(executable_path = 'CHROMEDRIVER_PATH_HERE', options=chrome_options)
driver.get('http://tradingview.com/')
time.sleep(45)  # Time to enter credentials
driver.quit()

firefox_options = FirefoxOptions()
firefox_options.add_argument("--user-data-dir=selenium")
driver = webdriver.Firefox(options=firefox_options)
chrome_options.add_argument("user-data-dir=selenium")
driver.get('http://tradingview.com/')
time.sleep(45)  # Time to enter credentials
driver.quit()
