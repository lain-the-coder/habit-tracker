from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return "This is my starter home page for my habit tracker app!"

if __name__ == "__main__":
    app.run(debug = True)