__author__ = "Bradon Lodwick"
__copyright__ = "Copyright 2019"
__credits__ = ["Bradon Lodwick"]
__license__ = "GPL"
__version__ = "1.0"
__maintainer__ = "Bradon Lodwick"
__email__ = "bradonlodwick22@gmail.com"
__status__ = "Development"

from discord.ext import commands
import os

# Setup the bot
command_prefix = '+'
bot = commands.Bot(command_prefix=command_prefix, description='Keep track of scores for random stuff using Top Score!')
# Load the token
token = os.getenv('BOT_TOKEN')


@bot.event
async def on_ready():
    """
    Sets up the bot.
    """

    # Prints out bot information
    print('--------------------')
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('--------------------')


@bot.event
async def on_message(message):
    """
    Triggers when a user sends a message to check if a point is being given.

    Args:
        message: The discord message that triggered the event.
    """

    # Check the message to see if it starts with the command prefix
    if message.content[0] == command_prefix:
        # Split the message into 3 parts on spaces, those being the prefix with point value, the category,
        # and the user to give the point to.
        split_contents = message.content.split(' ')
        # If the message contains the right number of parts, continue to handle the message
        if len(split_contents) != 3:
            # Check the number after the + to get the point value
            value = split_contents[0][1:]
            try:
                value = int(value)
            except ValueError:
                # TODO Handle error for unacceptable point value
                pass
            # Set the category for the point
            category = split_contents[1]
            # Get the user that was mentioned in the message
            # TODO try to do this using message contents not mention list
            # TODO make sure that the mention was a user, and not a role
            # TODO give the user the point
            # TODO send success message to the channel the message was sent in
        else:
            # TODO Handle error for unacceptable number of arguments given
            pass


if __name__ == '__main__':
    bot.run(token)
