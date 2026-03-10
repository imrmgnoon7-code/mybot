import discord
from discord.ext import commands
import asyncio
from flask import Flask
from threading import Thread

# --- سيرفر وهمي عشان الموقع ما يطفي البوت ---
app = Flask('')
@app.route('/')
def home(): return "Bot is Alive!"
def run(): app.run(host='0.0.0.0', port=8080)
def keep_alive():
    t = Thread(target=run)
    t.start()

# --- إعدادات البوت ---
intents = discord.Intents.default()
intents.voice_states = True
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

TOKEN = 'MTQ4MDk3MjQzNzMxNDA3Njc2Mg.GFc0_Z.mhsSWk9bRUHPa8ZxvVfI0QeHHfjcwG6JCKolyU'
TARGET_CHANNEL_ID = 1399602622914367679

@bot.event
async def on_ready():
    print(f'✅ {bot.user} is online!')
    channel = bot.get_channel(TARGET_CHANNEL_ID)
    if channel:
        try: await channel.connect()
        except: pass

@bot.event
async def on_voice_state_update(member, before, after):
    if member.id == bot.user.id: return
    if after.channel and after.channel.id == TARGET_CHANNEL_ID:
        if before.channel is None or before.channel.id != after.channel.id:
            vc = discord.utils.get(bot.voice_clients, guild=member.guild)
            if vc and not vc.is_playing():
                vc.play(discord.FFmpegPCMAudio('welcome.mp3'))

# تشغيل السيرفر والبوت
keep_alive()

bot.run(TOKEN)
