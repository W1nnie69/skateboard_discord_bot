from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time

chrome_options = Options()
chrome_options.add_argument("--disable-extensions")
chrome_options.add_argument("--disable-gpu")
# chrome_options.add_argument("--no-sandbox") # linux only
# chrome_options.add_argument("--headless=new") # for Chrome >= 109
# chrome_options.add_argument("--headless")
# chrome_options.headless = True # also works
driver = webdriver.Chrome(options=chrome_options)

url = "https://www.carousell.sg/search/skateboard?addRecent=true&canChangeKeyword=true&includeSuggestions=true&price_start=1&searchId=t1nH5D&sort_by=3&t-search_query_source=direct_search"

driver.get(url)

# time.sleep(1000)

driver.find_element(By.CLASS_NAME, "D_mP.D_bkw").click()

# ligma = driver.find_element(By.XPATH, '//div[@id="D_ue D_oA"]')
# print(ligma)

