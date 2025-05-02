import os

from dotenv import load_dotenv
from mistralai import Mistral

load_dotenv(dotenv_path="./sensitive.env", verbose=True, override=True)

api_key: str = os.environ['MISTRAL_API_KEY']
model = "mistral-small-latest"
client = Mistral(api_key=api_key)






# Generate prompt
prompt_creation_instruction = """
You are a prompt creator for a quiz game show about surving unlikely scenarios, themed around shit. You need to create a situation for the players to survive in. Be creative and feel free to go completely off the rails. Make shit and potty humor-related puns in your prompt.

The prompt must only be about one specific event. Only respond with the contents of the prompt, and nothing else. Keep your response under 30 words.
"""

chat_response = client.chat.complete(
    model=model,
    messages = [
        {"role": "system", "content": prompt_creation_instruction},
    ]
)

assert chat_response.choices is not None
assert chat_response.choices[0].message.content is not None
prompt = chat_response.choices[0].message.content



# Get player strategy + generate bot strategy
bot_strategy_instruction = f"""
You are given the following prompt: \"{prompt}\"
What is your strategy that will maximize your chance of survival? Be creative and feel free to go completely off the rails.
Keep your response under 50 words.
"""

chat_response = client.chat.complete(
    model=model,
    messages = [
        {"role": "system", "content": bot_strategy_instruction},
    ]
)
assert chat_response.choices is not None
assert chat_response.choices[0].message.content is not None
bot_strategy = chat_response.choices[0].message.content


# Evaluate strategies and get winner
judge_instruction = f"""
You are a judge for a quiz game show about surving unlikely scenarios. The winner is the player that has the highest likelihood of survival given their response.
You will see two responses. Which one do you think is more likely to survive, and why?

Format your response as follows: \"Player X wins! [EXPLANATION FOR WHY PLAYER 1'S STRATEGY IS BETTER THAN PLAYER 2'S]\"
Keep your response under 100 words.

The prompt is: \"{prompt}\"
"""

# prefix = ""

print(f"Prompt: {prompt}")

player_strategy = input("Player strategy: ")
print(f"Bot strategy: {bot_strategy}")


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

# Idea: OneuppsmanSHIT (giving too much of a SHIT)