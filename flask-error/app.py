import sentry_sdk
from flask import Flask
from sentry_sdk.integrations.flask import FlaskIntegration
import argparse

LOCAL_SENTRY_DSN = "https://93b7b137357b4edd9fbb538ee398b7e9@leeandher.ngrok.io/2"
LOCAL_GETSENTRY_DSN = "https://ee8749033b194d888fe17531eac25a35@leeandher.ngrok.io/4505319664189440"
HOSTED_DSN = "https://f61444722ce0460892f94a6d5d110596@o951660.ingest.sentry.io/5900755"
MARCOS_DSN = "https://9db93bc8a4f011eaa82d4201c0a8d032@o401775.ingest.sentry.io/5261902"

parser = argparse.ArgumentParser(description="Create some sentry errors")
parser.add_argument('instance',
                    default='local sentry',
                    const='sentry',
                    nargs='?',
                    choices=['local sentry', 'local getsentry', 'hosted'],
                    help='Sentry instance to receive errors')


def dsn_selector():
    args = parser.parse_args()
    print(f"Sending errors to '{args.instance}' instance...")
    if args.instance == 'local getsentry':
        return LOCAL_GETSENTRY_DSN
    elif args.instance == 'hosted':
        return HOSTED_DSN
    elif args.instance == 'marcos':
        return MARCOS_DSN
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
    sentry_sdk.capture_exception(ValueError("TestError5"))


if __name__ == "__main__":
    app.run()
