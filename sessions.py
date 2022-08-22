from pyrogram import Client
from config import api_id, api_hash

app = Client(
    "my_account",
    api_id=api_id,
    api_hash=api_hash,
    hide_password=True,
    sleep_threshold=30,
)

with app:
     me = app.get_me()
     print(f"[{me.first_name}] [{me.id}]")
     
     
