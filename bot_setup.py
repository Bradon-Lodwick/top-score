#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

from discord.ext import commands

# Initializes the discord bot to be imported in other files
bot = commands.Bot(command_prefix="+")


@bot.event
async def on_ready():
    """Prints out information on startup."""

    print('--------------------')
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('--------------------')
