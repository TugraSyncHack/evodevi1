import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.members = True  # on_member_join çalışması için gerekli

bot = commands.Bot(command_prefix="!", intents=intents)



@bot.event
async def on_ready():
    print(f"{bot.user} olarak giriş yapıldı!")



@bot.event
async def on_member_join(member):
    for channel in member.guild.text_channels:
        try:
            await channel.send(f"Hoş geldiniz, {member.mention}!")
            break
        except:
            continue


bot.run("BOT_TOKENİNİ_BURAYA_YAZ")
