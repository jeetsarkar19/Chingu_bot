#Coding the trial discord bot
import os
from discord.ext import commands
import discord
from dotenv import load_dotenv

#few variables for initialization
ctr = 0
banned = []
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN') #Secret Token from the .env file
GUILD = os.getenv('DISCORD_GUILD')
chingu= commands.Bot(command_prefix="&") #Setting up an instance and also a prefix

fh = open(r"D:\project\Discord bot\rule.txt","r") #File containing all the rules list
rules = fh.readlines()
fo = open(r"D:\project\Discord bot\banned.txt","r") #File containing all the rules list
for line in fo:
	element = line.rstrip()
	banned.append(element)
fo.close()
@chingu.event
async def on_ready(): #Bot start-up command
	print(f'{chingu.user} has connected to Discord! \n')
	
@chingu.command(aliases=['hello','what up','sup','hey','heya','hi','yo','helo']) #greet command
async def greet(ctx): 
	await ctx.send("Hey, there friend. This is your friendly bot, Chingu. At your service")

@chingu.command() #Rule display command
async def rule(ctx,*,number):
	await ctx.send(rules[int(number)-1])
@chingu.command() #kick members command
@commands.has_permissions(kick_members = True)
async def kick(ctx,member : discord.Member,*,reason="no reason needed by Mods"):
	await member.send('You have been removed from the server')
	await member.kick(reason=reason)
	await ctx.send(f'{discord.Member} has been kicked from the server')
@chingu.command() #Ban members command 
@commands.has_permissions(ban_members = True)
async def ban(ctx, member: discord.Member,*,reason="None"): #members are discord objects and can be tagged
	await member.ban(reason=reason)#reason shows up in the audit log
	#await 
@chingu.command() #unban members command
@commands.has_permissions(ban_members = True)
async def unban(ctx,*,member):
	userban = await ctx.guild.bans() #list of banned members from the server
	member_name, member_disc = member.split("#") #username being split in dicord into names and discriminator

	for banned in userban: 
		BanUser = banned.user #user represents a banned user from the list.
		if(BanUser.name, BanUser.discriminator) == (member_name,member_disc):
			#await BanUser.send(f'You have been added back to {discord.server}')
			await ctx.guild.unban(BanUser)
			await ctx.send(f'{BanUser} has been restored in the server')
			#await BanUser.send(f'You have been added back to {discord.server}')
			break
		else:
			await ctx.send("User is not found")
	return 
@chingu.event
async def on_message(msg):
	for word in banned:
		if word in msg.content:
			await msg.delete()
			await msg.author.send(f'Your message has been deleted for the usage of an abusive word.')
		await chingu.process_commands(msg)

chingu.run(TOKEN)