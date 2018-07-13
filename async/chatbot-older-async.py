""" The following is NOT a cog that you can use in the async liabary of discord.py WITHOUT the need of ext.commands
    I highly recommend NOT using this version of discord.py, but I'm supporting all bots with this.
    You may use this, but please consider giving some sort of credit or star the repo :)
    By Spectrix """
import json, apiai, discord, asyncio

client = discord.Client()
CLIENT_ACCESS_TOKEN = 'your client access token for dialogflow'
ai = apiai.ApiAI(CLIENT_ACCESS_TOKEN)

@client.event
async def on_ready():
    print('ok') # Do whatever you want here, this version doesn't support cogs

@client.event
async def on_message(message):
    if not message.author.bot and (message.server == None or client.user in message.mentions): # Checking if the bot is being mentioned by another user and not by itself
        try:
            if message.content.startswith(("$", "!", "?", "-", "*", "`", "~", "+", "/", ";", "=", "&", ">")): # a bunch of generic checks to see if the bot is not supposed to reply (for example if you're using another bot and you need to mention our bot, you don't want the bot to reply)
                pass
            else:
                await client.send_typing(message.channel) # Make it look like the bot is actually typing the message. This adds a nice touch to let the user know the bot has read the message and it processing it
                user_message = message.content.replace(message.server.me.mention,'') if message.server else message.content # Now we remove the mention from the message to get the input

                request = ai.text_request()
                request.query = user_message

                response = json.loads(request.getresponse().read()) # Get the json from dialogflow

                result = response['result'] # Get the actual plaintext reply
                action = result.get('action') # Get the action (this can be helpful if you want to make the bot able to run commands when asked. For example, telling the bot to send help could make it DM a user with a help command)

                await client.send_message(message.channel, f"{message.author.mention} {response['result']['fulfillment']['speech'])}") # Send the message and tag the message author

        except KeyError: # If the bot gets input dialogflow can't handle, it will raise a KeyError
            await client.send_message(message.channel, "`Error: 'KeyError', insufficiant input`")

client.run("your discord token")
# Honestly why do people use async like this still