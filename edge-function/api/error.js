import * as Sentry from '@sentry/nextjs';

// Configure Sentry for edge runtime
Sentry.init({
  dsn: process.env.SENTRY_DSN,
  environment: 'vercel-edge-function',
  tracesSampleRate: 1.0,
  // Additional tags to match the issue details
  initialScope: {
    tags: {
      server: 'vercel-edge-function',
      logger: 'edge-function',
      generated_by: 'error-generator.sentry.dev'
    }
  }
});

export const config = {
  runtime: 'edge',
};

/**
 * Vercel Edge Function to generate test errors for Sentry
 * Generates Error 5 within a test transaction
 */
export default async function handler(request) {
  const url = new URL(request.url);
  const errorNumber = url.searchParams.get('error') || '5';
  
  // Generate a unique transaction ID
  const transactionId = `test-transaction-0-${crypto.randomUUID()}`;
  
  try {
    // Start a Sentry transaction
    const transaction = Sentry.startTransaction({
      op: 'edge-function',
      name: transactionId,
      tags: {
        error_type: `Error ${errorNumber}`,
        function_type: 'edge-function'
      }
    });
    
    Sentry.getCurrentHub().configureScope((scope) => {
      scope.setSpan(transaction);
      scope.setTag('transaction_id', transactionId);
    });

    // Throw the error
    throw new Error(`Error ${errorNumber}`);
    
  } catch (error) {
    // Capture the exception to Sentry
    Sentry.captureException(error);
    
    // Return error response
    return new Response(
      JSON.stringify({
        error: error.message,
        transaction: transactionId,
        timestamp: new Date().toISOString()
      }),
      {
        status: 500,
        headers: {
          'Content-Type': 'application/json',
        },
      }
    );
  }
}