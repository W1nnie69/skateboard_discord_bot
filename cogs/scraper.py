import discord
import json
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from discord.ext import commands
from discord import Color
import time
import asyncio
from icecream import ic
import dcids


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
        driver = webdriver.Chrome(options=chrome_options)

        url = "https://www.carousell.sg/search/skateboard?addRecent=true&canChangeKeyword=true&includeSuggestions=true&price_start=1&searchId=t1nH5D&sort_by=3&t-search_query_source=direct_search"

        driver.get(url)

        # time.sleep(1000)

        driver.find_element(By.CSS_SELECTOR, "button.D_oX.D_biI").click()

        # time.sleep(100)
        ligma = driver.find_elements(By.CSS_SELECTOR, "div.D_tN.D_nO")

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



        with open("temp_old_data.json", "r", encoding="utf-8") as f:
            temp_old_data = json.load(f)


        
        # with open("div_content_list.json", "w", encoding="utf-8") as file:
        #     json.dump(div_content_list, file, ensure_ascii=False, indent=4)

        # with open("temp_old_data.json", "w", encoding="utf-8") as file:
        #     json.dump(temp_old_data, file, ensure_ascii=False, indent=4)

        time_list = ["23 hours ago", "22 hours ago", "21 hours ago", 
                     "20 hours ago", "19 hours ago", "18 hours ago", 
                     "17 hours ago", "16 hours ago", "15 hours ago",
                     "14 hours ago", "13 hours ago", "12 hours ago",
                     "11 hours ago", "10 hours ago", "9 hours ago",
                     "8 hours ago", "7 hours ago", "6 hours ago",
                     "5 hours ago", "4 hours ago", "3 hours ago",
                     "2 hours ago"]

        diff = []

        old_contents = {item['content'] for item in temp_old_data}

        for new_item in div_content_list:
            if "days" in new_item['content']:
                continue # Skip this item if it contains "days"

            if "day" in new_item['content']:
                continue # Skip this item if it contains "day"

            for time in time_list:
                if time in new_item['content']:
                    continue # Skip this item if it contains hours in the time_list

            if new_item['content'] not in old_contents:
                diff.append(new_item)

                
    

        with open("diff.json", "w", encoding="utf-8") as file:
            json.dump(diff, file, ensure_ascii=False, indent=4)


        with open("temp_old_data.json", "w", encoding="utf-8") as json_file:
            json.dump(div_content_list, json_file, ensure_ascii=False, indent=4)


        return diff


        
        




    async def send_alert(self, ctx, htmldata):
        red = Color.red()

        embed_alert = discord.Embed(
            title=':rotating_light::rotating_light:__**ALERT! New Listing Detected**__:rotating_light::rotating_light:',
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

        # for i in range(1, 2):
        #     if i < len(link_list):
        #         selected_items.append(link_list[i])
        #         selected_content.append(content_list[i])
        

        # dick = dict(zip(content_list, link_list))

        
        for x, y in zip(content_list, link_list):
            embed_alert.add_field(name='', value=f"{x}", inline=False)
            embed_alert.add_field(name='', value=f"[LINK HERE]({y})", inline=False)
            embed_alert.add_field(name='', value=f"<@{dcids.marcusid}><@{dcids.ryzzid}><@{dcids.danishid}>", inline=False)
            await ctx.send(embed=embed_alert)  
            embed_alert.clear_fields()
            await asyncio.sleep(1)







    # @commands.command()
    # async def toggle_ws(self, ctx):
    #     if self.gay == False:
    #         await ctx.send("Web Scraping Enabled!")
    #         await asyncio.sleep(1)

    #     self.gay = not self.gay

    #     while self.gay == True:
    #         data = await self.scrape()
    #         await self.send_alert(data)
            
    #         await asyncio.sleep(3)


    #         if self.gay == False:
    #             await ctx.send("Web Scraping Disabled!")
    #             break
            




    @commands.command()
    async def test_ws(self, ctx):
        htmldata = await self.scrape()
        await self.send_alert(ctx, htmldata)
        
    

    @commands.command()
    async def test_alert(self, ctx):
        red = Color.red()

        embed_alert = discord.Embed(
            title=':rotating_light::rotating_light:__**ALERT! New Listing Detected**__:rotating_light::rotating_light:',
            colour=red
        )

        content_list = []
        link_list = []
        selected_content = []
        selected_items = []


        with open('testing.json', 'r', encoding='utf-8') as jf:
            data = json.load(jf)
            
        for div in data:
            links = div.get('links', [])
            content = div.get('content', [])

            if len(links) >= 2:
                link_list.append(links[1])

            if content:
                content_list.append(content)
                
            else:
                pass

        for i in range(1, 2):
            if i < len(link_list):
                selected_items.append(link_list[i])
                selected_content.append(content_list[i])
        

        # dick = dict(zip(content_list, link_list))

        
        for x, y in zip(selected_content, selected_items):
            embed_alert.add_field(name='', value=f"{x}", inline=False)
            embed_alert.add_field(name='', value=f"[LINK HERE]({y})", inline=False)
            embed_alert.add_field(name='', value=f"<@{dcids.marcusid}><@{dcids.ryzzid}><@{dcids.danishid}>", inline=False)
            await ctx.send(embed=embed_alert)  
            embed_alert.clear_fields()
            await asyncio.sleep(1)

        # await ctx.send(embed=embed_alert)





    @commands.command()
    async def ts(self, ctx):
        await ctx.send("testing scraper")
        await self.scrap()



    @commands.command()
    async def test(self, ctx):
        await ctx.send("Testoingsfgnaodergnoetdgnoaetdnoetdihj")






    

async def setup(bot):
    await bot.add_cog(Scraper(bot))