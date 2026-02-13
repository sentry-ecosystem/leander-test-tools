# Sentry Test Tools (Leander)

A repo of error generating projects to debug sentry locally.

## Flask-Error

A small project useful for generating errors in a flask project. 
Set it up with `make setup` and `make install`.
Run it with `python app.py [sentry | getsentry | hosted]`, and go to [http://127.0.0.1:5000/error](http://127.0.0.1:5000/error) to trigger server errors.

Defaults to `sentry` as the error location (local development on `getsentry/sentry`). `getsentry` points to `getsentry/getsentry` development. `hosted` points to `sentry.io`.

## React-Error

Automated error generation in a react project. Useful for generating many events on a single issue with a variety of tags unique properties.
## Vercel Edge Functions (API)

This directory contains Vercel Edge Function handlers that demonstrate proper Sentry integration patterns.

### Transaction Handler (`/api/transaction`)

Demonstrates how to properly handle Sentry transactions in Vercel Edge Functions.

**Key Feature: Manual `Sentry.flush()`**

Edge Functions have unique runtime characteristics that require special handling for Sentry transactions:

- **The Problem**: Edge Function processes can terminate before Sentry's automatic event transmission completes, causing transaction data to be lost.
- **The Solution**: Explicitly call `await Sentry.flush()` before the handler returns to ensure all event data is sent to Sentry.
- **Why Manual Intervention is Necessary**: Unlike traditional web servers that have persistent processes and background workers, Edge Functions have limited execution time and no guarantee that async operations will complete after the response is sent.

**Example Usage:**

```typescript
export default async function handler(request: NextRequest): Promise<NextResponse> {
  const transaction = Sentry.startTransaction({
    op: 'http.server',
    name: 'My Transaction',
  });

  try {
    // Do work...
    transaction.setStatus('ok');
  } catch (error) {
    Sentry.captureException(error);
    transaction.setStatus('error');
  } finally {
    transaction.finish();
    // CRITICAL: Flush events before returning
    await Sentry.flush(2000); // Wait up to 2 seconds for events to be sent
  }

  return NextResponse.json({ success: true });
}
```

**Deployment**: When deployed to Vercel, hit `/api/transaction` to trigger the example transaction.

**Configuration**: Set the `SENTRY_DSN` environment variable in your Vercel project settings to send data to your Sentry project.