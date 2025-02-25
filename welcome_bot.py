import discord
from discord.ext import commands


import os
from dotenv import load_dotenv

# Cargar variables de entorno desde .env
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

# Verificar que el token se haya cargado correctamente
if not TOKEN:
    raise ValueError("El token no se encontró en el archivo .env")

# Configurar los intents necesarios
intents = discord.Intents.default()


intents.members = True  # Necesario para detectar nuevos miembros

# Crear instancia del bot
bot = commands.Bot(command_prefix="!", intents=intents)



# Evento cuando el bot está listo
@bot.event
async def on_ready():
    print(f'✅ Bot conectado como {bot.user}')

# Evento cuando un nuevo usuario se une al servidor
@bot.event
async def on_member_join(member):
    # Configura aquí el canal de bienvenida
    channel_id = 1334019870781735065 
    channel = bot.get_channel(channel_id)

    if channel:
        await channel.send(f'🎉 ¡Bienvenido {member.mention} a {member.guild.name}! Esperamos que la pases de putísima madre. 🚀')

# Iniciar el bot
bot.run(TOKEN)
