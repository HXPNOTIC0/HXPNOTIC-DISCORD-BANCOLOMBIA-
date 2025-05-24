import discord
from discord.ext import commands
from PIL import Image, ImageDraw, ImageFont
from datetime import datetime
from uuid import uuid4
from io import BytesIO
import pytz
import random
import asyncio
import os
from dotenv import load_dotenv

# CARGAR VARIABLES DE ENTORNO
load_dotenv()

# CONFIG HXPNOTIC
intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.members = True
bot = commands.Bot(command_prefix="!", intents=intents)

# SEMÁFORO PARA EVITAR SATURACIÓN
semaforo = asyncio.Semaphore(3)

# RUTAS HXPNOTIC
IMAGE_PATH = "climpio.png"
FONT_BOLD = "Montserrat-Bold.ttf"
FONT_REGULAR = "Montserrat-Regular.ttf"
FONT_LIGHT = "Montserrat-Light.ttf"
FONT_BIRREGULAR = "BiryaniRegular.ttf"
FONT_BIRBOLD = "BiryaniBold.ttf"
FONT_BIRSEMIBOLD = "BiryaniSemiBold.ttf"
FONT_NOYSEMI = "FrutigerNextMedium.ttf"
FONT_MYRBOLD = "Myriadprosemibold.ttf"

# COORDENADAS HXPNOTIC
COORDENADAS = {
    "comprobante": (285, 550),
    "fecha": (355, 610),
    "valor": (133, 1023),
    "nombre": (90, 1585),
    "cuenta": (90, 1645),
    "numeros": (90, 1705),
}

ROL_PERMITIDO_ID = 1375676181155942421

@bot.event
async def on_ready():
    print(f"BOT ENCENDIDO {bot.user}")

@bot.event
async def on_message(message):
    if message.author.bot:
        return
    if message.content.startswith("!cgen"):
        await bot.process_commands(message)

@bot.command(name="cgen")
async def generar_comprobante(ctx, *, mensaje: str):
    rol_autorizado = discord.utils.get(ctx.author.roles, id=ROL_PERMITIDO_ID)
    if not rol_autorizado:
        await ctx.send("**No tienes permisos para usar este comando. ❌**")
        return

    async with semaforo:
        try:
            lineas = mensaje.strip().split("\n")
            if len(lineas) != 4:
                await ctx.send("**Por favor usa el formato correcto:**\nNombre:\nCuenta:\nValor:\nNúmero de cuenta:")
                return

            nombre, cuenta, valor, numero_cuenta = [linea.strip() for linea in lineas]
            cuenta = cuenta or "Corriente - Bancolombia"
            valor = valor.replace("$", "").strip()
            numero_cuenta = numero_cuenta.replace(" ", "")

            if not numero_cuenta.isdigit() or len(numero_cuenta) not in (10, 11):
                await ctx.send("**El número de cuenta debe tener 10 o 11 dígitos.**")
                return

            if len(numero_cuenta) == 11:
                numero1, numero2, numero3 = numero_cuenta[:3], numero_cuenta[3:9], numero_cuenta[9:]
                numeros_texto = f"{numero1} - {numero2} - {numero3}"
            else:
                numeros_texto = numero_cuenta

            image = Image.open(IMAGE_PATH).convert("RGB")
            draw = ImageDraw.Draw(image)
            font_comprobante = ImageFont.truetype(FONT_REGULAR, 40)
            font_fecha = ImageFont.truetype(FONT_REGULAR, 40)
            font_valor = ImageFont.truetype(FONT_BIRBOLD, 52)
            font_signo = ImageFont.truetype(FONT_MYRBOLD, 60)
            font_nombre = ImageFont.truetype(FONT_BOLD, 37)
            font_cuenta = ImageFont.truetype(FONT_REGULAR, 33)
            font_numeros = ImageFont.truetype(FONT_NOYSEMI, 51)

            numero_comprobante = f"00000{random.randint(10000, 99999)}"
            draw.text(COORDENADAS["comprobante"], f"Comprobante No. {numero_comprobante}", font=font_comprobante, fill="black")

            bogota_tz = pytz.timezone("America/Bogota")
            fecha_actual = datetime.now(bogota_tz).strftime("%d %b %Y - %I:%M %p").lower().replace("am", "a.m.").replace("pm", "p.m.")
            draw.text(COORDENADAS["fecha"], fecha_actual, font=font_fecha, fill="black")

            draw.text((90, 1037), "$", font=font_signo, fill="black")
            draw.text(COORDENADAS["valor"], valor, font=font_valor, fill="black")
            draw.text(COORDENADAS["nombre"], nombre, font=font_nombre, fill="black")
            draw.text(COORDENADAS["cuenta"], cuenta, font=font_cuenta, fill="black")
            draw.text(COORDENADAS["numeros"], numeros_texto, font=font_numeros, fill="black")

            bio = BytesIO()
            bio.name = f"comprobante_{uuid4().hex[:6]}.png"
            image.save(bio, "PNG")
            bio.seek(0)

            await ctx.send("**COMPROBANTE GENERADO POR HXPNOTIC** 💸", file=discord.File(bio, filename=bio.name))
        except Exception as e:
            await ctx.send(f"Ocurrió un error: {e}")

# EJECUCIÓN HXPNOTIC
if __name__ == "__main__":
    bot.run(os.getenv("DISCORD_TOKEN"))
