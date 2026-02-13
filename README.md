# Sentry Test Tools (Leander)

A repo of error generating projects to debug sentry locally.

## Flask-Error

A small project useful for generating errors in a flask project. 
Set it up with `make setup` and `make install`.
Run it with `python app.py [sentry | getsentry | hosted]`, and go to [http://127.0.0.1:5000/error](http://127.0.0.1:5000/error) to trigger server errors.

Defaults to `sentry` as the error location (local development on `getsentry/sentry`). `getsentry` points to `getsentry/getsentry` development. `hosted` points to `sentry.io`.

## React-Error

Automated error generation in a react project. Useful for generating many events on a single issue with a variety of tags unique properties.
## Vercel Edge Functions

This repo includes a Vercel Edge Function handler for testing Sentry transactions in edge function environments.

### Important: Manual Sentry.flush() in Edge Functions

Edge functions (like Vercel Edge Functions) have unique runtime characteristics that require special handling for Sentry event transmission.

**The Problem:**
In traditional web server environments (Flask, Express, etc.), Sentry automatically batches and transmits events asynchronously. The process remains active long enough for Sentry to complete its operations. However, in serverless/edge computing environments:
- The process can terminate immediately after the HTTP response is sent
- Background operations like Sentry's event batching may not complete before termination
- This results in lost transaction and event data

**The Solution:**
Always explicitly call `await Sentry.flush(timeout)` in the `finally` block of your edge function handlers before the function completes. This ensures that all pending Sentry events and transactions are sent to Sentry before the process terminates.

### Example - Transaction Handler

See `/api/transaction.ts` for a working example of:
- Creating a Sentry transaction in an edge function
- Creating child spans
- Properly handling errors
- **Crucially: Using `await Sentry.flush()` before function completion**

This pattern is essential for edge functions but is generally NOT needed in traditional web server environments, making it an "unexpected manual intervention" for developers unfamiliar with serverless monitoring patterns.