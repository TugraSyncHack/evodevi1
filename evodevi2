import discord
from discord.ext import commands
import requests
import random
import json
import os


DATA_FILE = "pokemon_data.json"

def load_data():
    if not os.path.exists(DATA_FILE):
        with open(DATA_FILE, "w") as f:
            json.dump({}, f)
    with open(DATA_FILE, "r") as f:
        return json.load(f)

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)


intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)




@bot.event
async def on_ready():
    print(f"{bot.user} olarak giriş yapıldı!")
    print("Bot çalışıyor...")



@bot.event
async def on_member_join(member):
    for channel in member.guild.text_channels:
        try:
            await channel.send(f"🎉 Hoş geldiniz, {member.mention}! Pokémon macerasına hazır mısın?")
            break
        except:
            continue




@bot.command()
async def besle(ctx, pokemon_adi: str):
    user_id = str(ctx.author.id)
    data = load_data()

    # Kullanıcı yoksa oluştur
    if user_id not in data:
        data[user_id] = {}

    # Pokémon yoksa oluştur
    if pokemon_adi not in data[user_id]:
        data[user_id][pokemon_adi] = {"level": 1, "xp": 0}

    pokemon = data[user_id][pokemon_adi]

    # XP artır
    pokemon["xp"] += 10

    # Level up kontrol
    if pokemon["xp"] >= 50:
        pokemon["level"] += 1
        pokemon["xp"] = 0
        await ctx.send(f"🎉 **{pokemon_adi} seviye atladı!** Yeni seviye: {pokemon['level']}")
    else:
        await ctx.send(f"🍎 {pokemon_adi} beslendi! XP: {pokemon['xp']}/50")

    save_data(data)



@bot.command()
async def kesfet(ctx):
    await ctx.send("🔍 Çevre keşfediliyor...")

    chance = random.randint(1, 100)

    if chance <= 3:  # %3 şans
        rare_pokemon = random.choice(["mew", "lugia", "rayquaza", "mewtwo"])
        await ctx.send(f"✨ **Efsanevi bir Pokémon keşfettin: {rare_pokemon.upper()}!**")
    else:
        await ctx.send("Hiçbir şey bulamadın... belki bir dahaki sefere 🎒")




@bot.command()
async def pokemon(ctx, isim: str):
    url = f"https://pokeapi.co/api/v2/pokemon/{isim.lower()}"
    response = requests.get(url)

    if response.status_code != 200:
        await ctx.send("❌ Böyle bir Pokémon bulunamadı!")
        return

    data = response.json()

    name = data["name"]
    height = data["height"]
    weight = data["weight"]
    sprite = data["sprites"]["front_default"]

    embed = discord.Embed(
        title=f"{name.capitalize()} Bilgileri",
        description="PokeAPI üzerinden canlı veri",
        color=discord.Color.blue()
    )

    embed.add_field(name="Boy", value=height)
    embed.add_field(name="Kilo", value=weight)
    embed.set_thumbnail(url=sprite)

    await ctx.send(embed=embed)


# -------------------------
# BOTU ÇALIŞTIR
# -------------------------

bot.run("BOT_TOKENINI_YAZ")
