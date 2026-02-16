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

A Vercel Edge Function for generating test errors in a serverless edge environment. Useful for testing Sentry error tracking in edge runtime environments.

### Features
- Generates numbered errors (Error 1-5) based on query parameters
- Creates transactions with unique UUIDs in the format `test-transaction-0-{uuid}`
- Automatically tags errors with:
  - `logger: edge-function`
  - `server: vercel-edge-function`
  - `generated_by: error-generator.sentry.dev`

### Setup
Set up with `npm install` in the `edge-function/` directory.

### Usage
Trigger errors via: `https://your-deployment.vercel.app/api/error?error=5`

Where the `error` parameter can be any number (e.g., 1-5). The function will generate an error with that number.

### Deployment
Deploy to Vercel using `npm run deploy` or connect your repository to Vercel for automatic deployments.

See `edge-function/README.md` for detailed documentation.