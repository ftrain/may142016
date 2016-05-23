# Database setup

from peewee import Model, CharField, TextField, IntegerField, DateField
from playhouse.sqlite_ext import SqliteExtDatabase, FTSModel

db = SqliteExtDatabase('db/rhizome.db',
                       threadlocals=True)


class User(Model):
    screen_name = CharField(
        unique=True,
        primary_key=True)
    real_name = CharField(
        null=True)
    avatar = CharField(
        default=None,
        null=True)
    friends = IntegerField(
        null=True)
    followers = IntegerField(
        null=True)
    background = CharField(
        default=None,
        null=True)
    bio = CharField(
        default=None,
        null=True,
        index=True)
    location = CharField(
        default=None,
        null=True)

    class Meta:
        database = db


class Tweet(Model):
    id = IntegerField(
        primary_key=True)
    user_screen_name = CharField(
        index=True)
    tweet_text = TextField()
    tweet_timestamp = DateField(
        index=True)
    user_follower_ct = IntegerField()
    tweet_favorite_ct = IntegerField()
    tweet_retweet_ct = IntegerField()

    class Meta:
        database = db


class Friendship(Model):
    user_screen_name = CharField(
        index=True)
    friend_screen_name = CharField(
        index=True)

    class Meta:
        database = db


class Word(Model):
    user_screen_name = CharField(
        index=True)
    word = CharField(
        index=True)
    count = IntegerField()

    class Meta:
        database = db


class FTSTweet(FTSModel):
    tweet_id = IntegerField()
    content = TextField()

    class Meta:
        database = db


def create_tables():
    db.connect()
    db.create_tables([User,
                      Tweet,
                      Friendship,
                      Word,
                      FTSTweet, ])
