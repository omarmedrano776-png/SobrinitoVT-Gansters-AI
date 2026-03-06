import discord
import os
import google.generativeai as genai
from discord.ext import commands

# Configuramos las llaves desde los Secrets (el candado de Replit)
DISCORD_TOKEN = os.environ.get("DISCORD_TOKEN")
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

# Configurar Google Gemini
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-1.5-pro')

# Configurar Bot
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f'¡SobrinitoVT|Gan está en línea como {bot.user}!')

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    # El bot responde si lo mencionan o por mensaje directo
    if bot.user in message.mentions or isinstance(message.channel, discord.DMChannel):
        content = message.content.replace(f'<@{bot.user.id}>', '').strip()
        
        async with message.channel.typing():
            try:
                response = model.generate_content(content)
                response_text = response.text
                
                # Dividir mensajes largos para Discord
                for i in range(0, len(response_text), 2000):
                    await message.channel.send(response_text[i:i+2000])
            except Exception as e:
                print(f"Error: {e}")
                await message.channel.send("Lo siento, tuve un error al procesar tu mensaje.")
                
    await bot.process_commands(message)

# Ejecutar bot
bot.run(DISCORD_TOKEN)
