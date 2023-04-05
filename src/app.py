from flask import Flask, render_template, url_for, send_file, request
from modules.databaseManager import DatabaseManager
from modules.thumbnailManager import ThumbnailsManager
from paths import MOVIES_FILE, MOVIES_DIR, THUMBNAILS_DIR, DATABASE
from modules.movieFileHandler import MovieFileHandler

app = Flask(__name__)
app.config["SECRET_KEY"] = "Very very very secret key"

moviesHandler = MovieFileHandler(MOVIES_FILE, MOVIES_DIR, [".mp4"])

thumbnailsManager = ThumbnailsManager(THUMBNAILS_DIR, ["png", "jpg", "jpeg", "webp"], "no_thumbnail.jpg")
thumbnailsManager.loadThumbnails()

databaseManager = DatabaseManager(DATABASE)


@app.route("/")
def mainPage():
    return "Hello there! Old sport."


@app.route("/watch/<video_id>")
def videoPage(video_id: str):

    movie = moviesHandler.getMovie(video_id)

    return render_template("video_player.html", movie = {
        "title": movie.title,
        "url": url_for("static", filename=f"videos/{movie.file_name}")
    })


@app.route("/test_db")
def testDBPage():

    movie_id = v if not (v:=request.args.get("movie_id")) == '' else None
    movie_title = v if not (v:=request.args.get("movie_title")) == '' else None
    movie_series_id = v if not (v:=request.args.get("movie_series_id")) == '' else None

    series_id = v if not (v:=request.args.get("series_id")) == '' else None
    series_title = v if not (v:=request.args.get("series_title")) == '' else None

    user_id = v if not (v:=request.args.get("user_id")) == '' else None

    watchtime_movie_id = v if not (v:=request.args.get("watchtime_movie_id")) == '' else None
    watchtime_user_id = v if not (v:=request.args.get("watchtime_user_id")) == '' else None

    print(movie_id, movie_title, movie_series_id)
    print(series_id, series_title)

    movies = databaseManager.getMovies(_id=movie_id, title=movie_title, series_id=movie_series_id)

    if user_id is not None:
        movies.extend(databaseManager.getWatchList(user_id))

    series = databaseManager.getSeries(_id=series_id, title=series_title)

    watchtime = None

    if watchtime_user_id is not None and watchtime_movie_id is not None:
        watchtime = databaseManager.getWatchTime(watchtime_user_id, watchtime_movie_id)

    return render_template("db_test_page.html", movies = movies, _series = series, watchtime = watchtime)


def main():
    app.run("192.168.0.164", port=2137, debug=True)


if __name__ == "__main__":
    main()