from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
import json

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

#SAVING USING TXT FILE
# with open('test.txt', 'w', encoding='utf-8') as file:
#     for index, div in enumerate(ligma):
#         content = div.text
#         file.write(f"Content of div {index + 1}:\n")
#         file.write(content + "\n\n")



#SAVING USING JSON FILE
# div_html_dict = {f"div_{index + 1}": div.get_attribute("outerHTML") for index, div in enumerate(ligma)}

div_content_list = []

for index, div in enumerate(ligma):
    # Extract the div content
    div_content = {
        "div_number": index + 1,
        "content": div.text
    }
    
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


with open("testing.json", "w", encoding="utf-8") as json_file:
    json.dump(div_content_list, json_file, ensure_ascii=False, indent=4)

