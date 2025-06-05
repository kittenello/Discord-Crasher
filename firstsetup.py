from pystyle import Colors, Write, Center
import json
import os
import sys
import requests
import aiohttp
import asyncio
import webbrowser

def run_setup(language):
    os.system('cls' if os.name == 'nt' else 'clear')
    
    # Language-specific text
    texts = {
        "ru": {
            "banner": """
╔════════════════════════════════╗
║    Crash Discord Free Version  ║
║  (Russian&Русский язык только) ║
╚════════════════════════════════╝
""",
            "user_id_prompt": ">> ID твоего личного аккаунта дискорда: ",
            "bot_id_prompt": ">> ID твоего бота: ",
            "token_prompt": ">> Токен бота: ",
            "server_id_prompt": ">> Ты сможешь потом поменять\n>> ID сервера которого крашнуть: ",
            "success_banner": """
╔════════════════════════════════╗
║  Setup Completed Successfully! ║
╚════════════════════════════════╝
""",
            "config_saved": "\nКонфиг сохранен вот его данные:",
            "target_server": "- Target Server: {server_name} ({server_id})",
            "config_success": "\n\nКонфиг успешно сохранен! Начинаю запуск основного скрипта.",
            "unknown_server": "Unknown"
        },
        "en": {
            "banner": """
╔════════════════════════════════╗
║    Crash Discord Free Version  ║
║      (English Language Only)   ║
╚════════════════════════════════╝
""",
            "user_id_prompt": ">> Your Discord account ID: ",
            "bot_id_prompt": ">> Your bot's ID: ",
            "token_prompt": ">> Bot token: ",
            "server_id_prompt": ">> You can change this later\n>> Target server ID to crash: ",
            "success_banner": """
╔════════════════════════════════╗
║  Setup Completed Successfully! ║
╚════════════════════════════════╝
""",
            "config_saved": "\nConfiguration saved, here are the details:",
            "target_server": "- Target Server: {server_name} ({server_id})",
            "config_success": "\n\nConfiguration saved successfully! Starting the main script.",
            "unknown_server": "Unknown"
        }
    }

    # Select language texts
    lang_text = texts[language]
    
    Write.Print(Center.XCenter(lang_text["banner"]), Colors.red_to_blue, interval=0.0025)
    print("\n")

    config = {
        "USER_ID": Write.Input(lang_text["user_id_prompt"], Colors.red_to_white),
        "BOT_ID": Write.Input(lang_text["bot_id_prompt"], Colors.red_to_white),
        "TOKEN": Write.Input(lang_text["token_prompt"], Colors.red_to_white),
        "SERVER_ID": Write.Input(lang_text["server_id_prompt"], Colors.red_to_white),
    }

    try:
        headers = {"Authorization": f"Bot {config['TOKEN']}"}
        response = requests.get(
            f"https://discord.com/api/v9/guilds/{config['SERVER_ID']}", 
            headers=headers
        )
        server_name = response.json().get("name", lang_text["unknown_server"]) if response.status_code == 200 else lang_text["unknown_server"]
    except:
        server_name = lang_text["unknown_server"]

    full_config = {
        **config,
        "SERVER": {
            "id": config["SERVER_ID"],
            "name": server_name
        },
        "LANGUAGE": language
    }

    if not os.path.exists("configs"):
        os.makedirs("configs")

    with open("configs/setup.json", "w") as f:
        json.dump(full_config, f, indent=4)

    os.system('cls' if os.name == 'nt' else 'clear')
    Write.Print(Center.XCenter(lang_text["success_banner"]), Colors.green_to_blue, interval=0.0025)

    print(lang_text["config_saved"])
    print(f"- User ID: {config['USER_ID']}")
    print(f"- Bot ID: {config['BOT_ID']}")
    print(f"- Bot Token: {config['TOKEN']}")
    print(lang_text["target_server"].format(server_name=server_name, server_id=config["SERVER_ID"]))

    Write.Print(lang_text["config_success"], Colors.green_to_white)
    os.system("python main.py" if os.name == 'nt' else "python3 main.py")
    sys.exit()

async def check_update(language):
    texts = {
        "ru": {
            "version_check_fail": "\n>> Не удалось получить актуальную версию скрипта.",
            "error_connecting": "\n>> Ошибка при подключении к GitHub: {error}",
            "version_up_to_date": "\n>> У вас установлена актуальная версия {version}",
            "version_outdated": "\n>> Ваша версия: {local_version}, доступна новая: {remote_version}",
            "update_prompt": "\n>> Хотите перейти на страницу скачки? [Y/N]: ",
            "confirm_decline": "\n>> Вы точно отказываетесь? Это может вызвать ошибки, подтвердите еще раз [Y/N]: ",
            "declined_update": "\n>> Вы отказались от обновления, возможно будут ошибки в скрипте.\n"
        },
        "en": {
            "version_check_fail": "\n>> Failed to retrieve the latest script version.",
            "error_connecting": "\n>> Error connecting to GitHub: {error}",
            "version_up_to_date": "\n>> You are running the latest version {version}",
            "version_outdated": "\n>> Your version: {local_version}, new version available: {remote_version}",
            "update_prompt": "\n>> Would you like to visit the download page? [Y/N]: ",
            "confirm_decline": "\n>> Are you sure you want to decline? This may cause errors, confirm again [Y/N]: ",
            "declined_update": "\n>> You declined the update, errors may occur in the script.\n"
        }
    }

    lang_text = texts[language]

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

def select_language():
    os.system('cls' if os.name == 'nt' else 'clear')
    Write.Print(Center.XCenter("""
╔════════════════════════════════╗
║  Select Language / Выбор языка ║
║  1. Русский (RU)               ║
║  2. English (EN)               ║
╚════════════════════════════════╝
"""), Colors.red_to_white, interval=0.0025)
    choice = Write.Input("\n>> Choose: ", Colors.red_to_white)
    return "ru" if choice == "1" else "en"

if __name__ == "__main__":
    language = select_language()
    asyncio.run(check_update(language))
    if not os.path.exists("configs/setup.json"):
        run_setup(language)
    else:
        os.system("python main.py" if os.name == 'nt' else "python3 main.py")