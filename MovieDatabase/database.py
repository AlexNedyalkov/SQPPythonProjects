import sqlite3
import datetime

CREATE_MOVIE_TABLE = """CREATE TABLE if not exists movies (
                   title TEXT,
                    release_timestamp REAL
                    );"""

CREATE_WATCHLIST_TABLE = """CREATE TABLE if not exists watched (
                            watcher_name TEXT,
                            title TEXT
);"""

INSERT_MOVIES = "INSERT INTO movies (title, release_timestamp) VALUES(?, ?);"
DELETE_MOVIE = "DELETE FROM movies WHERE title = ?;"
SELECT_ALL_MOVIES = "SELECT * FROM movies"
SELECT_UPCOMING_MOVIES = "SELECT * FROM movies WHERE release_timestamp > ?;"
SELECT_WATCHED_MOVIES = "SELECT * FROM watched WHERE watcher_name = ?;"
INSERT_WATCHED_MOVIES = "INSERT INTO watched (watcher_name, title) VALUES(?, ?);"
SET_MOVIES_WATCHED = "UPDATE movies SET watched=1 WHERE title = ?;"


connection = sqlite3.connect("data.db")
connection.row_factory = sqlite3.Row

def create_tables():
    with connection:
        connection.execute(CREATE_MOVIE_TABLE)
        connection.execute(CREATE_WATCHLIST_TABLE)


def add_movie(title, release_timestamp):
    with connection:
        connection.execute(INSERT_MOVIES, (title, release_timestamp))


def get_movies(upcoming = False):
    with connection:
        cursor = connection.cursor()
        if upcoming:
            today_timestamp = datetime.datetime.today().timestamp()
            cursor.execute(SELECT_UPCOMING_MOVIES, (today_timestamp,))
        else:
            cursor.execute(SELECT_ALL_MOVIES)
        return cursor.fetchall()


def watch_movie(username, title):
    with connection:
        connection.execute(DELETE_MOVIE, (title,))
        connection.execute(INSERT_WATCHED_MOVIES, (username, title))


def get_watched_movies(username):
    with connection:
        cursor = connection.cursor()
        cursor.execute(SELECT_WATCHED_MOVIES, (username,))
        return cursor.fetchall()