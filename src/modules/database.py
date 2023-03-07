import sqlite3 

class DatabaseController:

    def __init__(self, path: str) -> None:
        
        self.con = sqlite3.connect(path, check_same_thread=False)


    def addMovie(self, _id: str, title: str, path: str, series: int = None):

        curs = self.con.execute(f"INSERT INTO movies VALUES ('{_id}', '{title}', {series if series is not None else 'null'}, '{path}');")
        self.con.commit()

    def getMovies(self, _id: str = None, title: str = None, series: int = None, path: str = None):

        if _id is not None:
            return self.con.execute(f"SELECT * FROM movies WHERE id LIKE '%{_id}%'")

        if title is not None:
            return self.con.execute(f"SELECT * FROM movies WHERE title LIKE '%{title}%'")

        if series is not None:
            return self.con.execute(f"SELECT * FROM movies WHERE series = {series}")

        if path is not None:
            return self.con.execute(f"SELECT * FROM movies WHERE path = {path}")

        return self.con.execute(f"SELECT * FROM movies")


    def deleteMovie(self, _id: str):

        self.con.execute(f"DELETE FROM movies WHERE id = {_id}")
        self.con.commit()

    
    def rename(self, _id: str, new_title: str):

        self.con.execute(f"UPDATE movies SET title = {new_title} WHERE id = {_id}")

    
    def purge(self):
        self.con.execute("DELETE movies")

    
    def toDict(self, cur: sqlite3.Cursor):

        movies = {}

        for movie in cur.fetchall():

            movie_dict = {}
            _id = None

            for data, field in zip(movie, cur.description):

                if field[0] == "id":
                    _id = data

                movie_dict[field] = data

            if _id is not None:
                movies[_id] = movie_dict

        return movies


    