from lumon import create_app
from lumon.incidents import INCIDENTS


def test_health_routes_are_available():
    client = create_app({"TESTING": True}).test_client()

    assert client.get("/health/live").status_code == 200
    assert client.get("/health/ready").status_code == 200
    assert client.get("/api/v1").json["demo_incidents"]


def test_every_demo_incident_produces_server_error():
    app = create_app({"TESTING": False})
    app.logger.disabled = True
    client = app.test_client()

    statuses = {
        incident.slug: client.open(incident.path, method=incident.method).status_code
        for incident in INCIDENTS
    }

    assert len(statuses) >= 25
    assert statuses == {incident.slug: 500 for incident in INCIDENTS}
