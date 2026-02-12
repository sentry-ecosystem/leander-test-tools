import * as Sentry from '@sentry/nextjs';
import { v4 as uuidv4 } from 'uuid';

// Initialize Sentry for Edge Runtime
Sentry.init({
  dsn: process.env.SENTRY_DSN || 'https://234c699ac7f8b1dfd98765149a65b9fd@o4506792933130240.ingest.us.sentry.io/4509407223152640',
  tracesSampleRate: 1.0,
  environment: process.env.VERCEL_ENV || 'development',
  integrations: [],
});

export const config = {
  runtime: 'edge',
};

export default async function handler(request) {
  const { searchParams } = new URL(request.url);
  const errorNumber = searchParams.get('error') || '1';
  
  // Generate UUID for transaction name
  const transactionId = uuidv4();
  const transactionName = `test-transaction-0-${transactionId}`;
  
  // Start a transaction
  const transaction = Sentry.startTransaction({
    op: 'http.server',
    name: transactionName,
  });
  
  // Set the transaction on the current scope
  Sentry.getCurrentHub().configureScope((scope) => {
    scope.setSpan(transaction);
    
    // Set specific tags
    scope.setTag('logger', 'edge-function');
    scope.setTag('server', 'vercel-edge-function');
    scope.setTag('generated_by', 'error-generator.sentry.dev');
  });
  
  try {
    // Generate the error based on the error parameter
    throw new Error(`Error ${errorNumber}`);
  } catch (error) {
    // Capture the error with Sentry
    Sentry.captureException(error);
    
    // Finish the transaction
    transaction.finish();
    
    // Flush the Sentry event to ensure it's sent before response
    await Sentry.flush(2000);
    
    // Return error response
    return new Response(
      JSON.stringify({
        error: error.message,
        transaction: transactionName,
        timestamp: new Date().toISOString(),
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