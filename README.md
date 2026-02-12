# Sentry Test Tools (Leander)

A repo of error generating projects to debug sentry locally.

## Flask-Error

A small project useful for generating errors in a flask project. 
Set it up with `make setup` and `make install`.
Run it with `python app.py [sentry | getsentry | hosted]`, and go to [http://127.0.0.1:5000/error](http://127.0.0.1:5000/error) to trigger server errors.

Defaults to `sentry` as the error location (local development on `getsentry/sentry`). `getsentry` points to `getsentry/getsentry` development. `hosted` points to `sentry.io`.

## React-Error

Automated error generation in a react project. Useful for generating many events on a single issue with a variety of tags unique properties.
## Edge-Function

A Vercel Edge Function for generating test errors in a serverless edge environment. This function generates "Error 5" type errors within test transactions.

### Setup

1. Install dependencies:
   ```bash
   cd edge-function
   npm install
   ```

2. Configure your Sentry DSN:
   ```bash
   cp .env.example .env
   # Edit .env and add your SENTRY_DSN
   ```

3. Deploy to Vercel:
   ```bash
   npm run deploy
   ```

   Or run locally:
   ```bash
   npm run dev
   ```

### Usage

Once deployed, trigger errors by visiting:
```
https://your-deployment.vercel.app/api/error
```

You can specify different error numbers:
```
https://your-deployment.vercel.app/api/error?error=5
```

Each request generates a unique test transaction with the format `test-transaction-0-{uuid}` and sends the error to Sentry with appropriate tags (`logger: edge-function`, `server: vercel-edge-function`, `generated_by: error-generator.sentry.dev`).