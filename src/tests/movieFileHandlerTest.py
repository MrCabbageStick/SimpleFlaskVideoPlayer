from modules.movieFileHandler import MovieFileHandler
from paths import MOVIES_FILE


handler = MovieFileHandler("./movies.json", "./static/videos", ["mp4"])

# print(handler.movies)
# print(handler.series)
print(handler.movies.extend(handler.detectMovies()))

print(handler.getMoviesFromSeries(handler.series[0]._id))

# handler.saveFile()
# print(handler.getSeries(_id="series_id#1"))

