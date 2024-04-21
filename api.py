import os
import requests
import urllib.parse
from discord import app_commands, Interaction, Intents
from discord.ext import commands
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
COC_API_KEY = os.getenv("COC_API_KEY")

class Barcher(object):
    def __init__(self, token):
        self.requests = requests
        self.token = token
        self.api_endpoint = "https://api.clashofclans.com/v1"
        self.timeout = 30  # Define the timeout attribute here

    def get(self, uri, params=None):
        headers = {
            'Accept': "application/json",
            'Authorization': "Bearer " + self.token
        }
        url = self.api_endpoint + uri
        try:
            response = self.requests.get(url, params=params, headers=headers, timeout=self.timeout)
            response.raise_for_status()  # Raises an HTTPError if the response status is 4xx or 5xx
            return response.json()
        except requests.exceptions.HTTPError as err:
            return {"error": "HTTP error occurred", "status_code": response.status_code, "details": str(err)}
        except requests.exceptions.RequestException as err:
            return {"error": "Request exception occurred", "details": str(err)}

    def find_clan(self, tag):
        encoded_tag = urllib.parse.quote(tag)  # URL encode the clan tag
        return self.get('/clans/' + encoded_tag)

# Initialize the Clash of Clans API client with the API key
coc_client = Barcher(COC_API_KEY)

# Setting up the bot with the command prefix and intents
bot = commands.Bot(command_prefix='!', intents=Intents.all())

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}!')
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} command(s)")
    except Exception as e:
        print(f"Failed to sync commands: {e}")

@bot.tree.command(name="search_clan", description="Search for a Clash of Clans clan by tag")
@app_commands.describe(tag="The clan tag to search for")
async def search_clan(interaction: Interaction, tag: str):
    """Slash command to search for a clan by tag."""
    clan_data = coc_client.find_clan(tag)
    if 'error' in clan_data:
        await interaction.response.send_message(f"Error: {clan_data['details']}")
    else:
        # Format the clan data into a message
        clan_name = clan_data.get('name', 'No name found')
        clan_desc = clan_data.get('description', 'No description provided')
        message = f"**Clan Name:** {clan_name}\n**Description:** {clan_desc}"
        await interaction.response.send_message(message)

@bot.tree.command(name="hello")
async def hello(interaction: Interaction):
    await interaction.response.send_message(f"Hello there! {interaction.user.mention}")

@bot.tree.command(name="say")
@app_commands.describe(things_to_say="What should I say?")
async def say(interaction: Interaction, things_to_say: str):
    await interaction.response.send_message(f"{interaction.user.name} said: {things_to_say}")

bot.run(TOKEN)
