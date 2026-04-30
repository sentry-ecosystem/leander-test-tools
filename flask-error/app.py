import argparse
import os
from datetime import datetime

import sentry_sdk
from flask import Flask
from sentry_sdk.integrations.flask import FlaskIntegration

LOCAL_SENTRY_DSN = (
    "https://c6b8c6c21bad812e48e2d115968a55e5@leeandher.ngrok.io/3"  # robots
)
LOCAL_SENTRY_DSN = (
    "https://87bca3472b590976a030e0e6456b72cc@leeandher.ngrok.io/2"  # humans
)
LOCAL_GETSENTRY_DSN = (
    "https://287a7215db7931a63e5d7a2f62506f9a@leeandher.ngrok.io/4506974030528528"
)

# devsentry-ecosystem
ECOSYSTEM_DSN = os.environ.get("ECOSYSTEM_DSN", "")
# sentry-leander-eu // legacy-data-forwarding
LEGACY_DATA_FORWARD_DSN = os.environ.get("LEGACY_DATA_FORWARD_DSN", "")

# sentry-leander // all-robots
SENTRY_LEANDER_DSN = os.environ.get("SENTRY_LEANDER_DSN", "")
#  lxyz2 // django
LXYZ2_DSN = os.environ.get("LXYZ2_DSN", "")
# leeandher // work-funnel
WORK_FUNNEL_DSN = os.environ.get("WORK_FUNNEL_DSN", "")

parser = argparse.ArgumentParser(description="Create some sentry errors")
parser.add_argument(
    "instance",
    default="sentry",
    const="sentry",
    nargs="?",
    choices=[
        "sentry",
        "getsentry",
        "lxyz2",
        "ecosystem",
        "leander",
        "temp",
        "work-funnel",
    ],
    help="Sentry instance to receive errors",
)


def dsn_selector():
    args = parser.parse_args()
    print(f"Sending errors to '{args.instance}' instance...")
    if args.instance == "getsentry":
        dsn = LOCAL_GETSENTRY_DSN
    elif args.instance == "lxyz2":
        dsn = LXYZ2_DSN
    elif args.instance == "ecosystem":
        dsn = ECOSYSTEM_DSN
    elif args.instance == "leander":
        dsn = SENTRY_LEANDER_DSN
    elif args.instance == "work-funnel":
        dsn = WORK_FUNNEL_DSN
    elif args.instance == "temp":
        dsn = LEGACY_DATA_FORWARD_DSN
    else:
        dsn = LOCAL_SENTRY_DSN
    if not dsn:
        raise RuntimeError(
            f"DSN for '{args.instance}' is not configured. "
            f"Set the corresponding environment variable (see .env.example)."
        )
    return dsn


sentry_sdk.init(
    dsn=dsn_selector(),
    integrations=[FlaskIntegration()],
    send_default_pii=True,
    traces_sample_rate=1.0,
)

app = Flask(__name__)


@app.route("/")
def home():
    return """
    <div>
    <h1>Hello World!</h1>
    <h1></h2>
    <a href="/regular">Link to regular page</a>
    <a href="/error">Link to error page</a>
    </div>"""


@app.route("/regular")
def regular():
    return """
    <div>
    <h1>Hello World!</h1>
    <a href="/">Link to home page</a>
    <a href="/error">Link to error page</a>
    </div>"""


@app.route("/error")
@app.route("/error/")
def error():
    sentry_sdk.set_user(
        {
            "id": 12,
            "email": "leander.rodrigues@sentry.io",
            "username": "leeandher",
            "ip_address": "12.34.56.78",
            "other": "property",
            "location": "canada",
        }
    )
    with sentry_sdk.configure_scope() as scope:
        scope.set_context(
            "large_numbers",
            {
                "decimal_number": 123456.789,
                "number": 123456789,
                "negative_number": -123456789,
                "big_decimal_number": 123456789.123456789,
                "big_number": 123456789123456789,
                "big_negative_number": -123456789123456789,
                "bug_report_number": 608548899684111178,
            },
        )
        from src.runner import error

        application = {}

        error()


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
