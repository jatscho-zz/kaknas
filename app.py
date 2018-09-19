import requests
from flask import Flask

app = Flask(__name__)


@app.route("/")
def hello_world():
    # r = requests.get(
    #     "https://api.github.com/users/zachyam/repos",
    #     headers={"Authorization": "access_token 11b1b74c676365dfb6fedc03322839d77bb335a2"},
    # )
    return "Hello"


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
