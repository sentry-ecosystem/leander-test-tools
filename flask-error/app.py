import argparse

import sentry_sdk
from flask import Flask
from sentry_sdk.integrations.flask import FlaskIntegration


LOCAL_SENTRY_DSN = "https://69b42e5ad1606cdf535262d253800f93@leeandher.ngrok.io/2"
LOCAL_GETSENTRY_DSN = (
    "https://ee8749033b194d888fe17531eac25a35@leeandher.ngrok.io/4505319664189440"
)
HOSTED_DSN = "https://6338209daaba4a868fca858e3f7ebfc2@us.sentry.io/6507927"
SILO_DSN = "https://e9a3d278c7729cdf4e9d2162ba377d83@test-region.test.my.sentry.io/4505992947957808"

parser = argparse.ArgumentParser(description="Create some sentry errors")
parser.add_argument(
    "instance",
    default="local sentry",
    const="sentry",
    nargs="?",
    choices=["local sentry", "local getsentry", "hosted", "silo"],
    help="Sentry instance to receive errors",
)


def dsn_selector():
    args = parser.parse_args()
    print(f"Sending errors to '{args.instance}' instance...")
    if args.instance == "local getsentry":
        return LOCAL_GETSENTRY_DSN
    elif args.instance == "hosted":
        return HOSTED_DSN
    elif args.instance == "silo":
        return SILO_DSN
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
    sentry_sdk.set_user({"id": 12, "email": "leander.rodrigues@sentry.io"})
    from src.runner import error_function

    error_function()


@app.route("/txn")
def transaction():
    counter = 1
    with sentry_sdk.start_transaction(op="task", name="Test TXN"):
        with sentry_sdk.start_span(description="Test Span"):
            while counter < 10000:
                counter = counter + 1
        return "<h1>Test</h1>"


if __name__ == "__main__":
    app.run(debug=True)
