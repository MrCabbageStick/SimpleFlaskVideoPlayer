from flask import Flask, render_template, url_for, jsonify, send_file, send_from_directory
from modules.database import DatabaseController
from paths import MOVIES_FILE, MOVIES_DIR
from modules.helpers import generateRandomId
from modules.movieFileHandler import MovieFileHandler

app = Flask(__name__)
app.config["SECRET_KEY"] = "Very very very secret key"

moviesHandler = MovieFileHandler(MOVIES_FILE, MOVIES_DIR, [".mp4"])


@app.route("/")
def mainPage():
    return "Hello there! Old sport."


@app.route("/watch/<video_id>")
def videoPage(video_id: str):

    movie = moviesHandler.getMovie(video_id)

    return render_template("video_player.html", movie = {
        "title": movie.title,
        "url": url_for("static", filename=f"videos/{movie.file_name}")
        # "url": f"/get_video/{video_id}"
    })


def main():
    app.run("192.168.0.164", port=2137, debug=True)


if __name__ == "__main__":
    main()