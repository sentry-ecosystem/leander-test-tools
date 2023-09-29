import sentry_sdk
from flask import Flask
from sentry_sdk.integrations.flask import FlaskIntegration
import argparse

LOCAL_SENTRY_DSN = "https://96e4bfeea741615f0d83ca82c187ec5d@leeandher.ngrok.io/18"
LOCAL_GETSENTRY_DSN = (
    "https://ee8749033b194d888fe17531eac25a35@leeandher.ngrok.io/4505319664189440"
)
HOSTED_DSN = "https://6338209daaba4a868fca858e3f7ebfc2@o951660.ingest.sentry.io/6507927"

parser = argparse.ArgumentParser(description="Create some sentry errors")
parser.add_argument(
    "instance",
    default="local sentry",
    const="sentry",
    nargs="?",
    choices=["local sentry", "local getsentry", "hosted"],
    help="Sentry instance to receive errors",
)


def dsn_selector():
    args = parser.parse_args()
    print(f"Sending errors to '{args.instance}' instance...")
    if args.instance == "local getsentry":
        return LOCAL_GETSENTRY_DSN
    elif args.instance == "hosted":
        return HOSTED_DSN
    else:
        return LOCAL_SENTRY_DSN


sentry_sdk.init(
    dsn=dsn_selector(),
    integrations=[FlaskIntegration()],
    traces_sample_rate=1.0,
)

app = Flask(__name__)


@app.route("/")
def home():
    return "<h1>Hello World!</h1>"


@app.route("/error")
def error():
    print(1 / 0)
    # sentry_sdk.capture_exception(ValueError("TestError5"))


if __name__ == "__main__":
    app.run()
