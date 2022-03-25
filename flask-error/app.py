import sentry_sdk
from flask import Flask
from sentry_sdk.integrations.flask import FlaskIntegration
import argparse

SENTRY_DSN = "http://93b7b137357b4edd9fbb538ee398b7e9@localhost:8000/2"
GETSENTRY_DSN = "http://bd63f9383e4747a89fa5015a94616197@dev.getsentry.net:8000/2"
HOSTED_DSN = "https://f61444722ce0460892f94a6d5d110596@o951660.ingest.sentry.io/5900755"

parser = argparse.ArgumentParser(description="Create some sentry errors")
parser.add_argument('instance',
                    default='sentry',
                    const='sentry',
                    nargs='?',
                    choices=['sentry', 'getsentry', 'hosted'],
                    help='Sentry instance to receive errors')


def dsn_selector():
    args = parser.parse_args()
    print(f"Sending errors to '{args.instance}' instance...")
    if args.instance == 'getsentry':
        return GETSENTRY_DSN
    elif args.instance == 'hosted':
        return HOSTED_DSN
    else:
        return SENTRY_DSN


sentry_sdk.init(
    dsn=dsn_selector(),
    integrations=[FlaskIntegration()],
    traces_sample_rate=1.0
)

app = Flask(__name__)


@app.route("/")
def home():
    return "<h1>Hello World!</h1>"


@app.route("/error")
def error():
    raise NameError("🔥 Error 3")


if __name__ == "__main__":
    app.run()
