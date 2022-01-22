import time  # remove if no timestamp needed for log file
import json
import requests
import logging
import discord
from discord.ext import commands

with open('config.json') as json_file:
    config = json.load(json_file)  

# Setting up logging
formatter = logging.Formatter('[%(levelname)s]:%(asctime)s:%(name)s:%(message)s')
logger = logging.getLogger('discord')
logger.setLevel(logging.INFO)

# handler = logging.FileHandler(filename=f'bot.log', encoding='utf-8', mode='w')  # no timestamp 
handler = logging.FileHandler(filename=f'bot{time.time()}.log', encoding='utf-8', mode='w') # with timestamp (creates unique file so that log does not get overwritten)
handler.setFormatter(formatter)
logger.addHandler(handler)

#stream_handler = logging.StreamHandler()
#stream_handler.setFormatter(formatter)
#logger.addHandler(stream_handler)

# Bot command prefix and webhook communication
bot = commands.Bot(command_prefix='/')

@bot.event
async def on_ready():
    logger.info(f'Logged in as {bot.user} (ID: {bot.user.id})')
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')

@bot.command()
async def send(ctx):
    try: 
        upload = ctx.message.attachments[0].url  # parses out URL from message
    # Issue finding photo
    except IndexError:
        await ctx.message.add_reaction('🤨')
        await ctx.send("`[!]: IndexError` couldn't find the photo!")
    
    # URL search successful
    else:
        #  Pulls the ID of the author and finds its existence in config file
        if str(ctx.message.author.id) in config['users']: 
            #  Using the author id as a key, it pulls the relevant `messageid`
            messageid = config['users'][str(ctx.message.author.id)]["messageid"] 
            url = f"https://discord.com/api/webhooks/{config['webhookid']}/{config['webhooktoken']}/messages/{messageid}"
            r = requests.patch(url, data={'content': upload})
            if r.status_code == 200:
                await ctx.message.add_reaction('✅')
                logger.info(f"SUCCESS: Taken in message from {ctx.message.author}/{ctx.message.author.id} as {upload} -> {messageid}")
            else:
                await ctx.message.add_reaction('❌')
                await ctx.send("`[!]: status_code != 200` we ran into a problem!")
                logger.warning(f"There seems to be a problem reaching specified webhook: {r.status_code} {url}")
        else: 
            await ctx.send("`[!]`: Could not match you to a webhook!")
            logger.warning(f"Could not match {ctx.message.author}/{ctx.message.author.id} to a webhook")

@bot.command()
async def beep(ctx):
    await ctx.send('boop')
    print(ctx.message.author.id)
    logger.info(f'I have been beeped: {ctx.message.author}/{ctx.message.author.id}')

bot.run(config['bottoken'])