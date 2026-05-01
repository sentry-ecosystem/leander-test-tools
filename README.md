# Sentry Test Tools (Leander)

A repo of error generating projects to debug sentry locally.

## Flask-Error

A small project useful for generating errors in a flask project. 
Set it up with `make setup` and `make install`.
Run it with `python app.py [sentry | getsentry | hosted]`, and go to [http://127.0.0.1:5000/error](http://127.0.0.1:5000/error) to trigger server errors.

Defaults to `sentry` as the error location (local development on `getsentry/sentry`). `getsentry` points to `getsentry/getsentry` development. `hosted` points to `sentry.io`.

## React-Error

Automated error generation in a react project. Useful for generating many events on a single issue with a variety of tags unique properties.

## Edge-Error

Vercel Edge Function error generator for Sentry testing. Generates synthetic errors inside named test transactions in the Edge runtime.

Deploy with `vercel --prod` or run locally with `vercel dev`. Trigger error scenarios via query parameters:

- `GET /api/error?scenario=gotcha+1` — generates a TypeError
- `GET /api/error?scenario=gotcha+2` — generates an Error
- `GET /api/error?scenario=gotcha+3` — generates a RangeError

Optional `txn` parameter sets the transaction suffix (e.g. `?scenario=gotcha+2&txn=abc123` creates `test-transaction-0-abc123`).