import discord
import json
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from webdriver_manager.chrome import ChromeDriverManager
from discord.ext import commands
from discord import Color
from icecream import ic
import time
import asyncio
import dcids as id



class Scraper(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot



    @commands.Cog.listener()
    async def on_ready(self):
        print("Scraper cog loaded")


    gay = False


    async def scrape(self):
        chrome_options = Options()
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument("--disable-gpu")
        # chrome_options.add_argument("--no-sandbox") # linux only
        # chrome_options.add_argument("--headless=new") # for Chrome >= 109
        # chrome_options.add_argument("--headless")
        # chrome_options.headless = True # also works
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

        url = "https://www.carousell.sg/search/skateboard?addRecent=true&canChangeKeyword=true&includeSuggestions=true&price_start=1&searchId=t1nH5D&sort_by=3&t-search_query_source=direct_search"

        driver.set_page_load_timeout(25)

        try:
            driver.get(url)

        except TimeoutException:
            print("Page took too long to load...")

        except Exception as e:
            # Handle any other exceptions that may occur
            print(f"An error occurred: {e}")



        # time.sleep(1000)

        # driver.find_element(By.XPATH, '//button[@aria-label="Close"]').click()
        # driver.find_element(By.XPATH, '//div[@role="dialog" and @aria-modal="true"]').click()

    
        # time.sleep(100)
        testid_divs = driver.find_elements(By.XPATH, '//div[contains(@data-testid, "listing-card-")]')

        div_content_list = []

        for index, div in enumerate(testid_divs):
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


        driver.quit()


        with open("old_data.json", "r", encoding="utf-8") as f:
            old_data = json.load(f)


        
        # with open("div_content_list.json", "w", encoding="utf-8") as file:
        #     json.dump(div_content_list, file, ensure_ascii=False, indent=4)

        # with open("temp_old_data.json", "w", encoding="utf-8") as file:
        #     json.dump(temp_old_data, file, ensure_ascii=False, indent=4)

        
        time_list_new = ['4 minutes ago', '5 minutes ago', '6 minutes ago', 
                         '7 minutes ago', '8 minutes ago', '9 minutes ago', 
                         '10 minutes ago', '11 minutes ago', '12 minutes ago', 
                         '13 minutes ago', '14 minutes ago', '15 minutes ago', 
                         '16 minutes ago', '17 minutes ago', '18 minutes ago', 
                         '19 minutes ago', '20 minutes ago', '21 minutes ago', 
                         '22 minutes ago', '23 minutes ago', '24 minutes ago', 
                         '25 minutes ago', '26 minutes ago', '27 minutes ago', 
                         '28 minutes ago', '29 minutes ago', '30 minutes ago', 
                         '31 minutes ago', '32 minutes ago', '33 minutes ago', 
                         '34 minutes ago', '35 minutes ago', '36 minutes ago', 
                         '37 minutes ago', '38 minutes ago', '39 minutes ago', 
                         '40 minutes ago', '41 minutes ago', '42 minutes ago', 
                         '43 minutes ago', '44 minutes ago', '45 minutes ago', 
                         '46 minutes ago', '47 minutes ago', '48 minutes ago', 
                         '49 minutes ago', '50 minutes ago', '51 minutes ago', 
                         '52 minutes ago', '53 minutes ago', '54 minutes ago', 
                         '55 minutes ago', '56 minutes ago', '57 minutes ago', 
                         '58 minutes ago', '59 minutes ago', '60 minutes ago', 
                         '1 hour ago', '2 hours ago', '3 hours ago', 
                         '4 hours ago', '5 hours ago', '6 hours ago', 
                         '7 hours ago', '8 hours ago', '9 hours ago', 
                         '10 hours ago', '11 hours ago', '12 hours ago', 
                         '13 hours ago', '14 hours ago', '15 hours ago', 
                         '16 hours ago', '17 hours ago', '18 hours ago', 
                         '19 hours ago', '20 hours ago', '21 hours ago', 
                         '22 hours ago', '23 hours ago', '24 hours ago']

        diff = []

        old_contents = {item['content'] for item in old_data}

        for new_item in div_content_list:
            if "theskateboardshop" in new_item['content']:
                continue # Skip this item if it contains "theskateboardshop"
            
            if "day" in new_item['content'] or "days" in new_item['content']:
                continue # Skip this item if it contains "days or day"

            if any(time in new_item['content'] for time in time_list_new):
                continue # Skip this item if it contains any time from the time_list

            if new_item['content'] not in old_contents:
                diff.append(new_item)

        ic(diff)

        if diff:
            with open("diff.json", "w", encoding="utf-8") as file:
                json.dump(diff, file, ensure_ascii=False, indent=4)

            with open("old_data.json", "w", encoding="utf-8") as json_file:
                        json.dump(div_content_list, json_file, ensure_ascii=False, indent=4)

            return diff
            
        else:
            print("IF YOU SEE THIS THAT MEANS 'DIFF' IS EMPTY")
            with open("old_data.json", "w", encoding="utf-8") as json_file:
                        json.dump(div_content_list, json_file, ensure_ascii=False, indent=4)

            print("IF YOU SEE THIS THAT MEANS IT WORKS!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
       


        
    async def send_alert(self, ctx, htmldata):
        red = Color.red()

        embed_alert = discord.Embed(
            title='ALERT! New Listing Detected',
            colour=red
        )

        content_list = []
        link_list = []
        selected_content = []
        selected_items = []

            
        for div in htmldata:
            links = div.get('links', [])
            content = div.get('content', [])

            if len(links) >= 2:
                link_list.append(links[1])

            if content:
                content_list.append(content)
                
            else:
                pass

        ic(content_list)
        # for i in range(1, 2):
        #     if i < len(link_list):
        #         selected_items.append(link_list[i])
        #         selected_content.append(content_list[i])
        

        # dick = dict(zip(content_list, link_list))
        marcus = self.bot.get_user(id.marcusid)
        dani = self.bot.get_user(id.myid)
        
        for x, y in zip(content_list, link_list):
            embed_alert.add_field(name='', value=f"{x}", inline=False)
            embed_alert.add_field(name='', value=f"[LINK HERE]({y})", inline=False)
            embed_alert.add_field(name='', value=f"<@{id.marcusid}>", inline=False)
            await marcus.send(embed=embed_alert)
            await dani.send(embed=embed_alert)
            embed_alert.clear_fields()
            await asyncio.sleep(1)





    async def toggle_logic(self, ctx):
         while self.gay == True:
            htmldata = await self.scrape()

            if htmldata:
                await self.send_alert(ctx, htmldata)
        
            else:
                pass
            
            await asyncio.sleep(180)

            if self.gay == False:
                break




    @commands.command()
    async def toggle_ws(self, ctx):
        if self.gay == False:
            await ctx.send("Web Scraping Enabled!")
            await asyncio.sleep(1)

        self.gay = not self.gay

        if self.gay == True:
            await self.toggle_logic(ctx)

        else:
            await ctx.send("Web Scraping Disabled!")
            



    # @commands.command()
    # async def send_msg(self, ctx, *, msg: str):
        
    #     await self.victim_selected.send(msg)


    # @commands.command()
    # async def test_ws(self, ctx):
    #     htmldata = await self.scrape()

    #     if htmldata:
    #         await self.send_alert(ctx, htmldata)
        
    #     else:
    #         pass




    @commands.command()
    async def ts(self, ctx):
        await ctx.send("testing scraper")
        await self.scrap()



    @commands.command()
    async def test(self, ctx):
        await ctx.send("Testoingsfgnaodergnoetdgnoaetdnoetdihj")






    

async def setup(bot):
    await bot.add_cog(Scraper(bot))