import discord
from discord.ext import commands, tasks
from discord.utils import get
import random, os
import mariadb

try:
    conn = mariadb.connect(
            user='surt@localhost',
            password='lp',
            database='alcoholics'
            )
    print("were in")
except mariadb.Error as e:
    print(f"Error connecting to MariaDB Platform: {e}")
cur = conn.cursor()
intents = discord.Intents.all()

bot = commands.Bot(command_prefix=",", help_command = None, intents=intents)
token = "SECRET_TOKEN_USED_TO_CONNECT_TO_BOT"

@bot.event
async def on_ready():
    print("Bot online")
    await bot.change_presence(status=discord.Status.online)
    await bot.change_presence(activity=discord.Game(name="Hi! Run ,help for more help"))


@bot.command()
async def ping(ctx):
    await ctx.send(f"Pong! :ping_pong:  {round(bot.latency*1000,2)} ms")

@bot.event
async def on_message_delete(msg):
  global content
  global author
  content = msg.content
  author = msg.author.name
@bot.command()
@commands.cooldown(1,15, commands.BucketType.user)
async def snipe(ctx):
  global content
  global author
  embed = discord.Embed(title = f"{author}", description = content, color = discord.Color.blurple())
  embed.set_footer(text = f"Requested by {ctx.author.name}")
  embed.set_author(name= "Busted")
  await ctx.send(embed = embed)


@bot.event
async def on_message(message):
  global count
  if message.author == bot.user:
    return
  if not isinstance(message.channel, discord.channel.DMChannel):
    if "<@1112814634819403776>" in message.content.lower():
       await message.channel.send("Hello! My prefix is `,`. Try running `,help`")
    await bot.process_commands(message)


@bot.command()
async def verify(ctx):
    role = get(ctx.author.guild.roles, name="Visitor")
    await ctx.author.edit(roles=[role])


@bot.command()
async def nuhuh(ctx):
  await ctx.send("https://media.tenor.com/c5a_h8U1MzkAAAAC/nuh-uh-beocord.gif")

@bot.command()
async def baller(ctx):
    await ctx.send("https://tenor.com/view/roblox-baller-roblox-baller-baller-guy-ballers-gif-26937843")

@bot.command()
@commands.has_any_role("Coordinator")
async def issue(ctx, *,string):
    name = string[:string.find(" ")]
    items = string[string.find(" ")+1::]
    cur.execute("select * from issues")
    for i in cur:
        print(i)
    cur.execute("insert into issues(name, things_taken) values (?,?)",(name, items));
    conn.commit()
    await ctx.send("items issued");

ppl_allowed = ["Coordinator", "Moderator"]

@bot.command()
@commands.has_any_role(*ppl_allowed)
async def listall(ctx):
    cur.execute("select * from issues")
    for i in cur:
        id = i[0]
        name = i[1]
        items = i[2]
        date = i[3]
        status = int(i[4])
        await ctx.send(f"{id}. {name} had issued {items} on {date} [returned = {status}]")

@bot.command()
async def list(ctx):
    cur.execute("select * from issues where returned=0")
    for i in cur:
        id = i[0]
        name = i[1]
        items = i[2]
        date = i[3]
        await ctx.send(f"{id}. {name} had issued {items} on {date}")


@bot.command()
@commands.has_any_role("Coordinator")
async def rt(ctx, id):
    cur.execute("update issues set returned = 1 where id = {}".format(id))
    conn.commit()
    await ctx.send("updated")

@bot.command()
async def search(ctx, name):
    cur.execute("select * from issues where name='{}'".format(name))
    for i in cur:
        await ctx.send(i)

@bot.command()
async def help(ctx):
    embed = discord.Embed(
                title="hepl 4 u yeah",
                description = "bottom text",
                color=discord.Color.purple()
            )
    embed.add_field(
            name="Fun",
            value="baller \n nuhuh \n ping \n snipe"
            , inline = False
            )
    embed.add_field(
            name="Issue Items [Coordinator / Mod only]",
            value="issue \n rt \n list \n listall"
            , inline = False
            )
    await ctx.send(embed = embed)
bot.run(token)
