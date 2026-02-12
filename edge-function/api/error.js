/**
 * Vercel Edge Function for testing error handling and Sentry integration
 * Only generates errors when explicitly requested via query parameters
 */

import * as Sentry from '@sentry/node';

export const config = {
  runtime: 'edge',
};

export default async function handler(request) {
  const url = new URL(request.url);
  
  // Extract query parameters - NOTE: No defaults for error parameter
  const transactionName = url.searchParams.get('transaction') || 'test-transaction-0';
  const errorName = url.searchParams.get('error'); // No default - must be explicitly provided
  const userName = url.searchParams.get('user') || 'test-user-0';
  
  // Only generate errors if explicitly requested
  if (!errorName) {
    // Return success response when no error is requested
    return new Response(
      JSON.stringify({
        status: 'ok',
        message: 'Edge function is working. Add ?error=<error-name> to generate an error.',
        availableParams: {
          transaction: 'Transaction name (default: test-transaction-0)',
          error: 'Error name (required to trigger error)',
          user: 'User name (default: test-user-0)'
        }
      }),
      {
        status: 200,
        headers: {
          'Content-Type': 'application/json',
        },
      }
    );
  }

  // Initialize Sentry transaction for error tracking
  const transaction = Sentry.startTransaction({
    op: 'edge.function',
    name: transactionName,
    data: {
      url: request.url,
      method: request.method,
    },
  });

  try {
    // Add breadcrumb for tracking
    Sentry.addBreadcrumb({
      category: 'edge.function',
      message: `Generating error: ${errorName}`,
      level: 'info',
      data: {
        transaction: transactionName,
        error: errorName,
        user: userName,
      },
    });

    // Set user context
    Sentry.setUser({
      username: userName,
      id: userName,
    });

    // Set tags
    Sentry.setTag('generator', 'error-generator.sentry.dev');
    Sentry.setTag('logger', 'edge-function');
    Sentry.setTag('transaction', transactionName);

    // Create and throw the error with proper context
    const error = new Error(errorName);
    error.name = errorName;
    
    // Capture the error with Sentry
    Sentry.captureException(error);
    
    // Mark transaction as failed
    transaction.setStatus('internal_error');
    
    // Return error response
    return new Response(
      JSON.stringify({
        error: errorName,
        transaction: transactionName,
        user: userName,
        message: 'Error generated and captured by Sentry',
      }),
      {
        status: 500,
        headers: {
          'Content-Type': 'application/json',
        },
      }
    );
  } finally {
    // Finish the transaction
    transaction.finish();
  }
}