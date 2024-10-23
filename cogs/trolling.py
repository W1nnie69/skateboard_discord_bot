import discord
from discord.ext import commands
from icecream import ic
import asyncio
import dcids as id



class Trolling(commands.Cog):
    def __init__(self, bot: commands.bot):
        self.bot = bot


    @commands.Cog.listener()
    async def on_ready(self):
        print("Trolling cog loaded")

    

    @commands.command()
    async def sel_victim(self, ctx, index: str):
        phonebook = [id.marcusid, id.myid, id.ryzzid, id.danishid, id.rusid]

        if index == "show":
            await ctx.send("1:Marcus, 2:Dani, 3:Ryzz, 4:Danish, 5:Rus")

        elif index:
            xedni = int(index)
            x = phonebook[xedni - 1]
            self.victim_selected = self.bot.get_user(x)

            ic(x)
            ic(self.victim_selected)


            if xedni == 1:
                await ctx.send("Marcus selected")
            elif xedni == 2:
                await ctx.send("Dani selected")
            elif xedni == 3:
                await ctx.send("Ryzz selected")
            elif xedni == 4:
                await ctx.send("Danish selected")
            elif xedni == 5:
                await ctx.send("Rus selected")
            else:
                await ctx.send("Select only 1 to 5 dumbass")




    @commands.command()
    async def send_msg(self, ctx, *, msg: str):
        
        await self.victim_selected.send(msg)




async def setup(bot):
    await bot.add_cog(Trolling(bot))