__author__ = "Bradon Lodwick"
__copyright__ = "Copyright 2019"
__credits__ = ["Bradon Lodwick"]
__license__ = "GPL"
__version__ = "1.0"
__maintainer__ = "Bradon Lodwick"
__email__ = "bradonlodwick22@gmail.com"
__status__ = "Development"

from datetime import datetime
import marshmallow_mongoengine as ma
import mongoengine as me


class UserDocument(me.EmbeddedDocument):
    """
    Represents a user stored in the database.
    """

    _id = me.StringField(unique=True, required=True)
    username = me.StringField(required=True)
    discriminator = me.StringField(min_length=4, max_length=4)
    avatar = me.StringField()
    nickname = me.StringField()
    locale = me.StringField()
    bot = me.BooleanField()
    score = me.IntField()


class PointDocument(me.EmbeddedDocument):
    """
    Represents a point within a guild.
    """

    issuer = me.EmbeddedDocumentField(UserDocument, required=True)
    value = me.IntField(required=True)
    date = me.DateField(required=True, default=datetime.utcnow())


class CategoryDocument(me.EmbeddedDocument):
    """
    Represents a category within a guild.
    """

    name = me.StringField(unique=True, required=True)
    total_score = me.IntField(required=True, default=0)
    points = me.EmbeddedDocumentListField(PointDocument, required=True, default=[])


class RoleDocument(me.EmbeddedDocument):
    """
    Represents a role within a guild. Used to setup guild administration.
    """

    _id = me.StringField(unique=True, required=True)
    name = me.StringField(required=True)


class GuildDocument(me.Document):
    """
    Represents a guild as the top level of the collection.

    """

    _id = me.StringField(primary_key=True)
    name = me.StringField(required=True)
    icon = me.StringField()
    server_score = me.IntField(required=True, default=0)
    users = me.EmbeddedDocumentListField(required=True)
    admin_role = me.EmbeddedDocumentField(RoleDocument)
    issuer_role = me.EmbeddedDocumentField(RoleDocument)
    all_can_issue_points = me.BooleanField(required=True, default=False)
    all_can_create_categories = me.BooleanField(required=True, default=False)
