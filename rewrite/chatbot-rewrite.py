""" The following is a cog that you can use in the rewrite liabary of discord.py (with ext.commands)
    You may use this, but please consider giving some sort of credit or star the repo :)
    By Spectrix """
import json, apiai, discord, asyncio
from discord.ext import commands

CLIENT_ACCESS_TOKEN = 'your client access token for dialogflow'
ai = apiai.ApiAI(CLIENT_ACCESS_TOKEN)

class chatbot:
    """ Talk to your dialogflow chatbot! Made by Spectrix """

    def __init__(self, bot):
        self.bot = bot

    async def on_message(self, message):
        if not message.author.bot and self.bot.user in message.mentions: # Checking if the bot is being mentioned by another user and not by itself
            try:
                if message.content.startswith(("$", "!", "?", "-", "*", "`", "~", "+", "/", ";", "=", "&", ">")): # a bunch of generic checks to see if the bot is not supposed to reply
                    pass
                else:
                    async with message.channel.typing(): # Make it look like the bot is actually typing the message. This adds a nice touch to let the user know the bot has read the message and it processing it
                        user_message = message.content.replace(message.guild.me.mention,'') if message.guild else message.content # Now we remove the mention from the message to get the input

                        request = ai.text_request()
                        request.query = user_message

                        response = json.loads(request.getresponse().read()) # Get the json from dialogflow

                        result = response['result'] # Get the actual plaintext reply
                        action = result.get('action') # Get the action (this can be helpful if you want to make the bot able to run commands when asked. For example, telling the bot to send help could make it DM a user with a help command)

                    await message.channel.send(f"{message.author.mention} {response['result']['fulfillment']['speech']}") # Send the message and tag the message author

            except KeyError: # If the bot gets input dialogflow can't handle, it will raise a KeyError
                await message.channel.send("```Error: 'KeyError', make sure you gave not too little input and not too much ;)```")

def setup(bot):
    bot.add_cog(chatbot(bot))