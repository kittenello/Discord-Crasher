from pystyle import Colors, Write, Center
import json
import os
import sys
import requests

def run_setup():
    os.system('cls' if os.name == 'nt' else 'clear')
    Write.Print(Center.XCenter("""
╔════════════════════════════════╗
║    Crash Discord Free Version  ║
║  (Russian&Русский язык только) ║
╚════════════════════════════════╝
"""), Colors.red_to_blue, interval=0.0025)

    print("\n")

    config = {
        "USER_ID": Write.Input(">> ID твоего личного аккаунта дискорда: ", Colors.red_to_white),
        "BOT_ID": Write.Input(">> ID твоего бота: ", Colors.red_to_white),
        "TOKEN": Write.Input(">> Токен бота: ", Colors.red_to_white),
        "SERVER_ID": Write.Input(">> Ты сможешь потом поменять\n>> ID сервера которого крашнуть: ", Colors.red_to_white),
    }

    try:
        headers = {"Authorization": f"Bot {config['TOKEN']}"}
        response = requests.get(
            f"https://discord.com/api/v9/guilds/{config['SERVER_ID']}", 
            headers=headers
        )
        server_name = response.json().get("name", "Unknown") if response.status_code == 200 else "Unknown"
    except:
        server_name = "Unknown"

    full_config = {
        **config,
        "SERVER": {
            "id": config["SERVER_ID"],
            "name": server_name
        }
    }

    if not os.path.exists("configs"):
        os.makedirs("configs")

    with open("configs/setup.json", "w") as f:
        json.dump(full_config, f, indent=4)

    os.system('cls' if os.name == 'nt' else 'clear')
    Write.Print(Center.XCenter("""
╔════════════════════════════════╗
║  Setup Completed Successfully! ║
╚════════════════════════════════╝
"""), Colors.green_to_blue, interval=0.0025)

    print("\nКонфиг сохранен вот его данные:")
    print(f"- User ID: {config['USER_ID']}")
    print(f"- Bot ID: {config['BOT_ID']}")
    print(f"- Bot Token: {config['TOKEN']}")
    print(f"- Target Server: {server_name} ({config['SERVER_ID']})")

    Write.Print("\n\nКонфиг успешно сохранен! Начинаю запуск основного скрипта.", Colors.green_to_white)
    os.system("python main.py" if os.name == 'nt' else "python3 main.py")
    sys.exit()

if __name__ == "__main__":
    if not os.path.exists("configs/setup.json"):
        run_setup()
    else:
        os.system("python main.py" if os.name == 'nt' else "python3 main.py")
