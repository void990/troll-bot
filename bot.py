#Copyright (C) 2022 https://github.com/void990/troll-bot

#This program comes with ABSOLUTELY NO WARRANTY.

#This is free software, and you are welcome to redistribute it under certain conditions.

from logging import exception
from pdb import Restart
from pyrogram import Client, filters, enums
from sessions import app
import random
import string
from os.path import exists
import configparser
from rich.console import Console
from asyncio import sleep
from pyrogram.raw import functions
from pyrogram.types import Message, User

console = Console()
password = []
cfg = configparser.ConfigParser()
cfg.read('config.cfg')
file = open(cfg.get('settings', 'dict'), 'r')
text = file.read().split('\n')
prefix = cfg.get('settings', 'prefix')
floodwork = True
trolling = False
file.close()
chat_id = int(cfg.get('settings', 'chat_id'))
delay = int(cfg.get('settings', 'delay'))
console.print(
    "Copyright (C) 2022 https://github.com/void990/troll-bot\n"
    "This program comes with ABSOLUTELY NO WARRANTY.\n"
    "This is free software, and you are welcome to redistribute it under certain conditions.\n"
)

console.print(f'[red bold]Chat id: [white bold]{chat_id}[red bold] Delay: [white bold]{delay}')

@app.on_message(filters.command('chat', prefix) & filters.me)
async def chatid(client, message):
    chat_id = message.text.split(' ')[1]
    await message.edit(f'Raid chat id set to {chat_id}')
    cfg.set('settings', 'chat_id', chat_id)
    with open('config.cfg', 'w') as configfile:
        cfg.write(configfile)
    console.log(f'[blue bold]log: New chat id for raids: {chat_id}')
    
@app.on_message(filters.command('delay', prefix) & filters.me)
async def cdelay(client, message): 
    delay = message.text.split(' ')[1]
    await message.edit(f'Delay changed to <code>{delay}</code>!')
    cfg.set('settings', 'delay', delay)
    with open('config.cfg', 'w') as configfile:
        cfg.write(configfile)
    console.log(f'[blue bold]log: delay changed to {delay}!')

@app.on_message(filters.command('troll', prefix) & filters.me)
async def handler(client, message):
    global trolling
    if trolling == False:
        trolling = True
        await message.edit(f'Trolling mode is {trolling}')
    elif trolling == True:
        trolling = False
        await message.edit(f'Trolling mode is {trolling}')  
        
@app.on_message(filters.command(["flood"], prefix) & filters.me)
async def flood(client, message):
    global floodwork
    if floodwork == False:
        try: 
            floodwork = True   
            await message.edit(f'Flood started requested by user!')
            console.print(f'[blue bold]logs: Starting flood by command: {message.text}') 
            while floodwork:
                # await app.send_chat_action(chat_id, enums.ChatAction.TYPING)
                await message.reply(random.choice(text))
                await sleep(int(cfg.get('settings', 'delay')))
            
        except Exception as error:
            console.print('[red bold] Error [white]', error)
    elif floodwork == True:
        try:
            floodwork = False
            console.print(f'[blue bold]logs: Stopping flood by command: {message.text}')
            await message.edit(f'Flood stopped requested by user!')
        except Exception as error:
            console.print(f'[bold red]Error: {error}')
        
        
@app.on_message(filters.command(["id"],prefix) & filters.me)
async def user_id(client, message):
    if message.reply_to_message:
        user=await app.get_users(message.reply_to_message.from_user.id)
        await message.edit(f"""|-<b>Username: @{user.username}\n|-Id: <code>{user.id}</code>
        </b>""")
    else:
        check = message.text.split(f'{prefix}id')[1]
        user = await app.get_users(check)
        await message.edit(f"""|-<b>Username: @{user.username}\n|-Id: <code>{user.id}</code>
        </b>""")
    # console.log(f'User info: {user}')
    
@app.on_message(filters.command(["info"], prefix) & filters.me)
async def handler(client, message):
    if message.reply_to_message:
        user=await app.get_users(message.reply_to_message.from_user.id)
        await message.edit(f"""<b>|=Username: <code>{user.username}</code>\n|-Name:<code> {user.first_name} {"" if not user.last_name else user.last_name}</code>\n|-ID: <code>{user.id}</code>\n|-Self: <code>{user.is_self}</code>\n|-Contact: <code>{user.is_contact}</code>\n|-Mutal contact: <code>{user.is_mutual_contact}</code>\n|-Deleted: <code>{user.is_deleted}</code>\n|-Bot: <code>{user.is_bot}</code>\n|-Verified: <code>{user.is_verified}</code>\n|-Restricted: <code>{user.is_restricted}</code>\n|-Scam: <code>{user.is_scam}</code>\n|-Fake: <code>{user.is_fake}</code>\n|-Premium: <code>{user.is_premium}</code>\n|-Phone Number: <code>{user.phone_number}</code>
        </b>""")
    else:
        check = message.text.split(f'{prefix}info')[1]
        user = await app.get_users(check)
        console.print(f'{check}')
        await message.edit(f"""<b>|=Username: <code>{user.username}</code>\n|-Name:<code> {user.first_name} {"" if not user.last_name else user.last_name}</code>\n|-ID: <code>{user.id}</code>\n|-Self: <code>{user.is_self}</code>\n|-Contact: <code>{user.is_contact}</code>\n|-Mutal contact: <code>{user.is_mutual_contact}</code>\n|-Deleted: <code>{user.is_deleted}</code>\n|-Bot: <code>{user.is_bot}</code>\n|-Verified: <code>{user.is_verified}</code>\n|-Restricted: <code>{user.is_restricted}</code>\n|-Scam: <code>{user.is_scam}</code>\n|-Fake: <code>{user.is_fake}</code>\n|-Premium: <code>{user.is_premium}</code>\n|-Phone Number: <code>{user.phone_number}</code>
        </b>""")

@app.on_message(filters.command(["dict"], prefix) & filters.me)
async def dict(client, message):
    path = message.text.split(' ')[1]
    global text
    global file
    try:
        cfg.set('settings', 'dict', path)
        with open('config.cfg', 'w') as configfile:
            cfg.write(configfile)
        await message.edit(f'New path to dictionary: {path}')
        file = open(cfg.get('settings', 'dict'), 'r')
        text = file.read().split('\n')
    except Exception as error:
        await message.edit(f'Error: {error}')       
 
@app.on_message(filters.command(['g', 'generate'], prefix) & filters.me)
async def reply(client, message):
    await message.edit('Generating...')
    length = int(message.text.split(' ')[1])
    lower = string.ascii_lowercase
    upper = string.ascii_uppercase
    num = string.digits
    symbols = string.punctuation
    all = lower + upper + num + symbols
    temp = random.sample(all, length)
    password = "".join(temp)
    await message.edit(f'<spoiler>Password generated:</spoiler> {password}')
    
@app.on_message(filters.command(['help', 'h'], prefix))
async def help(client, message):
    await message.edit(f'Help:\n|-{prefix}chat <chat_id> - Изменить чат для троллинга\n|-{prefix}delay - Изменить задержку между отправкой сообщений бота\n|-{prefix}troll - Включить/Отключить режим троллинга\n|-{prefix}flood - Включить/Отключить режим флуда\n|-{prefix}id <username> или в ответ на сообщение - Узнать id пользователя\n|-{prefix}info <username> или в ответ на сообщение - Узнать информацию о пользователе\n|-{prefix}dict - Изменить путь к словарю для флуда/тролинга\n|-{prefix}g или generate - Сгенерировать пароль\n|-{prefix}h или help - Помощь по командам')
 
@app.on_message()
async def troll(client, message):
    chat = int(message.chat.id)
    global trolling
    if trolling == True and chat == int(cfg.get('settings', 'chat_id')):
        if int(message.from_user.id) == int(cfg.get('settings', 'chat_id')):
                await app.send_chat_action(chat_id, enums.ChatAction.TYPING)
                await sleep(int(cfg.get('settings', 'delay')))
                await message.reply(random.choice(text))
                console.log(f'[blue bold]logs: [white bold] ID: {chat_id} {message.text}')
    elif trolling == False and chat == int(cfg.get('settings', 'chat_id')):
                console.log(f"[red bold]Error: [white bold]Trolling is off")
            
        
app.run()
