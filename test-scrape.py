from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
import json
from icecream import ic

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

buttons = driver.find_elements(By.XPATH, '//button[@aria-label="Close"]')
if len(buttons) >= 2:
    buttons[1].click()

else:
    print("No buttons lil bro")

# time.sleep(100)
ligma = driver.find_elements(By.XPATH, '//div[contains(@data-testid, "listing-card-")]')


div_content_list = []

for index, div in enumerate(ligma):
    # Extract the div content
    div_content = {
        "div_number": index + 1,
        "content": div.text
    
    }


    # Locate the <path> element inside the div and extract its 'id'
    try:
        path_element = div.find_element(By.CSS_SELECTOR, 'path[id="iconBumpOutlined"]')
        bump_Present = "Bump-found"
    except:
        bump_Present= "Not-found" # If the path with the id isn't found, set to None
        # path_element = "Not found"

    div_content["bump_Present"] = bump_Present # Add bump id to the content
    
    
    # Find links inside the current div (searching for anchor tags <a>)
    links = []
    a_tags = div.find_elements(By.TAG_NAME, "a")
    

    for a in a_tags:
        href = a.get_attribute("href")
        if href:  # Only add the href if it exists
            links.append(href)
    
    # Add the links to the div_content object
    div_content["links"] = links
    
    # Append the div content (with links) to the list
    div_content_list.append(div_content)


with open("test-scrape.json", "w", encoding="utf-8") as json_file:
    json.dump(div_content_list, json_file, ensure_ascii=False, indent=4)

