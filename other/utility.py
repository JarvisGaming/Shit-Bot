import inspect

from other.global_constants import *


async def send_in_all_channels(message: str):
    """Sends <message> in all approved channels."""
    
    channel = bot.get_channel(GAME_CHANNEL)
    await channel.send(message)  # type: ignore

def get_bot_response(instruction: str) -> str:
    instruction = inspect.cleandoc(instruction)
    
    chat_response = client.chat.complete(
        model=model,
        temperature=0.9,
        messages = [
            {"role": "system", "content": instruction},
        ]
    )

    response = chat_response.choices[0].message.content    # type: ignore
    return response     # type: ignore