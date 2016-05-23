from flask import *
import nltk
import db
import re


# Start up our Flask app
app = Flask(__name__, static_url_path='/static')
app.config.update(dict(
    DEBUG=True,
))


# Catches twitter usernames in text
twitter_username_re = re.compile(r'@([A-Za-z0-9_]+)')


def handle_strip(text):
    return re.sub(twitter_username_re, '', text)


def is_rt(tweet):
    """Add a boolean property to a tweet and set it."""
    tweet.is_rt = None
    is_rt = re.match("RT", tweet.tweet_text)
    if is_rt:
        tweet.is_rt = True
    return tweet


def get_words(tweets):
    """Given a set of tweets, return the most frequently-used words."""
    tweets = filter(lambda x: not(x.is_rt), tweets)
    tokenized = [nltk.word_tokenize(handle_strip(t.tweet_text))
                 for t in tweets]
    words = [item for sublist in tokenized for item in sublist]
    longwords = filter(lambda x: len(x) > 6, words)
    lcwords = map(lambda x: x.lower(), longwords)
    fdist = nltk.FreqDist(lcwords)
    common = fdist.most_common(100)
    common = filter(lambda x: x[1] > 4, common)
    common = map(lambda x: [x[0], 6 + int(x[1]/3)], common)
    return common


@app.route("/")
def hello():
    """List the users. Copied straight from the Flask tutorial."""
    users = db.User.select()\
                   .order_by(db.User.screen_name)
    return render_template('index.html',
                           users=users)


@app.route("/name/<screen_name>")
def tweets(screen_name):
    """Display information about a user."""
    tweets = db.Tweet.select()\
                     .where(db.Tweet.user_screen_name == screen_name)\
                     .order_by(db.Tweet.tweet_timestamp)
    user = db.User.select().where(db.User.screen_name == screen_name).get()
    tweets = [is_rt(tweet) for tweet in tweets]
    words = get_words(tweets)
    return render_template('user.html',
                           words=words,
                           user=user,
                           tweets=tweets)


@app.route("/word", methods=['GET'])
def words():
    """Display search results for a search term."""
    term = request.args.get('q', '')
    tweets = (db.Tweet
              .select()
              .join(
                  db.FTSTweet,
                  on=(db.Tweet.id == db.FTSTweet.tweet_id))
              .where(db.FTSTweet.match(term))
              .order_by(db.Tweet.user_screen_name,
                        db.Tweet.tweet_timestamp))
    tweets = [is_rt(tweet) for tweet in tweets]
    return render_template('word.html',
                           term=term,
                           tweets=tweets)


if __name__ == "__main__":
    app.run()
