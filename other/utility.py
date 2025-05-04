import inspect
import re

from other.global_constants import *


async def send_in_all_channels(message: str):
    """Sends <message> in all approved channels."""
    
    channel = bot.get_channel(GAME_CHANNEL)
    await channel.send(message)  # type: ignore

def get_bot_response(instruction: str) -> str:
    instruction = inspect.cleandoc(instruction)
    
    # response = client.chat.complete(
    #     model=model,
    #     temperature=1.0,
    #     messages = [
    #         {"role": "system", "content": instruction},
    #     ]
    # )
    
    response = client.chat.completions.create(
        model=model,
        top_p=0.5,
        messages=[{"role": "user", "content": instruction}]
    )
    # Remove chain of thought tokens
    response = response.choices[0].message.content # type: ignore
    cleaned_response = re.sub(pattern='<think>.*?</think>', repl='', string=response, flags=re.DOTALL)  # type: ignore
    cleaned_response = inspect.cleandoc(cleaned_response)

    return cleaned_response