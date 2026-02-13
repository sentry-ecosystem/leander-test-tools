import { VercelResponse, VercelRequest } from '@vercel/node';
import * as Sentry from '@sentry/node';

// Initialize Sentry for the edge function
Sentry.init({
  dsn: process.env.SENTRY_DSN || '',
  tracesSampleRate: 1.0,
  environment: process.env.VERCEL_ENV || 'development',
  integrations: [
    new Sentry.Integrations.Http({ tracing: true }),
  ],
});

/**
 * Vercel Edge Function handler for creating a test transaction.
 * 
 * IMPORTANT: This function demonstrates the critical pattern required for
 * Sentry transaction handling in edge function environments.
 * 
 * Edge functions have unique runtime characteristics where the process can
 * terminate before Sentry's automatic event transmission completes. Without
 * the explicit await Sentry.flush() call below, transaction data would be
 * lost because the HTTP response is sent before Sentry finishes its async
 * operations.
 * 
 * This is NOT required in traditional web server environments like Flask,
 * but IS required in serverless/edge computing contexts.
 */
export default async function handler(
  req: VercelRequest,
  res: VercelResponse
) {
  // Create a transaction for this request
  const transaction = Sentry.startTransaction({
    op: 'http.server',
    name: 'test-transaction',
    description: 'Test transaction in Vercel Edge Function',
  });

  try {
    // Create a child span
    const span = transaction.startChild({
      op: 'task',
      description: 'Simulating work in edge function',
    });

    // Simulate some work
    let counter = 1;
    while (counter < 10000) {
      counter = counter + 1;
    }

    span.finish();

    // Return the response
    return res.status(200).json({
      success: true,
      message: 'Transaction completed successfully',
      transactionId: transaction.traceId,
    });
  } catch (error) {
    // Capture any errors that occur
    Sentry.captureException(error);
    transaction.setStatus('internal_error');
    return res.status(500).json({
      success: false,
      message: 'An error occurred during transaction processing',
      error: error instanceof Error ? error.message : 'Unknown error',
    });
  } finally {
    // CRITICAL: Finish the transaction
    transaction.finish();

    // CRITICAL: Explicitly flush Sentry events before the function terminates.
    // This is essential in edge function environments where the process may
    // terminate immediately after the response is sent, preventing Sentry's
    // automatic batching and transmission from completing.
    //
    // This manual intervention is NOT typical in traditional web environments,
    // but is necessary for Vercel Edge Functions and other serverless/edge
    // computing contexts.
    await Sentry.flush(2000);
  }
}