import { NextRequest, NextResponse } from 'next/server';
import * as Sentry from '@sentry/node';

// Initialize Sentry for Edge Functions
Sentry.init({
  dsn: process.env.SENTRY_DSN || 'https://examplePublicKey@o0.ingest.sentry.io/0',
  environment: process.env.VERCEL_ENV || 'development',
  tracesSampleRate: 1.0,
  integrations: [
    new Sentry.Integrations.Http({ tracing: true }),
  ],
});

/**
 * Vercel Edge Function that demonstrates proper Sentry transaction handling.
 * 
 * IMPORTANT: Edge Functions have unique runtime characteristics where the process
 * can terminate before Sentry's automatic event transmission completes. This requires
 * an explicit call to `await Sentry.flush()` before returning the response to ensure
 * transaction data is actually sent to Sentry.
 */
export const config = {
  runtime: 'nodejs',
};

export default async function handler(
  request: NextRequest
): Promise<NextResponse> {
  // Create a transaction for this handler
  const transaction = Sentry.startTransaction({
    op: 'http.server',
    name: 'Test Transaction - Edge Function',
  });

  // Set transaction on the scope
  Sentry.setCurrentClient(new Sentry.NodeClient({
    dsn: process.env.SENTRY_DSN || 'https://examplePublicKey@o0.ingest.sentry.io/0',
  }));

  try {
    // Simulate some work with a span
    const span = transaction.startChild({
      op: 'task.process',
      description: 'Simulated processing task',
    });

    // Simulate work
    let counter = 0;
    while (counter < 10000) {
      counter++;
    }

    span.finish();

    // Mark transaction as successful
    transaction.setStatus('ok');

    return NextResponse.json(
      { message: 'Transaction completed successfully' },
      { status: 200 }
    );
  } catch (error) {
    // Capture any errors
    Sentry.captureException(error);
    transaction.setStatus('error');

    return NextResponse.json(
      { error: 'Transaction failed', message: error instanceof Error ? error.message : 'Unknown error' },
      { status: 500 }
    );
  } finally {
    // CRITICAL: Finish the transaction
    transaction.finish();

    /**
     * MANUAL FLUSH REQUIRED FOR EDGE FUNCTIONS
     * 
     * This is the crucial step that was missing before. Edge Functions don't guarantee
     * that background operations (like Sentry's automatic event batching) will complete
     * before the function finishes execution and the process terminates.
     * 
     * Without this explicit flush, transaction data gets lost because the HTTP response
     * is sent back before Sentry finishes its async operations to transmit the event.
     * 
     * This is why "manual intervention" was needed - developers must explicitly wait
     * for Sentry to finish sending before the function can complete.
     */
    await Sentry.flush(2000); // Wait up to 2 seconds for events to be sent
  }
}