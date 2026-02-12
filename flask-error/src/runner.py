def get_user_profile(user_id):
    users = {
        1: {"name": "Alice", "email": "alice@example.com", "subscription": {"plan": "pro", "expires": "2026-03-01"}},
        2: {"name": "Bob", "email": "bob@example.com", "subscription": None},
        12: {"name": "Leander", "email": "leander.rodrigues@sentry.io", "subscription": {"plan": "free", "expires": "2026-12-31"}},
    }
    return users.get(user_id)


def error():
    user = get_user_profile(12)
    subscription = user.get("subscription")
    if subscription:
        plan = subscription.get("plan")
    else:
        plan = None
