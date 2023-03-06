from flask import Flask, render_template


app = Flask(__name__)
app.config["SECRET_KEY"] = "Very very very secret key"


@app.route("/")
def mainPage():
    return "Hello there! Old sport."






def main():
    app.run(debug=True)


if __name__ == "__main__":
    main()