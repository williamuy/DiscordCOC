from typing import Final 
import os
from discord import Intents, Client, Message
from responses import get_response

from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")


#Bot Setup

Intents = Intents.default()
Intents.message_content = True
client = Client(intents=Intents)

#Functionality

async def send_message(message: Message, user_message: str) -> None:
    if not user_message:
        print('(Message was empty becaues intents were not enabled probably)')
        return
    
    #For private messages that end in ?
    if is_private := user_message[0] == '?':
        user_message = user_message[1:]
        
    try:
        response: str = get_response(user_message)
        await message.author.send(response if is_private else await message.channel.send(response))
    except NotImplementedError:
        await message.channel.send('Sorry, I don\'t know how to respond to that')
        
        
        
        
@client.event
async def on_ready() -> None:
    print('Ready!')
    
@client.event
async def on_message(message: Message) -> None:
    if message.author == client.user:
        return
    
    username: str = str(message.author)
    user_message: str = message.content
    channel: str = str(message.channel)
    
    print(f'[{channel}], [username]: "{user_message}"')
    await send_message(message, user_message)
    

def main() -> None:
    client.run(TOKEN)
    
    
if __name__ == '__main__':
    main()



import discord 
from discord import app_commands
from discord.ext import commands
from dotenv import load_dotenv
import os
bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())

@bot.event
async def on_ready():
    print('Ready!')
    
    try: 
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} command(s)")
        
    except Exception as e:
        print(e)
        

@bot.tree.command(name="hello", description="Responds with a greeting")
async def hello(interaction: discord.Interaction):
    # Responds to the slash command with "Hello!"
    await interaction.response.send_message("Hello!")

load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")


from dotenv import load_dotenv
import os
bot.run(TOKEN)