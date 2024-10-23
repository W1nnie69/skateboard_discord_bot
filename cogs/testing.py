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




class Testing(commands.Cog):
    def __init__(self, bot:commands.Bot):
        self.bot = bot



    @commands.Cog.listener()
    async def on_ready(self):
        print("STesting cog loaded")
    

    @commands.command()
    async def ts_a(self, ctx):
        red = Color.red()

        embed_alert = discord.Embed(
            title='This is a test Alert!',
            colour=red
        )

        content_list = []
        link_list = []
        selected_content = []
        selected_items = []


        with open('testing.json', 'r', encoding='utf-8') as f:
            htmldata = json.load(f)
            

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



async def setup(bot):
    await bot.add_cog(Testing(bot))

