from typing import Final
import os
import discord
from dotenv import load_dotenv
from discord import Intents, Client, Message
from responses import get_response
from discord.ext import tasks, commands
from utility import returnNextMatch

load_dotenv()
TOKEN: Final[str] = os.getenv('DISCORD_TOKEN')
CHANNEL_ID: Final[int] = int(os.getenv('DISCORD_CHANNEL_ID'))

intents: Intents = Intents.default()
intents.message_content = True
client: Client = Client(intents=intents)


async def send_message(message: Message, user_message: str) -> None:
    if not user_message:
        print('(Message was empty because intents were not enabled probably)')
        return
    
    if is_private := user_message[0] == '?':
        user_message = user_message[1:]
    
    try:
        response: str = get_response(user_message)
        await message.author.send(response) if is_private else await message.channel.send(response)
    except Exception as e:
        print(e)
        
@client.event
async def on_ready() -> None:
    check_match.start()
    print(f'{client.user} is now running!')

@client.event
async def on_message(message: Message) -> None:
    if message.author == client.user:
        return
    
    username: str = str(message.author)
    user_message: str = message.content
    channel: str = str(message.channel)
    

    print(f'[{channel} {username}: "{user_message}"]')
    await send_message(message, user_message)

@tasks.loop(hours=24)
async def check_match():
    channel = client.get_channel(CHANNEL_ID)
    if channel:
        match_message = returnNextMatch()
        if match_message:
            await channel.send(returnNextMatch())   

def main() -> None:
    client.run(token=TOKEN)

if __name__ == '__main__':
    main()