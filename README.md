# May 14, 2016 Twitter search tool

This is a Flask app and some utilities that load data into SQLite.

Standard caveats apply but has the merit of working okay.

It makes it possible to search and browse historical tweets across a
group of individuals.

It was created to support [a collaborative project by Miranda July and Paul Ford as part of the Rhizome 7on7 project](https://vimeo.com/167171454).

Up and running:

- python 3
- put all the twitter handles in data/handles.csv
- `pip install -r requirements.txt`
- go get a twitter API key
- copy `config_template.py` to `config.py` and modify per that API key
  - `python -m util.make_db`
  - `python -m util.load_users`
  - `python -m util.import_tweets`

This will take a long time, many hours or days depending on your list of people.

Run it:

- `python app.py`