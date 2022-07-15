import os
import discord
from dotenv import load_dotenv
import random

#Read in enviorment viariables
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
GUILDID = int(os.getenv('DISCORD_GUILD_ID'))

#initialize bot client
intents = discord.Intents.default()
intents.members = True
intents.messages = True
client = discord.Client(intents = intents)

#################################
#event listeners
################################

#when the bot is initilized
@client.event
async def on_ready():
	guild = discord.utils.find(lambda g: g.id == GUILDID, client.guilds )
	print(
	f'{client.user} has connected to Discord! \n'
	f'{guild.name} (id: {guild.id})'
	)
			

	members = '\n - '.join(member.name for member in guild.members)
	print (f'Guild Members: \n - {members} ')

@client.event
async def on_member_join(member):
	await member.create_dm()
	await member.dm_channel.send(
		f'Hi {member.name}, Welcome to my Discord server!'
	)

@client.event
async def on_message(message):
	if message.author == client.user:
		return
	
	responses = ["hallo", "hello", "ola"]
	if message.content == 'hallo':
		response = random.choice(responses)
		await message.channel.send(response)

@client.event
async def on_error(event, *args, **kwargs):
	with open('err.log', 'a') as f:
		if event == 'on_message':
			f.write(f'Unhandled message: { args[0]} \n')
		else:
			raise

#start the actual bot
client.run(TOKEN)