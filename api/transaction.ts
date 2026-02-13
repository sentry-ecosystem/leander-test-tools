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
  const transaction = Sentry.startTransaction({
    op: 'http.server',
    name: 'test-transaction-0',
  });

  try {
    Sentry.getCurrentHub().setSpan(transaction);

    // Set user context
    Sentry.setUser({
      id: 'test-user-0-22d8f4e7-3b01-41e8-92ee-d89f5a84510f',
      username: 'test-user',
      email: 'test@example.com',
    });

    const span = transaction.startChild({
      op: 'db.query',
      description: 'Test database query',
    });

    // Simulate some async work
    await new Promise(resolve => setTimeout(resolve, 100));

    span.finish();

    // Add breadcrumb
    Sentry.addBreadcrumb({
      message: 'Test transaction completed',
      level: 'info',
      category: 'transaction',
    });

    transaction.finish();

    return NextResponse.json(
      { success: true, message: 'Transaction completed' },
      { status: 200 }
    );
  } catch (error) {
    transaction.setStatus('internal_error');
    Sentry.captureException(error, {
      contexts: {
        trace: {
          trace_id: transaction.traceId,
          span_id: transaction.spanId,
        },
      },
    });
    transaction.finish();

    return NextResponse.json(
      { error: 'Internal Server Error' },
      { status: 500 }
    );
  }
}