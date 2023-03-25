import json
from modules.fileFinder import findFilesByExtension
from paths import MOVIES_FILE, MOVIES_DIR
from dataclasses import dataclass
from modules.helpers import generateRandomId

'''
~~ MOVIE FILE STRUCTURE ~~

> movies.json
|
|- series:
|  |- series_id:
|  .  |- "title": "<title>" 
|  .  |- "movies": ...movie_ids
|  |- ...
|
|- movies:
|   |- movie_id:
|   .  |- "title": "<title>"
|   .  |- "file_name": "<file_name>"
|   |- ...
'''

class FileStructureError(Exception):
    ''' MovieFileHandler() can't get find "movies" or "series" in the movies file'''

    def __init__(self, message = "MovieFileHandler() can't get find \"movies\" or \"series\" in the movies file") -> None:
        super().__init__(message)


@dataclass
class Movie:
    _id: str
    title: str
    file_name: str

    def asDict(self):
        return {"title": self.title, "file_name": self.file_name}

@dataclass
class Series:
    _id: str
    title: str
    movies: list[str]

    def asDict(self):
        return {"title": self.title, "movies": self.movies}


class MovieFileHandler():

    movies: list[Movie] = []
    series: list[Series] = []
    file_path: str
    movies_dir_path: str
    movie_extensions: list[str]


    def __init__(self, file_path: str, movies_dir_path: str, movie_extensions: list[str]) -> None:
        
        self.file_path = file_path
        self.movies_dir_path = movies_dir_path
        self.movie_extensions = movie_extensions

        self.loadMovies()
        self.loadSeries()


    def detectMovies(self) -> list[Movie]: 

        file_names = findFilesByExtension(self.movies_dir_path, *self.movie_extensions)

        not_existing = [file_name for file_name in file_names if len(self.getMovies(file_name=file_name)) == 0]

        return [self.generateMovieFromFileName(file_name) for file_name in not_existing]
    

    def generateMovieFromFileName(self, file_name: str) -> Movie:

        _id = generateRandomId()

        # If id exists generate a new one
        while len(self.getMovies(_id=_id)) > 0:
            _id = generateRandomId()

        return Movie(
            _id = _id,
            title = ".".join(file_name.split('.')[:-1]),  # Remove an extension from the file_name
            file_name = file_name
        )


    def getMovies(self, _id: str = None, title: str = None, file_name: str = None) -> list[Movie]:

        movies = []

        if _id is not None:
            movies.extend([movie for movie in self.movies if movie._id == _id])

        if title is not None:
            movies.extend([movie for movie in self.movies if movie.title == title])

        if file_name is not None:
            movies.extend([movie for movie in self.movies if movie.file_name == file_name])

        return movies
    

    def getMovie(self, _id: str) -> Movie | None:

        for movie in self.movies:
            if movie._id == _id:
                return movie
            
        return None
    
    
    def getSeries(self, _id: str = None, title: str = None, movie_id: str = None) -> list[Series]:

        _series = []

        if _id is not None:
            _series.extend([series for series in self.series if series._id == _id])

        if title is not None:
            _series.extend([series for series in self.series if series.title == title])

        if movie_id is not None:
            _series.extend([series for series in self.series if movie_id in series.movies])

        return _series
    

    def getSingleSeries(self, _id: str) -> Series | None:

        for series in self.series:
            if series._id == _id:
                return series
            
        return None
    
    
    def getMoviesFromSeries(self, series_id: str) -> list[Movie]:

        movie_ids = self.getSeries(_id = series_id)[0].movies
        return list(filter(None, [self.getMovie(movie_id) for movie_id in movie_ids]))


    def loadMovies(self):

        with open(self.file_path, "r") as file:

            movies_dict: dict = json.load(file).get("movies")

            if movies_dict is None:
                raise FileStructureError(f"MovieFileHandler() can't find \"movies\" in: \"{self.file_path}\"")

            movie_ids = [movie._id for movie in self.movies]


        for movie_id, movie in movies_dict.items():

            # If the movie exists skip the current iteration
            if movie_id in movie_ids:
                continue

            # Append the movie
            self.movies.append(Movie(
                _id = movie_id,
                title = movie.get("title"),
                file_name = movie.get("file_name")
            ))
            

    def loadSeries(self):

        with open(self.file_path, "r") as file:

            series_dict: dict = json.load(file).get("series")

            if series_dict is None:
                raise FileStructureError(f"MovieFileHandler() can't find \"series\" in: \"{self.file_path}\"")
            
            series_ids = [series._id for series in self.series]

        for series_id, series in series_dict.items():

            # If the series exists skip the current iteration
            if series_id in series_ids:
                continue

            # Append the series
            self.series.append(Series(
                _id = series_id,
                title = series.get("title"),
                movies = series.get("movies")
            ))


    def getMoviesDict(self) -> dict:

        movie_dict = {}

        for movie in self.movies: 
            movie_dict[movie._id] = movie.asDict()

        return movie_dict
    

    def getSeriesDict(self) -> dict:

        series_dict = {}

        for series in self.series: 
            series_dict[series._id] = series.asDict()

        return series_dict


    def saveFile(self):

        with open(self.file_path, "w") as file:
            json.dump({"series": self.getSeriesDict(), "movies": self.getMoviesDict()}, file, indent=4)






