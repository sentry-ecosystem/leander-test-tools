import sentry_sdk
from flask import Flask
from sentry_sdk.integrations.flask import FlaskIntegration

sentry_sdk.init(
    dsn="http://26624a659d0540b3a9de021b97d70169@localhost:8000/1",
    integrations=[FlaskIntegration()],
    traces_sample_rate=1.0
)

app = Flask(__name__)


@app.route("/")
def home():
    return "<p> Working hello world!</p"


@app.route("/error")
def error():
    raise RuntimeError("something is breaking 😬")
