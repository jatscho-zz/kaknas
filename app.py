import requests
from flask import Flask

app = Flask(__name__)


@app.route("/")
def hello_world():
    return "Hello"

@app.route("/health")
def health_check():
    return "200 OK"

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
