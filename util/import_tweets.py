import tweepy
import config
import sys
from time import sleep
import db


class TwitterSearchClient(object):
    """Set up a tweepy client"""
    def __init__(self,
                 consumer_key, consumer_secret,
                 access_token, access_secret):
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_secret)
        self.client = tweepy.API(auth)
        return None


class TwitterSearchResponse(object):
    """Talk to Twitter."""
    def __init__(self, client, user):
        self.client = client.client
        self.screen_name = user.screen_name

    def save(self):
        try:
            print("[search] [search_term: {}]".format(self.screen_name))
            i = 0
            for page in tweepy.Cursor(self.client.user_timeline,
                                      screen_name=self.screen_name,
                                      count=200).pages(100):
                print("{}.".format(i))
                i = i + 1
                sleep(config.TWITTER_API_DELAY)
                self.process_page(page)
            
        except tweepy.error.RateLimitError:
            print("[search] [error: rate limit] [{}]".format(self))
            sleep(60)

        except tweepy.error.TweepError as e:
            print("[search] [error: tweepy] [{}]".format(e))
            sleep(60)

        except:
            print("[search] [error: unknown] [{}]".format(sys.exc_info()[0]))
            sleep(60)

    def process_page(self, page):
            for item in page:
                print("saving tweet {}/{}".format(item.user.screen_name,
                                                  item.id,))
                db.Tweet.create(
                    id=item.id,
                    user_screen_name=item.user.screen_name,
                    user_follower_ct=item.user.followers_count,
                    tweet_text=item.text,
                    tweet_timestamp=item.created_at,
                    tweet_favorite_ct=item.favorite_count,
                    tweet_retweet_ct=item.retweet_count,)
                db.FTSTweet.create(
                    tweet_id=item.id,
                    content=item.text,)


def __main__():
    client = TwitterSearchClient(config.TWITTER_CONSUMER_KEY,
                                 config.TWITTER_CONSUMER_SECRET,
                                 config.TWITTER_ACCESS_TOKEN,
                                 config.TWITTER_ACCESS_TOKEN_SECRET)
    users = db.User.select()
    for user in users:
        tsr = TwitterSearchResponse(client, user)
        tsr.save()

__main__()
