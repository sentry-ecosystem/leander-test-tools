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
  try {
    // Generate the 'robots-welcome' error
    const error = new Error('robots-welcome');
    error.name = 'robots-welcome';
    
    Sentry.captureException(error, {
      tags: {
        environment: 'edge-function',
        location: 'robots endpoint',
      },
      contexts: {
        "robot": {
          "type": "welcome",
          "status": "active"
        }
      }
    });

    return NextResponse.json(
      { message: 'robots-welcome error captured' },
      { status: 500 }
    );
  } catch (error) {
    Sentry.captureException(error);
    return NextResponse.json(
      { error: 'Internal server error' },
      { status: 500 }
    );
  }
}