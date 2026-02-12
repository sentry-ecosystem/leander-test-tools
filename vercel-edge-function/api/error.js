import * as Sentry from "@sentry/nextjs";

// Initialize Sentry
Sentry.init({
  dsn: process.env.SENTRY_DSN || "https://examplePublicKey@o0.ingest.sentry.io/0",
  environment: "edge-function",
  tracesSampleRate: 1.0,
});

export default async function handler(request) {
  const transaction = Sentry.startTransaction({
    op: "edge-function",
    name: "test-transaction-0",
  });

  try {
    Sentry.getCurrentHub().configureScope((scope) => {
      scope.setSpan(transaction);
    });

    // This is the error that needs to be fixed
    // The error message "humans-only" suggests this should be for humans only
    // but it's being thrown unconditionally
    throw new Error("humans-only");
  } catch (error) {
    Sentry.captureException(error);
    throw error;
  } finally {
    transaction.finish();
  }
}

export const config = {
  runtime: "edge",
};