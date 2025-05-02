import os
import time

from dotenv import load_dotenv
from mistralai import Mistral

load_dotenv(dotenv_path="./sensitive.env", verbose=True, override=True)

api_key: str = os.environ['MISTRAL_API_KEY']
model = "mistral-small-latest"
client = Mistral(api_key=api_key)


# Generate prompt
prompt_creation_instruction = """
Create a scenario where the player is expected to show compassion / help others. Your response should only contain the prompt. Keep it under 30 words. End the prompt with the exact words \"What do you do?\".
"""

chat_response = client.chat.complete(
    model=model,
    temperature=0.7,
    messages = [
        {"role": "system", "content": prompt_creation_instruction},
    ]
)

assert chat_response.choices is not None
assert chat_response.choices[0].message.content is not None
prompt = chat_response.choices[0].message.content

print(f"Prompt: {prompt}")
time.sleep(5)

# Get player response + generate bot response
bot_response_instruction = f"""
You are given the following prompt: \"{prompt}\"
How do you make yourself look as good as possible in front of others in this situation? Do not roleplay. Your response should only contain your specific actions.
Respond in one paragraph without any formatting. Keep your response under 50 words.
"""

chat_response = client.chat.complete(
    model=model,
    temperature=0.7,
    messages = [
        {"role": "system", "content": bot_response_instruction},
    ]
)
assert chat_response.choices is not None
assert chat_response.choices[0].message.content is not None
bot_strategy = chat_response.choices[0].message.content


# Evaluate strategies and get winner
judge_instruction = f"""
You are a judge for a game show about showing compassion and helping others. Given two responses, determine which player did better in the given scenario.
Format your response as follows: \"Player X wins! [EXPLANATION FOR WHY PLAYER 1'S RESPONSE IS BETTER] [EXPLANATION FOR WHY PLAYER 2'S RESPONSE IS NOT AS GOOD]\"
Keep your response under 100 words.

The scenario is: \"{prompt}\"
"""

# prefix = ""

player_strategy = input("Player response: ")
print(f"Bot response: {bot_strategy}")


question = f"""
Player 1: {player_strategy}

Player 2: {bot_strategy}
"""

chat_response = client.chat.complete(
    model=model,
    messages = [
        {"role": "system", "content": judge_instruction},
        {"role": "user", "content": question},
        # {"role": "assistant", "content": prefix, "prefix": True},
    ]
)

assert chat_response.choices is not None
assert chat_response.choices[0].message.content is not None
judge_response = chat_response.choices[0].message.content
# print(chat_response.choices[0].message.content[len(prefix):])   # type: ignore

print(f"Judge: {judge_response}")