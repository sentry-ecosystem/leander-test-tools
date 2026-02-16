import * as Sentry from "@sentry/nextjs";
import { NextResponse } from 'next/server';

// Configure this Edge Function to use the Edge Runtime
export const config = {
  runtime: 'edge',
};

/**
 * Vercel Edge Function for testing error handling and Sentry integration.
 * This function handles error generation and ensures proper trace data is captured.
 */
export default async function handler(req) {
  // Extract transaction name from query params or use default
  const url = new URL(req.url);
  const transactionName = url.searchParams.get('transaction') || 'test-transaction-0';
  const errorName = url.searchParams.get('error') || 'robots-welcome-a';
  
  // Start a Sentry transaction to ensure trace context is captured
  const transaction = Sentry.startTransaction({
    op: 'edge.function',
    name: transactionName,
    tags: {
      'generated-by': 'error-generator.sentry.dev',
      'logger': 'edge-function',
      'server': 'vercel-edge-function',
    },
  });

  try {
    // Set the transaction as the active span
    Sentry.getCurrentHub().configureScope((scope) => {
      scope.setSpan(transaction);
    });

    // Add additional context to the transaction
    Sentry.setContext('edge_runtime', {
      url: req.url,
      method: req.method,
      headers: Object.fromEntries(req.headers),
      timestamp: new Date().toISOString(),
    });

    // Set user context if provided
    const userId = url.searchParams.get('user') || 'test-user-0';
    Sentry.setUser({
      id: userId,
      username: userId,
    });

    // Add tags for better error tracking
    Sentry.setTag('edge-function', 'error-handler');
    Sentry.setTag('environment', 'default');

    // Create and throw the error with proper context
    const error = new Error(errorName);
    error.name = errorName;
    
    // Add breadcrumbs to provide context
    Sentry.addBreadcrumb({
      category: 'edge-function',
      message: `Generating error: ${errorName}`,
      level: 'info',
      data: {
        transaction: transactionName,
        errorName: errorName,
      },
    });

    // Capture the exception with full context
    Sentry.withScope((scope) => {
      scope.setContext('error_details', {
        errorName: errorName,
        transactionName: transactionName,
        generatedBy: 'error-generator.sentry.dev',
      });
      
      scope.setContext('request_info', {
        url: req.url,
        method: req.method,
        userAgent: req.headers.get('user-agent'),
      });

      // Associate the error with the transaction
      scope.setSpan(transaction);
      
      Sentry.captureException(error);
    });

    // Finish the transaction with error status
    transaction.setStatus('internal_error');
    transaction.finish();

    // Ensure Sentry events are flushed before response
    await Sentry.flush(2000);

    // Return error response
    return new NextResponse(JSON.stringify({
      success: false,
      message: `Error "${errorName}" captured in transaction "${transactionName}"`,
      error: error.message,
      transaction: transactionName,
      timestamp: new Date().toISOString(),
    }), {
      status: 500,
      headers: {
        'content-type': 'application/json',
      },
    });

  } catch (handlerError) {
    // Catch any errors that occur during error handling itself
    console.error('Error in edge function handler:', handlerError);
    
    Sentry.captureException(handlerError);
    transaction.setStatus('internal_error');
    transaction.finish();
    
    await Sentry.flush(2000);

    return new NextResponse(JSON.stringify({
      success: false,
      message: 'An unexpected error occurred',
      error: handlerError.message,
    }), {
      status: 500,
      headers: {
        'content-type': 'application/json',
      },
    });
  }
}