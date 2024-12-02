import discord
from discord.ext import commands
import config
import os


bot = commands.Bot(command_prefix="!", intents=discord.Intents.all(), application_id = 1295760755613765715)


@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')

    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            await bot.load_extension(f"cogs.{filename[:-3]}")


    # Sync commands
    print("Commands have been synced.")


if __name__ == '__main__':
    bot.run(config.token)

