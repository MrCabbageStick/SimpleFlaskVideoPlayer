from flask import Flask, render_template, url_for, jsonify
from modules.database import DatabaseController
from paths import MOVIES_DB, MOVIES_DIR
from modules.helpers import generateRandomId
from modules.detect_movies import scanForMovies

app = Flask(__name__)
app.config["SECRET_KEY"] = "Very very very secret key"

movies_db = DatabaseController(MOVIES_DB)


@app.route("/")
def mainPage():
    return "Hello there! Old sport."


@app.route("/watch/<video_id>")
def videoPage(video_id: str):

    return render_template("video_player.html", movie = {
        "title": "Mamuśki",
        "url": url_for("static", filename="videos/pusia_w_butach.mp4")
    })


@app.route("/detect_movies")
def detectMoviesPage():

    paths = scanForMovies(MOVIES_DB)

    for path in paths:

        if movies_db.getMovies(path=path).arraysize > 0:
            continue

        movies_db.addMovie(generateRandomId(), "".join(path.split(".")[:-2]), path)
    
    # return jsonify(movies_db.toDict(cur = movies_db.getMovies() ))
    return jsonify(cur = movies_db.getMovies().fetchall())




def main():
    app.run("192.168.0.164", port=2137, debug=True)


if __name__ == "__main__":
    main()