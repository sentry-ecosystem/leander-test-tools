import argparse
import sys
from pathlib import Path
from urllib.error import HTTPError
from urllib.request import Request, urlopen


PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "src"))

import sentry_sdk  # noqa: E402

from lumon import create_app  # noqa: E402
from lumon.incidents import BY_SLUG, INCIDENTS  # noqa: E402


def parse_args():
    parser = argparse.ArgumentParser(description="Generate Lumon production incidents")
    parser.add_argument("slugs", nargs="*", help="Only generate the named incident slugs")
    parser.add_argument("--base-url", help="Send HTTP requests to a running app instead")
    parser.add_argument("--repeat", type=int, default=1, help="Events to send per issue")
    parser.add_argument("--list", action="store_true", help="List incidents without sending")
    return parser.parse_args()


def select_incidents(slugs):
    unknown = sorted(set(slugs) - BY_SLUG.keys())
    if unknown:
        raise SystemExit(f"Unknown incident slug(s): {', '.join(unknown)}")
    return [BY_SLUG[slug] for slug in slugs] if slugs else list(INCIDENTS)


def send_remote(base_url, incident):
    request = Request(
        f"{base_url.rstrip('/')}{incident.path}",
        method=incident.method,
        headers={"X-Lumon-Floor": "severed", "X-Workstation": "MDR-DEMO"},
    )
    try:
        with urlopen(request, timeout=10) as response:
            return response.status
    except HTTPError as error:
        return error.code


def main():
    args = parse_args()
    incidents = select_incidents(args.slugs)
    if args.list:
        for incident in incidents:
            print(f"{incident.slug:28} {incident.method:4} {incident.path}")
        return 0

    client = None
    if not args.base_url:
        app = create_app({"TESTING": False})
        app.logger.disabled = True
        client = app.test_client()

    sent = 0
    for iteration in range(args.repeat):
        for incident in incidents:
            if client:
                response = client.open(
                    incident.path,
                    method=incident.method,
                    headers={"X-Lumon-Floor": "severed", "X-Workstation": "MDR-DEMO"},
                )
                status = response.status_code
            else:
                status = send_remote(args.base_url, incident)
            result = "captured" if status == 500 else f"unexpected HTTP {status}"
            print(f"[{iteration + 1}/{args.repeat}] {incident.slug:28} {result}")
            sent += status == 500

    sentry_sdk.flush(timeout=10)
    print(f"\nCompleted: {sent}/{len(incidents) * args.repeat} error events generated.")
    return 0 if sent == len(incidents) * args.repeat else 1


if __name__ == "__main__":
    raise SystemExit(main())
