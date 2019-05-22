#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

from discord.ext import commands

import database as db
from bot_setup import bot


def is_admin():
    """Checks to see if the user is an admin in the guild or for the guild."""

    async def predicate(ctx):
        # If the user has admin anyways, this ends here
        if ctx.author.guild_permissions.administrator:
            return True
        else:
            return False
    return commands.check(predicate)


@bot.command()
@is_admin()
async def set_channel(ctx):
    """Sets the channel that the bot will look for messages in. This does NOT include this admin command."""

    pass

bot.run(os.environ["BOT_TOKEN"])
