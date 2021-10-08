from random import random

import sentry_sdk
from flask import Flask
from sentry_sdk.integrations.flask import FlaskIntegration

sentry_sdk.init(
    dsn="http://93b7b137357b4edd9fbb538ee398b7e9@localhost:8000/2",
    integrations=[FlaskIntegration()],
    traces_sample_rate=1.0,
)

app = Flask(__name__)


@app.route("/")
def home():
    return "<p> Working hello world!</p"


@app.route("/error")
def error():

    raise NameError("🦄🦄🦄  This is a new issue!  🦄🦄🦄" + str(random()))
