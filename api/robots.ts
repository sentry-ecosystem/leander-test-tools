import { NextRequest, NextResponse } from 'next/server';
import * as Sentry from '@sentry/nextjs';

// Initialize Sentry for Edge Functions
Sentry.init({
  dsn: process.env.SENTRY_DSN,
  environment: process.env.VERCEL_ENV || 'development',
  tracesSampleRate: 1.0,
  integrations: [
    new Sentry.Integrations.OnUncaughtException(),
  ],
});

export const runtime = 'edge';

export default async function handler(req: NextRequest) {
  try {
    // Set user context
    Sentry.setUser({
      id: 'test-user-0-22d8f4e7-3b01-41e8-92ee-d89f5a84510f',
      username: 'test-user',
      email: 'test@example.com',
    });

    // Set transaction context
    const transaction = Sentry.startTransaction({
      op: 'http.server',
      name: 'test-transaction-0',
    });

    Sentry.getCurrentHub().setSpan(transaction);

    // Simulate a robots-welcome error
    const error = new Error('robots-welcome');
    error.name = 'robots-welcome';
    
    // Capture the error with additional context
    Sentry.captureException(error, {
      tags: {
        environment: 'vercel-edge-function',
        logger: 'edge-function',
      },
      contexts: {
        trace: {
          trace_id: transaction.traceId,
          span_id: transaction.spanId,
        },
      },
    });

    transaction.finish();

    return NextResponse.json(
      { error: 'robots-welcome' },
      { status: 500 }
    );
  } catch (error) {
    Sentry.captureException(error);
    return NextResponse.json(
      { error: 'Internal Server Error' },
      { status: 500 }
    );
  }
}