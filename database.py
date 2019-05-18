#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from datetime import datetime
from uuid import uuid4

from sqlalchemy import create_engine, Column, String, Boolean, Integer, ForeignKey, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
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

# Session object to be used when creating new sessions
Session = sessionmaker(bind=engine)


class User(Base):
    """Defines the table for the user object."""
    __tablename__ = "users"

    id = Column(String(len_snowflake), primary_key=True)
    username = Column(String(len_name), nullable=False)
    discriminator = Column(String(len_discriminator), nullable=False)
    avatar = Column(String(len_pic_hash))

    memberships = relationship("Member", back_populates="user", uselist=True)


class Member(Base):
    """Defines the table for the member object, which represent a user with guild-specific settings."""
    __tablename__ = "members"

    id = Column(UUID, primary_key=True, default=uuid4)
    user_id = Column(String(len_snowflake), ForeignKey("users.id"), nullable=False)
    guild_id = Column(String(len_snowflake), ForeignKey("guilds.id"), nullable=False)
    nickname = Column(String(len_name))
    score_admin = Column(Boolean, default=False, nullable=False)
    score_giver = Column(Boolean, default=False, nullable=False)

    user = relationship("User", back_populates="memberships", uselist=False)
    guild = relationship("Guild", back_populates="members", uselist=False)


class Guild(Base):
    """Defines the table for the guild object."""
    __tablename__ = "guilds"

    id = Column(String(len_snowflake), primary_key=True)
    name = Column(String(len_name), nullable=False)
    icon = Column(String(len_pic_hash))
    channel_id = Column(String(len_snowflake))
    channel_name = Column(String(len_snowflake))

    members = relationship("Member", back_populates="guild", uselist=True)
    points = relationship("Point", back_populates="guild", uselist=True)
    quotes = relationship("Quote", back_populates="guild", uselist=True)
    roles = relationship("Role", back_populates="guild", uselist=True)
    categories = relationship("Category", back_populates="guild", uselist=True)


class Role(Base):
    """Defines the table for the role object."""
    __tablename__ = "roles"

    id = Column(String(len_snowflake), primary_key=True)
    guild_id = Column(String(len_snowflake), ForeignKey("guilds.id"))
    name = Column(String(len_guild_name))
    score_admin = Column(Boolean, default=False, nullable=False)
    score_giver = Column(Boolean, default=False, nullable=False)

    guild = relationship("Guild", back_populates="roles", uselist=False)


class Category(Base):
    """Defines the table for the category object."""
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(len_guild_name))
    guild_id = Column(String(len_snowflake), ForeignKey("guilds.id"))

    guild = relationship("Guild", back_populates="categories", uselist=False)
    points = relationship("Point", back_populates="category", uselist=True)


class Point(Base):
    """Defines the table for the point object."""
    __tablename__ = "points"

    id = Column(UUID, primary_key=True, default=uuid4)
    giver_id = Column(UUID(as_uuid=True), ForeignKey("members.id"), nullable=False)
    receiver_id = Column(UUID(as_uuid=True), ForeignKey("members.id"), nullable=False)
    guild_id = Column(String(len_snowflake), ForeignKey("guilds.id"), nullable=False)
    category_id = Column(Integer, ForeignKey("categories.id"))
    date = Column(DateTime, default=datetime.now, nullable=False)

    category = relationship("Category", back_populates="points", uselist=False)
    giver = relationship("Member", foreign_keys=[giver_id], uselist=False)
    receiver = relationship("Member", foreign_keys=[receiver_id], uselist=False)
    guild = relationship("Guild", back_populates="points", uselist=False)


class Quote(Base):
    """Defines the table for the quote object."""
    __tablename__ = "quotes"

    id = Column(UUID, primary_key=True, default=uuid4)
    author_id = Column(UUID(as_uuid=True), ForeignKey("members.id"), nullable=False)
    quoter_id = Column(UUID(as_uuid=True), ForeignKey("members.id"), nullable=False)
    guild_id = Column(String(len_snowflake), ForeignKey("guilds.id"), nullable=False)
    date = Column(DateTime, default=datetime.now, nullable=False)

    author = relationship("Member", foreign_keys=[author_id], uselist=False)
    quoter = relationship("Member", foreign_keys=[quoter_id], uselist=False)
    guild = relationship("Guild", back_populates="quotes", uselist=False)


# Creates all the tables when this file is directly ran
if __name__ == "__main__":
    Base.metadata.create_all(engine)
