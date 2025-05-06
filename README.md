# One-upmanSHIT
_giving three shits is better than two_

An interactive AI Discord bot written in Python. Provides a game where users try to "one-up" the AI in different scenarios. See demo video for more information.
Currently running in [this discord server](https://discord.gg/qNfCMBgCCW), in case you want to try it out without the hassle of setting it up.

## Demo video
[![Watch the video](https://img.youtube.com/vi/bQcXch3zvlo/default.jpg)](https://youtu.be/bQcXch3zvlo)

\* Sound effects not included in product.

## How to run
1. Create an application on the [Discord Developer Portal](https://discord.com/developers/applications), give it sufficient permissions (eg View Channels, Manage Messages) and turn on all Privileged Gateway Intents.
2. Invite it to your server of choice.
3. Create a `sensitive.env` file and place it in the same directory as `bot.py`. Inside it, include:
   - `BOT_TOKEN`: Can be found in your [Discord Developer Portal](https://discord.com/developers/applications) application, inside the Bot tab.
   - `TOGETHER_API_KEY`: This bot uses [together.ai](https://api.together.ai/). If you wish to use another service, make the necessary adjustments in `./other/global_constants.py` and `./other/utility.py`.
4. Run `bot.py`.
5. The slash commands can then be used in any channel that the bot can see, or in the bot's DMs.
