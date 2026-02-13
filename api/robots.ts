import { VercelRequest, VercelResponse } from "@vercel/node";
import * as Sentry from "@sentry/node";

// Initialize Sentry
Sentry.init({
  dsn: process.env.SENTRY_DSN,
  integrations: [
    new Sentry.Integrations.OnUncaughtException(),
    new Sentry.Integrations.OnUnhandledRejection(),
  ],
  tracesSampleRate: 1.0,
});

export default function handler(
  request: VercelRequest,
  response: VercelResponse
) {
  const transaction = Sentry.startTransaction({
    op: "http.server",
    name: "test-transaction-0",
  });

  try {
    Sentry.getCurrentHub().configureScope((scope) => {
      scope.setSpan(transaction);
    });

    // Generate the robots-welcome error
    const error = new Error("robots-welcome");
    throw error;
  } catch (error) {
    Sentry.captureException(error);
    transaction.setStatus("error");
    transaction.finish();

    response.status(500).json({
      error: "robots-welcome",
      message: "An error occurred in the robots endpoint",
    });
  }
}