import sentry_sdk
from flask import Flask
from sentry_sdk.integrations.flask import FlaskIntegration

sentry_sdk.init(
    dsn="https://f61444722ce0460892f94a6d5d110596@o951660.ingest.sentry.io/5900755",
    integrations=[FlaskIntegration()],
    traces_sample_rate=1.0
)

app = Flask(__name__)


@app.route("/")
def home():
    return "<p> Working hello world!</p"


@app.route("/error")
def error():
    raise NameError("🚧🚧🚧  Error 9  🚧🚧🚧")
