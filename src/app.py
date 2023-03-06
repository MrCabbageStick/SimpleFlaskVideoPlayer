from flask import Flask, render_template, url_for


app = Flask(__name__)
app.config["SECRET_KEY"] = "Very very very secret key"


@app.route("/")
def mainPage():
    return "Hello there! Old sport."


@app.route("/watch/<video_id>")
def videoPage(video_id: str):

    return render_template("video_player.html", movie = {
        "title": "Mamuśki",
        "url": url_for("static", filename="videos/pusia_w_butach.mp4")
    })





def main():
    app.run("192.168.0.164", port=2137, debug=True)


if __name__ == "__main__":
    main()