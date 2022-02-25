import os
import time
from dotenv import load_dotenv
from discord.ext import commands, tasks

from utils import *

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

bot = commands.Bot(command_prefix="!")


@bot.event
async def on_ready():
    print(f"{bot.user.name} has connected to Discord!")


async def fetcher(ctx):
    print("📙 Fetcher function called!")
    prob_list = get_problems_from_csv()
    res = f""""""
    for i in range(len(prob_list)):
        res += "{}. {} - {} \n".format(i + 1, prob_list[i][0], prob_list[i][1])
    await ctx.send(res)


@tasks.loop(hours=24)
async def called_once_a_day(ctx):
    print("📙 Called once a day!")
    try:
        await get_problems()
        await fetcher(ctx)
    except Exception as e:
        print(e)


@bot.command(name="lc")
async def execute(ctx):
    await fetcher(ctx)


bot.run(TOKEN)
