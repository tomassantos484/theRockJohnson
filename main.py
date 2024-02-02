#Importing Libraries & Modules
import discord
import os
import random
import giphy_client
from giphy_client.rest import ApiException
from rpschoices import RPS_CHOICES
from discord.ext import commands
from discord import app_commands
from dotenv import load_dotenv

#Loading Keys
load_dotenv()
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
GIPHY_KEY = os.getenv('GIPHY_KEY')

#Creating Bot
client = commands.Bot(command_prefix = '!', intents=discord.Intents.all())

#On Ready Event
@client.event
async def on_ready():
    print("It's about drive, it's about power. We stay hungry, we devour. Put in the work, put in the hours, and take what's ours.")
    await client.change_presence(activity=discord.Game(name="Rock, Paper, Scissors"))
    try: 
        #Syncing Slash Commands
        synced = await client.tree.sync()
    except Exception as e:
        print(e)

#Test Command with random emoji
@client.tree.command(name= "testing" , description= "Testing, Testing, 1, 2, 3!")
async def testing(interaction: discord.Interaction):
    #Random emoji
    emojiList = ["😃", "😊", "🎉", "🤖", "👍", "❤️", "🔥", "🚀", "💡"]
    emoji = random.choice(emojiList)

    #Test Statement
    await interaction.response.send_message(f"Testing, Testing, 1, 2, 3! {emoji}", ephemeral=False)

#Storing active challenges (coming soon)
active_challenges = {}

#Rock, Paper, Scissors Game
@client.tree.command(name="challenge", description="Play Rock, Paper, Scissors!")
async def challenge(interaction: discord.Interaction, choice: str):
    #GIPHY API for use after each game
    api_instance = giphy_client.DefaultApi()
    try:
        api_response = api_instance.gifs_search_get(GIPHY_KEY, q = "Dwayne Johnson", rating="g")
        random_gif_list = list(api_response.data)
        gif_selection = random.choice(random_gif_list)

        emb = discord.Embed(
            title= "", 
            color= discord.Color.red()
            )
        emb.set_image(url=f'https://media.giphy.com/media/{gif_selection.id}/giphy.gif')
        emb.set_footer(text = "Powered by GIPHY", icon_url = "attachment://image.gif")

    except ApiException as e:
        print("Exception when calling DefaultApi->gifs_random_get: %s\n" % e)
        await interaction.response.send_message("Sorry, I couldn't find a gif for that.", ephemeral=True)

    #Beginning of Game Logic
    if choice.lower() not in RPS_CHOICES:
        await interaction.response.send_message("Please choose rock, paper, or scissors.", ephemeral=True)
        return
    
    #Determining Winner
    async def determine_winner(player_choice, bot_choice):
        if player_choice == bot_choice:
            await interaction.response.send_message(f"You chose {choice.lower()} and The Rock chose {bot_choice}. It's a tie!", embed=emb, ephemeral=False)
        elif (player_choice == 'rock' and bot_choice == 'scissors') or\
            (player_choice == 'scissors' and bot_choice == 'paper') or\
            (player_choice == 'paper' and bot_choice == 'rock'):
            await interaction.response.send_message(f"You chose {choice.lower()} and The Rock chose {bot_choice}. Congrats, {interaction.user.mention}, you have WON!", embed=emb, ephemeral=False)
        else:
            await interaction.response.send_message(f"You chose {choice.lower()} and The Rock chose {bot_choice}. The Rock has WON!", embed=emb, ephemeral=False)
   
    choice = choice.lower()
    bot_choice = random.choice(list(RPS_CHOICES.keys()))
    #Calling function to determine winner
    await determine_winner(choice.lower(), bot_choice)

#Main
client.run(DISCORD_TOKEN)
