import csv
import db
import tweepy
import config
from time import sleep


class TwitterSearchClient(object):
    def __init__(self,
                 consumer_key, consumer_secret,
                 access_token, access_secret):
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_secret)
        self.client = tweepy.API(auth)
        return None


def __main__():
    print("Logging in to twitter")
    client = TwitterSearchClient(config.TWITTER_CONSUMER_KEY,
                                 config.TWITTER_CONSUMER_SECRET,
                                 config.TWITTER_ACCESS_TOKEN,
                                 config.TWITTER_ACCESS_TOKEN_SECRET)

    with open('data/handles.csv', 'rt') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            sleep(3)
            screen_name = row[0]
            print("fetching for {}".format(screen_name,))
            user = client.client.get_user(screen_name=screen_name)

            # get user 
            db.User.create(
                screen_name=row[0],
                real_name=user.name,
                bio=user.description,
                location=user.location,
                friends=user.friends_count,
                followers=user.followers_count,
                avatar=user.profile_image_url,
                background=user.profile_background_image_url,)


__main__()
