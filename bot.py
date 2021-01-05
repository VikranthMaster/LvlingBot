import discord
from discord.ext import commands
from discord import DMChannel
import os
import json
import asyncio

client = commands.Bot(command_prefix=">")
client.remove_command("help")

@client.event
async def on_ready():
    print("Bot is ready !")
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=">help"))


@client.command()
async def hello(ctx):
    await ctx.send(f"Hello {ctx.message.author.mention}")

@client.command()
async def create(ctx, code, stime, duration):
    embed = discord.Embed(
        title="Forest",
        color = discord.Color.blue()
    )   
    try:
        embed.add_field(name = "Hosted by: ", value = ctx.message.author.mention, inline = False)
        embed.add_field(name = "Code: ", value = code, inline = False)
        embed.add_field(name = "Starting Time: ", value = stime, inline = False)
        embed.add_field(name = "Duration: ", value = duration, inline = False)

        await ctx.send(embed=embed)

        user = await client.fetch_user(ctx.message.author.id)
        await DMChannel.send(user, f"Hello there, You have hosted a forest session at **{stime}** and code is **{code}** of **{duration}**mins")

    except:
        await ctx.send("Sorry, but give the full parameters required or type >help for the more commands")

@client.command()
async def ping(ctx):
    embed = discord.Embed(
        color= discord.Color.blue()
    )
    embed.add_field(name = "Ping", value= "Pong! {0}".format(round(client.latency, 1)), inline = False)

    await ctx.send(embed=embed)


@client.event
async def on_member_join(member):
    with open('users.json','r') as f:
        users = json.load(f)

    await update_data(users, member)

    with open('users.json','w') as f:
        json.dump(users,f)

@client.event
async def on_message(message):
    with open('users.json','r') as f:
        users = json.load(f)
    
    await update_data(users, message.author)
    await add_experience(users, message.author, 5)
    await level_up(users, message.author, message.channel)

    with open('users.json','w') as f:
        json.dump(users,f)

    await client.process_commands(message)

async def update_data(users,user):
  if not str(user.id) in users:
      users[str(user.id)] = {}
      users[str(user.id)]['experience'] = 0
      users[str(user.id)]['level'] = 1
    
async def add_experience(users, user, exp):
  users[str(user.id)]['experience'] += exp

async def level_up(users,user, channel):
  experience = users[str(user.id)]['experience']
  lvl_start = users[str(user.id)]['level']
  lvl_end = int(experience ** (1/4))

  if lvl_start < lvl_end:
      await channel.send(f'GG!! {user.mention} u have leveled upto **{lvl_end}**!')
      users[str(user.id)]['level'] = lvl_end

@client.command()
async def level(ctx, member: discord.Member = None):
  if not member:
    id = ctx.message.author.id
    with open('users.json', 'r') as f:
      users = json.load(f)
      lvl = users[str(id)]['level']
      await ctx.send(f'{member.mention}You are at level **{lvl}**!')
  else:
    id = member.id
    with open('users.json', 'r') as f:
      users = json.load(f)
      lvl = users[str(id)]['level']
      await ctx.send(f'{member.mention} is at level **{lvl}**!')

def get_top_experience():
  with open('users.json', 'r') as f:
    users = json.load(f)
  usersss = {}
  for i in users.keys():
    usersss[i] =  users[f'{i}']['experience']
  rank = sorted(usersss, key=usersss.get, reverse=True)
  return rank

# @client.command()
# async def rank(ctx):
#   rank = get_top_experience()
#   id = ctx.author.id
#   num_rank = rank.index(str(id))
#   await ctx.send(f'{ctx.author.mention} is at level {num_rank} and at rank')

@client.command()
async def rank(ctx, member: discord.Member = None):
  rank = get_top_experience()
  if not member:
    id = ctx.author.id
    with open('users.json', 'r') as f:
      users = json.load(f)
      lvl = users[str(id)]['level']
      num_rank = rank.index(str(id))
      await ctx.send(f'{ctx.author.mention} your rank is #**{num_rank + 1}**')
  else:
    id = member.id
    with open('users.json', 'r') as f:
      users = json.load(f)
      lvl = users[str(id)]['level']
      num_rank = rank.index(str(id))
      await ctx.send(f'{member.mention} is at level **{lvl}** and at rank #**{num_rank + 1}**!')


@client.command()
async def help(ctx):
  embed  = discord.Embed(title="Bot Help", colour=discord.Color.blue())

  embed.add_field(name="Forest", value = "Type >create {code} {starting time} {duration}. Dont include brackets", inline=False)
  embed.add_field(name="Hello", value="Type >hello, whenever u are feeling lonely", inline=False)
  embed.add_field(name="Levels", value="Type >level to check your level, you can check ur frinds levels too", inline=False)
  embed.add_field(name="Rank", value="Type >rank to check ur rank, you can check ur friends rank too", inline=False)
  embed.add_field(name="ping", value="Type >ping to check ur ping", inline=False)

  await ctx.send(embed=embed)
  
  client.run('TOKEN')
