def get_user_profile(user_id):
    users = {
        1: {"name": "Alice", "email": "alice@example.com", "subscription": {"plan": "pro", "expires": "2026-03-01"}},
        2: {"name": "Bob", "email": "bob@example.com", "subscription": None},
        12: {"name": "Leander", "email": "leander.rodrigues@sentry.io", "subscription": {"plan": "pro", "expires": "2026-03-01"}},
    }
    return users.get(user_id)


def error():
    user = get_user_profile(12)
    plan = user["subscription"]["plan"]
