# Sentry Test Tools (Leander)

A repo of error generating projects to debug sentry locally.

## Flask-Error

A small project useful for generating errors in a flask project. 
Set it up with `make setup` and `make install`.
Run it with `python app.py [sentry | getsentry | hosted]`, and go to [http://127.0.0.1:5000/error](http://127.0.0.1:5000/error) to trigger server errors.

Defaults to `sentry` as the error location (local development on `getsentry/sentry`). `getsentry` points to `getsentry/getsentry` development. `hosted` points to `sentry.io`.

## React-Error

Automated error generation in a react project. Useful for generating many events on a single issue with a variety of tags unique properties.
## Vercel Edge Function Error Generator

A Vercel Edge Function that generates the `robots-welcome` error for testing Sentry's integration with edge functions.

### Setup

1. Install dependencies:
   ```
   npm install
   ```

2. Set your Sentry DSN in environment variables:
   ```
   export SENTRY_DSN="your-sentry-dsn-here"
   ```

### Running Locally

To run the edge function locally:
```
npm run dev
```

Then visit `http://localhost:3000/api/robots` to trigger the `robots-welcome` error.

### Deployment

Deploy to Vercel:
```
vercel deploy
```

After deployment, visit `https://your-vercel-url.vercel.app/api/robots` to trigger the error.