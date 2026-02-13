import { NextRequest, NextResponse } from 'next/server';
import * as Sentry from "@sentry/nextjs";

export const config = {
  runtime: 'edge',
};

Sentry.init({
  dsn: process.env.SENTRY_DSN || "https://examplePublicKey@o0.ingest.sentry.io/0",
  tracesSampleRate: 1.0,
  environment: 'edge-function',
});

export default async function handler(req: NextRequest) {
  const transaction = Sentry.startTransaction({
    op: 'http.server',
    name: 'test-transaction-0',
    description: 'Test transaction from Vercel Edge Function',
  });

  Sentry.setUser({
    id: 'test-user-0',
    username: 'test-user',
    email: 'test@example.com',
  });

  try {
    const span = transaction.startChild({
      op: 'http.client',
      description: 'Processing transaction data',
    });

    // Simulate some async work
    await new Promise(resolve => setTimeout(resolve, 100));

    span.finish();

    return NextResponse.json(
      { 
        message: 'Transaction completed successfully',
        transactionId: 'test-transaction-0',
        status: 'success'
      },
      { status: 200 }
    );
  } catch (error) {
    transaction.setStatus('error');
    Sentry.captureException(error, {
      tags: {
        'transaction.op': 'http.server',
      }
    });

    return NextResponse.json(
      { error: 'Transaction failed' },
      { status: 500 }
    );
  } finally {
    transaction.finish();
  }
}