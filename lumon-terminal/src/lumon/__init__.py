import os
from pathlib import Path

import sentry_sdk
from dotenv import load_dotenv
from flask import Flask, jsonify, request
from sentry_sdk.integrations.flask import FlaskIntegration

from .incidents import INCIDENTS
from .routes import api


DEFAULT_LOCAL_SENTRY_DSN = (
    "https://219bcfa335e826aa4b7863f3f50c9674@leeandher.ngrok.io/2"
)

load_dotenv(Path(__file__).resolve().parents[2] / ".env")


def _dsn() -> str | None:
    if "SENTRY_DSN" in os.environ:
        return os.environ["SENTRY_DSN"] or None
    return os.getenv("LOCAL_SENTRY_DSN", DEFAULT_LOCAL_SENTRY_DSN)


def create_app(config: dict | None = None) -> Flask:
    sentry_sdk.init(
        dsn=_dsn(),
        integrations=[FlaskIntegration()],
        environment=os.getenv("SENTRY_ENVIRONMENT", "development"),
        release=os.getenv("SENTRY_RELEASE", "lumon-terminal@1.0.0"),
        send_default_pii=True,
        traces_sample_rate=float(os.getenv("SENTRY_TRACES_SAMPLE_RATE", "1.0")),
        profiles_sample_rate=float(os.getenv("SENTRY_PROFILES_SAMPLE_RATE", "0.0")),
        in_app_include=["lumon"],
    )

    app = Flask(__name__)
    app.config.update(JSON_SORT_KEYS=False)
    if config:
        app.config.update(config)
    app.register_blueprint(api)

    @app.before_request
    def add_lumon_context() -> None:
        sentry_sdk.set_tag("lumon.floor", request.headers.get("X-Lumon-Floor", "severed"))
        sentry_sdk.set_tag("lumon.workstation", request.headers.get("X-Workstation", "MDR-04"))
        sentry_sdk.set_user(
            {
                "id": request.headers.get("X-Employee-ID", "481516"),
                "username": request.headers.get("X-Employee-Name", "Mark S."),
                "department": request.headers.get("X-Department", "Macrodata Refinement"),
            }
        )

    @app.get("/")
    def index():
        return jsonify(
            service="Lumon Severed Floor Operations Terminal",
            motto="A remembered man does not decay.",
            status="all departments nominal",
            incident_count=len(INCIDENTS),
            routes="/api/v1",
        )

    @app.get("/health/live")
    def live():
        return {"status": "alive", "kier_is_watching": True}

    @app.get("/health/ready")
    def ready():
        return {"status": "ready", "floor": "severed", "elevator": "available"}

    return app
