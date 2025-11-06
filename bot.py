import discord, random, datetime
from discord import app_commands
from discord.ext import commands
from flask import Flask
from threading import Thread

# --- tiny web page so Render/UptimeRobot can ping it ---
app = Flask(__name__)

@app.route('/')
def home():
    return "Stupid Bot is awake!"

def run():
    app.run(host="0.0.0.0", port=8080)

Thread(target=run).start()
# --------------------------------------------------------

intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix="!", intents=intents)

start_time = datetime.datetime.utcnow()

@bot.event
async def on_ready():
    print(f"{bot.user} is online!")
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} slash commands.")
    except Exception as e:
        print(e)

# --- /randomping ---
@bot.tree.command(name="randomping", description="Ping a random person with a meme.")
async def randomping(interaction: discord.Interaction):
    members = [m for m in interaction.guild.members if not m.bot]
    if not members:
        await interaction.response.send_message("No people to ping!", ephemeral=True)
        return
    target = random.choice(members)
    memes = [
        "https://i.imgur.com/funny1.jpg",
        "https://i.imgur.com/funny2.jpg",
        "https://i.imgur.com/funny3.jpg"
    ]
    meme = random.choice(memes)
    embed = discord.Embed(title="Random Meme!", color=discord.Color.blurple())
    embed.set_image(url=meme)
    await interaction.response.send_message(f"{target.mention}, you’ve been chosen!", embed=embed)

# --- /hello ---
@bot.tree.command(name="hello", description="Say hello to the bot.")
async def hello(interaction: discord.Interaction):
    await interaction.response.send_message("Hey there! I’m Stupid Bot 👋")

# --- /coinflip ---
@bot.tree.command(name="coinflip", description="Flip a coin.")
async def coinflip(interaction: discord.Interaction):
    await interaction.response.send_message(f"The coin landed on **{random.choice(['Heads', 'Tails'])}**!")

# --- /roll ---
@bot.tree.command(name="roll", description="Roll a 6-sided die.")
async def roll(interaction: discord.Interaction):
    await interaction.response.send_message(f"You rolled a 🎲 **{random.randint(1,6)}**")

# --- /info ---
@bot.tree.command(name="info", description="Shows info about the bot.")
async def info(interaction: discord.Interaction):
    uptime = datetime.datetime.utcnow() - start_time
    embed = discord.Embed(title="Stupid Bot Info", color=discord.Color.gold())
    embed.add_field(name="Creator", value="You 😎", inline=True)
    embed.add_field(name="Servers", value=f"{len(bot.guilds)}", inline=True)
    embed.add_field(name="Uptime", value=str(uptime).split('.')[0], inline=False)
    embed.set_footer(text="Made with ❤️ by you")
    await interaction.response.send_message(embed=embed)

# --- /help ---
@bot.tree.command(name="help", description="Shows all available commands.")
async def help_cmd(interaction: discord.Interaction):
    embed = discord.Embed(title="Stupid Bot Commands", color=discord.Color.green())
    embed.add_field(name="/randomping", value="Ping a random member with a meme.", inline=False)
    embed.add_field(name="/hello", value="Say hi to the bot.", inline=False)
    embed.add_field(name="/coinflip", value="Flip a coin.", inline=False)
    embed.add_field(name="/roll", value="Roll a 6-sided die.", inline=False)
    embed.add_field(name="/info", value="Shows bot information.", inline=False)
    embed.add_field(name="/help", value="Shows this help menu.", inline=False)
    await interaction.response.send_message(embed=embed)
# --------------------------------------------------------

bot.run("YOUR_TOKEN_HERE")
