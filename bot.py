from pyrogram import Client, filters
from sessions import app
import random
from config import text
from rich.console import Console

console = Console()

console.print(
    "Copyright (C) 2022  https://github.com/void990/troll-bot\n"
    "This program comes with ABSOLUTELY NO WARRANTY.\n"
    "This is free software, and you are welcome to redistribute it under certain conditions.\n"
)

chat_id = int(console.input('[bold red]CHAT / USER ID: '))

@app.on_message(filters.chat(int(chat_id)))
def troll(client, message):
    message.reply(random.choice(text))
    console.print(f'[blue]logs: [white]{message.text}')
    
app.run()
