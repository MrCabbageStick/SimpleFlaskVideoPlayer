from consts import TIMESTAMP_FORMAT
from modules.movieClasses import Movie, Series, User
import sqlite3
import datetime

class DatabaseManager():

    database: sqlite3.Connection

    def __init__(self, db_file_path: str) -> None:
        
        self.database = sqlite3.connect(db_file_path, check_same_thread=False)

    
    # Movie related

    def getMovies(self, *, _id: str = None, title: str = None, series_id: str = None) -> list[Movie]: 

        movies = []

        if _id is not None:
            movies.extend(self.database.execute(f"SELECT * FROM movies WHERE id = '{_id}'").fetchall())

        if title is not None:
            movies.extend(self.database.execute(f"SELECT * FROM movies WHERE title LIKE '%{title}%'").fetchall())

        if series_id is not None:
            movies.extend(self.database.execute(f"SELECT * FROM movies WHERE series = '{series_id}'").fetchall())

        return [Movie(*movie) for movie in movies]


    def getSeries(self, _id: str = None, title: str = None) -> list[Series]:

        series = []

        if _id is not None:
            series.extend(self.database.execute(f"SELECT * FROM series WHERE id = '{_id}'").fetchall())

        if title is not None:
            series.extend(self.database.execute(f"SELECT * FROM series WHERE title LIKE '%{title}%'").fetchall())

        return [Series(*_series) for _series in series]


    def getWatchList(self, user_id: str) -> list[Movie]: 

        video_ids = self.database.execute(f"SELECT movie_id FROM watch_list WHERE user_id = '{user_id}'").fetchall()
        video_ids = map(lambda x: x[0], video_ids)

        return [self.getMovies(_id=video_id)[0] for video_id in video_ids]


    def getWatchTime(self, user_id: str, movie_id: str) -> int:

        time = self.database.execute(f"SELECT watch_time FROM watch_time WHERE user_id = '{user_id}' AND movie_id = '{movie_id}'").fetchall()

        return time[0][0] if time else 0
    

    # User related

    def addUser(self, *, user: User = None):

        timestamp = datetime.datetime.now().strftime(TIMESTAMP_FORMAT)

        self.database.execute(f"INSERT INTO users VALUES ('{user._id}', '{user.name}', '{timestamp}', {user.permission_level})")


