# "May 14, 2016" Twitter search tool

This was created to support [a collaborative project by Miranda July and Paul Ford with support from Starlee Kine as part of the Rhizome 7on7 project](https://vimeo.com/167171454).

![Here is a screenshot.](https://raw.githubusercontent.com/ftrain/may142016/master/doc/screenshot.jpg)

This is a Flask app and some utilities that load data into SQLite. Standard caveats about speed of development and general incompetence apply/but has the merit of working okay.

It makes it possible to search and browse historical tweets across a group of individuals. For example: Load in all the people in your Slack room, search their tweets for "dream," and recite their dreams back to them.

## Up and running:

- python 3
- put all the twitter handles in `data/handles.csv`
- `pip install -r requirements.txt`
- go get a twitter API key
- copy `config_template.py` to `config.py` and modify per that API key

- Run these things
  - `python -m util.setup_nltk` # load the nltk punkt model
  - `python -m util.make_db` # make the database
  - `python -m util.load_users` # load the users from `data/handles.csv`
  - `python -m util.import_tweets` # import the tweets from those handles

Tweet importing will take a long time, many hours or days depending on your list of people, their prolixity, etc.

Run the app:

- `python app.py`

## Notes

- Works fine under `gunicorn`.
- If you start to mess with it while the tweets are loading into SQLite it can skip tweets because SQLite wants none of that.

## Mac OS X setup

Here is how @dphiffer got this up and running on his Mac, which didn't have Python 3 setup yet (but did have [Homebrew](https://brew.sh/)). This is a little more specific and detailed, but YMMV.

```
brew link xz
brew install python3
cd /usr/local
git clone https://github.com/ftrain/may142016.git
cd may142016
pip3 install -r requirements.txt
cp config_template.py config.py
emacs config.py
```

* Create new [OAuth application](https://app.twitter.com/)
* Generate Access token
* Copy/paste into config.py
* Save (ctrl-x ctrl-s)
* Quit (ctrl-x ctrl-c)

```
emacs data/handles.csv
```

* Edit the list of accounts you want to download
* Save (ctrl-x ctrl-s)
* Quit (ctrl-x ctrl-c)

```
python3 -m util.setup_nltk
python3 -m util.make_db
python3 -m util.load_users
python3 -m util.import_tweets
python3 app.py
```

Now you should be able to go to http://localhost:5000/ and poke around.
