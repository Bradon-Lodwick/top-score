#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

import discord
import typing
from discord.ext import commands

import database as db
from database import Session

bot = commands.Bot(command_prefix="+")


@bot.event
async def on_ready():
    """Prints out information on startup."""

    print('--------------------')
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('--------------------')


def is_admin():
    """Checks to see if the user is an admin in the guild or for the guild."""

    async def predicate(ctx):
        # If the user has admin anyways, this ends here
        if ctx.author.guild_permissions.administrator:
            return True
        else:
            # Get the roles from the database
            guild_id = str(ctx.guild.id)
            session = Session()
            try:
                roles = session.query(db.Guild).filter_by(guild_id=guild_id, score_admin=True)
            finally:
                session.close()

            # Check to see if any of the admin roles are in the user's account
            for user_role in ctx.author.roles:
                if any(x for x in roles if x.id == user_role.id):
                    return True

            # If this has been reached, the user is not an admin
            return False
    return commands.check(predicate)


@bot.command()
@is_admin()
async def set_channel(ctx):
    """Sets the channel that the bot will look for messages in. This does NOT include this admin command."""

    session = Session()
    try:
        guild = session.query(db.Guild).get(str(ctx.guild.id))
        if guild is None:
            # Set the guild variables
            guild = db.Guild(
                id=str(ctx.guild.id),
                name=ctx.guild.name,
                icon=ctx.guild.icon
            )
        guild.icon = ctx.guild.icon
        guild.channel_id = str(ctx.channel.id)
        guild.channel_name = str(ctx.channel.name)
        session.add(guild)
        session.commit()
        await ctx.send("The channel that top score will listen to has been set to here.")
    finally:
        session.close()

bot.run(os.environ["BOT_TOKEN"])
