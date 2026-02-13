import { NextRequest, NextResponse } from 'next/server';
import * as Sentry from "@sentry/nextjs";

export const config = {
  runtime: 'edge',
};

Sentry.init({
  dsn: process.env.SENTRY_DSN,
  tracesSampleRate: 1.0,
});

export default async function handler(req: NextRequest) {
  try {
    // Generate the robots-welcome error
    const error = new Error('robots-welcome');
    error.name = 'robots-welcome';
    
    // Capture the error with Sentry
    Sentry.captureException(error, {
      contexts: {
        app: {
          server: 'vercel-edge-function',
        },
      },
      tags: {
        logger: 'edge-function',
      },
      transaction: 'test-transaction-0',
    });
    
    throw error;
  } catch (error) {
    Sentry.captureException(error);
    return NextResponse.json(
      { error: 'robots-welcome error generated' },
      { status: 500 }
    );
  }
}