from flask import Flask, render_template, url_for, send_file
from modules.thumbnailManager import ThumbnailsManager
from paths import MOVIES_FILE, MOVIES_DIR, THUMBNAILS_DIR
from modules.movieFileHandler import MovieFileHandler

app = Flask(__name__)
app.config["SECRET_KEY"] = "Very very very secret key"

moviesHandler = MovieFileHandler(MOVIES_FILE, MOVIES_DIR, [".mp4"])

thumbnailsManager = ThumbnailsManager(THUMBNAILS_DIR, ["png", "jpg", "jpeg", "webp"], "no_thumbnail.jpg")
thumbnailsManager.loadThumbnails()


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


def main():
    app.run("192.168.0.164", port=2137, debug=True)


if __name__ == "__main__":
    main()