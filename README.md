# Sentry Test Tools (Leander)

A repo of error generating projects to debug sentry locally.

## Flask-Error

A small project useful for generating errors in a flask project. 
Set it up with `make setup` and `make install`.
Run it with `python app.py [sentry | getsentry | hosted]`, and go to [http://127.0.0.1:5000/error](http://127.0.0.1:5000/error) to trigger server errors.

Defaults to `sentry` as the error location (local development on `getsentry/sentry`). `getsentry` points to `getsentry/getsentry` development. `hosted` points to `sentry.io`.

### Filtering Synthetic Test Errors

The Flask error application now includes built-in filtering to prevent synthetic test errors from polluting production error monitoring. The `before_send` callback automatically filters out:

- **Test transaction patterns**: Errors with transaction names matching `test-transaction-*` (e.g., `test-transaction-0-49abf9f4-3cc0-42d3-949f-adbc45c214bd`)
- **Known test error names**: Errors named `robots-welcome` or matching `test-error-*` patterns
- **Tagged test events**: Events with tags like `synthetic_test=true` or `error_generator=true`
- **Error generator contexts**: Events with `error_generator` context information

#### Environment Configuration

The filtering behavior can be controlled using environment variables:

- **`FLASK_ENV`**: Set to `production` (default) to enable strict filtering, or `development`/`test` to allow test errors through for debugging
- **`ALLOW_TEST_ERRORS`**: Set to `true` to explicitly allow synthetic test errors even in production (not recommended)

Example usage:
```bash
# Production mode - filters all synthetic test errors (default)
python app.py

# Development mode - allows synthetic test errors for testing
FLASK_ENV=development python app.py

# Explicitly allow test errors in production (not recommended)
FLASK_ENV=production ALLOW_TEST_ERRORS=true python app.py
```

This ensures that tools like `error-generator.sentry.dev` can send test errors for validation purposes without creating noise in your production error monitoring.

## React-Error

Automated error generation in a react project. Useful for generating many events on a single issue with a variety of tags unique properties.