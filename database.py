#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from datetime import datetime
from uuid import uuid4

from sqlalchemy import create_engine, Column, String, Boolean, Integer, ForeignKey, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.pool import QueuePool

# Create an engine that allows connection pooling
engine = create_engine(os.environ["DATABASE_URL"], pool_size=10, max_overflow=5, poolclass=QueuePool)

# The base to use for table objects
Base = declarative_base()

# The length values for table information
len_snowflake = 18
len_name = 32
len_guild_name = 100
len_pic_hash = 34
len_discriminator = 4


class User(Base):
    """Defines the table for the user object."""
    __tablename__ = "users"

    id = Column(String(len_snowflake), primary_key=True)
    username = Column(String(len_name), nullable=False)
    discriminator = Column(String(len_discriminator), nullable=False)
    avatar = Column(String(len_pic_hash))

    memberships = relationship("members", back_populates="user")


class Member(Base):
    """Defines the table for the member object, which represent a user with guild-specific settings."""
    __tablename__ = "members"

    id = Column(UUID, primary_key=True)
    user_id = Column(String(len_snowflake), ForeignKey("users.id"), nullable=False)
    guild_id = Column(String(len_snowflake), ForeignKey("guilds.id"), nullable=False)
    nickname = Column(String(len_name))
    score_admin = Column(Boolean, default=False, nullable=False)
    score_giver = Column(Boolean, default=False, nullable=False)

    user = relationship("users", back_populates="memberships")
    guild = relationship("guilds", back_populates="members")


class Guild(Base):
    """Defines the table for the guild object."""
    __tablename__ = "guilds"

    id = Column(String(len_snowflake), primary_key=True)
    name = Column(String(len_name), nullable=False)
    icon = Column(String(len_pic_hash))
    channel_id = Column(String(len_snowflake))
    channel_name = Column(String(len_snowflake))

    members = relationship("members", back_populates="guild")
    points = relationship("points", back_populates="guild")
    quotes = relationship("quotes", back_populates="guild")
    roles = relationship("roles", back_populates="guild")
    categories = relationship("categories", back_populates="guild")


class Role(Base):
    """Defines the table for the role object."""
    __tablename__ = "roles"

    id = Column(String(len_snowflake), primary_key=True)
    guild_id = Column(String(len_snowflake), ForeignKey("guilds.id"))
    name = Column(String(len_guild_name))
    score_admin = Column(Boolean, default=False, nullable=False)
    score_giver = Column(Boolean, default=False, nullable=False)

    guild = relationship("guilds", back_populates="roles")


class Category(Base):
    """Defines the table for the category object."""
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(len_guild_name))
    guild_id = Column(String(len_snowflake), ForeignKey("guilds.id"))

    guild = relationship("guilds", back_populates="categories")
    points = relationship("points", back_populates="category")


class Point(Base):
    """Defines the table for the point object."""
    __tablename__ = "points"

    id = Column(Integer, primary_key=True, autoincrement=True)
    giver_id = Column(UUID(as_uuid=True), ForeignKey("members.id"), nullable=False)
    receiver_id = Column(UUID(as_uuid=True), ForeignKey("members.id"), nullable=False)
    guild_id = Column(String(len_snowflake), ForeignKey("guilds.id"), nullable=False)
    category_id = Column(Integer, ForeignKey("categories.id"))
    date = Column(DateTime, default=datetime.now, nullable=False)

    category = relationship("categories", back_populates="points")
    giver = relationship("members", foreign_keys=giver_id)
    receiver = relationship("members", foreign_keys=receiver_id)
    guild = relationship("guilds", back_populates="points")


class Quote(Base):
    """Defines the table for the quote object."""
    __tablename__ = "quotes"

    id = Column(Integer, primary_key=True, autoincrement=True)
    author_id = Column(UUID(as_uuid=True), ForeignKey("members.id"), nullable=False)
    quoter_id = Column(UUID(as_uuid=True), ForeignKey("members.id"), nullable=False)
    guild_id = Column(String(len_snowflake), ForeignKey("guilds.id"), nullable=False)
    date = Column(DateTime, default=datetime.now, nullable=False)

    author = relationship("members", foreign_keys=author_id)
    quoter = relationship("members", foreign_keys=quoter_id)


# Creates all the tables when this file is directly ran
if __name__ == "__main__":
    Base.metadata.create_all(engine)
