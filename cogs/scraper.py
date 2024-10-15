import discord
import requests
from discord.ext import commands
from bs4 import BeautifulSoup



class Scraper(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot



    @commands.Cog.listener()
    async def on_ready(self):
        print("Scraper cog loaded")



    async def scrap(self):
        url = "https://www.carousell.sg/"

        page = requests.get(url)

        soup = BeautifulSoup(page.text, 'html')

        print(soup)




    @commands.command()
    async def ts(self, ctx):
        await ctx.send("testing scraper")
        await self.scrap()



    @commands.command()
    async def test(self, ctx):
        await ctx.send("Testoingsfgnaodergnoetdgnoaetdnoetdihj")






    

async def setup(bot):
    await bot.add_cog(Scraper(bot))