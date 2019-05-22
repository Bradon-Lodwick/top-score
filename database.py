#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

import mongoengine as me

from bot_setup import bot

# Setup the mongoengine connection
me.connect('top-score', host=os.environ["MONGODB_URI"])


class GivenEntity(me.EmbeddedDocument):
    """
    Represents a point in the database.
    """

    giver_id = me.IntField(nullable=False)
    receiver_id = me.IntField(nullable=False)

    meta = {"allow_inheritance": True}

    def __init__(self, giver_id, receiver_id, *args, **kwargs):
        """
        Creates a new given entity.

        Args:
            giver_id (int): The id of the giver.
            receiver_id (int): The id of the receiver.
            *args:
            **kwargs:
        """
        super().__init__(*args, **kwargs)
        self.giver_id = giver_id
        self.receiver_id = receiver_id
        self.discord_giver = None
        self.discord_receiver = None

    @property
    async def giver(self):
        """
        Gets the giver of the entity as a discord User object.

        Returns:
            discord(User): The giver of the entity.
        """

        # Load the giver user if it is not loaded yet
        if self.giver is None:
            self.discord_giver = await bot.fetch_user(self.giver_id)
        return self.discord_giver

    @giver.setter
    def giver(self, giver):
        """
        Sets the discord giver object in a way that allows the database to be updated.

        Args:
            giver (discord.User): The giver of the entity.
        """

        # Make sure the user was not None
        if giver is None:
            raise ValueError("User cannot be None")
        # Sets the guild as well as the guild id for the database.
        self.discord_giver = giver
        self.discord_giver = giver.id

    @property
    async def receiver(self):
        """
        Gets the receiver of the entity as a discord User object.

        Returns:
            discord(User): The receiver of the entity.
        """

        # Load the receiver user if it is not loaded yet
        if self.receiver is None:
            self.discord_receiver = await bot.fetch_user(self.receiver_id)
        return self.discord_receiver

    @giver.setter
    def giver(self, giver):
        """
        Sets the discord guild object in a way that allows the database to be updated.

        Args:
            giver (discord.User): The giver of the entity.
        """

        # Make sure the user was not None
        if giver is None:
            raise ValueError("User cannot be None")
        # Sets the guild as well as the guild id for the database.
        self.discord_giver = giver
        self.discord_giver = giver.id


class Point(GivenEntity):
    """
    Represents a point in the database.
    """

    value = me.IntField(nullable=False)
    category = me.StringField()

    def __init__(self, giver_id, receiver_id, value, category=None, *args, **kwargs):
        """
        Creates a new point.

        Args:
            giver_id (int): The id of the giver.
            receiver_id (int): The id of the receiver.
            value (int): The value of the point.
            category (str): The category of the point.
        """

        super().__init__(giver_id, receiver_id, *args, **kwargs)
        self.value = value
        self.category = category


class Quote(GivenEntity):
    """
    Represents a quote in the database.
    """

    text = me.StringField(nullable=False)

    def __init__(self, giver_id, receiver_id, text, *args, **kwargs):
        """
        Creates a new point.

        Args:
            giver_id (int): The id of the giver.
            receiver_id (int): The id of the receiver.
            text (str): The text of the quoted message.
        """

        super().__init__(giver_id, receiver_id, *args, **kwargs)
        self.text = text


class ScoreGuild(me.Document):
    """
    Represents a guild with it's scores.
    """

    guild_id = me.IntField(primary_key=True)
    points = me.EmbeddedDocumentListField(Point)
    quotes = me.EmbeddedDocumentListField(Quote)
    admin_role_id = me.IntField()
    judge_role_id = me.IntField()

    def __init__(self, guild_id, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.guild_id = guild_id
        self._guild = None
        self._admin_role = None
        self._judge_role = None

    @property
    async def guild(self):
        """
        The discord guild object.

        Returns:
            A discord guild object.
        """

        # Load the discord guild if it is not loaded yet
        if self._guild is None:
            self._guild = await bot.fetch_guild(self.guild_id)
            # If the guild is still None, then it is an invalid guild id
            if self._guild is None:
                raise ValueError("invalid guild id")
        return self._guild

    @guild.setter
    def guild(self, guild):
        """
        Sets the discord guild object in a way that allows the database to be updated.

        Args:
            guild (discord.Guild): The guild to have it set to.
        """

        # Make sure the guild was not None
        if guild is None:
            raise ValueError("Guild cannot be None")
        # Sets the guild as well as the guild id for the database.
        self._guild = guild
        self.guild_id = guild.id

    @property
    def admin_role(self):
        """
        The discord admin role object.

        Returns:
            A discord role object.
        """

        # Load the discord admin role if it is not loaded yet
        if self._admin_role is None:
            self._admin_role = self.guild.fetch_role(self.guild_id)
            # If the role is still None, then it is an invalid role id
            if self._admin_role is None:
                raise ValueError("invalid role id")
        return self._admin_role

    @admin_role.setter
    def admin_role(self, role):
        """
        Sets the discord admin role object in a way that allows the database to be updated.

        Args:
            role (discord.Role): The role to have it set to.
        """

        # Sets the role as well as the role id for the database.
        self._admin_role = role
        self.admin_role_id = role.id

    @property
    def judge_role(self):
        """
        The discord judge role object.

        Returns:
            A discord role object.
        """

        # Load the discord judge role if it is not loaded yet
        if self._judge_role is None:
            self._judge_role = self.guild.fetch_role(self.judge_role_id)
            # If the role is still None, then it is an invalid role id
            if self._admin_role is None:
                raise ValueError("invalid role id")
        return self._judge_role

    @judge_role.setter
    def judge_role(self, role):
        """
        Sets the discord judge role object in a way that allows the database to be updated.

        Args:
            role (discord.Role): The role to have it set to.
        """

        # Sets the role as well as the role id for the database.
        self._judge_role = role
        self.judge_role_id = role.id
