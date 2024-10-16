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

driver.find_element(By.CSS_SELECTOR, "button.D_oX.D_biI").click()

# time.sleep(100)
ligma = driver.find_elements(By.CSS_SELECTOR, "div.D_tN.D_nO")
 
with open("test.txt", "a"):
    for index, div in enumerate(ligma):
        content = div.text



