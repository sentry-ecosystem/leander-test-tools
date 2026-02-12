import * as Sentry from "@sentry/nextjs";

/**
 * Sentry configuration for Vercel Edge Runtime
 * This configuration ensures proper error tracking and performance monitoring
 * in the Edge Function environment.
 */
Sentry.init({
  // Set your Sentry DSN here - can be overridden via environment variable
  dsn: process.env.SENTRY_DSN || process.env.NEXT_PUBLIC_SENTRY_DSN,

  // Adjust this value in production, or use tracesSampler for greater control
  // Set to 1.0 to capture 100% of transactions for performance monitoring
  tracesSampleRate: 1.0,

  // Enable debug mode for troubleshooting (disable in production)
  debug: process.env.NODE_ENV === 'development',

  // Set the environment (e.g., 'production', 'staging', 'development')
  environment: process.env.VERCEL_ENV || process.env.NODE_ENV || 'default',

  // Enable performance monitoring
  enableTracing: true,

  // Capture all errors by default
  sampleRate: 1.0,

  // Integrations specific to Edge Runtime
  integrations: [
    // Transaction tracking integration
    new Sentry.Integrations.Http({ tracing: true }),
  ],

  // Add default tags for all events
  initialScope: {
    tags: {
      'runtime': 'edge',
      'server': 'vercel-edge-function',
      'logger': 'edge-function',
    },
  },

  // Configure what to send to Sentry
  beforeSend(event, hint) {
    // Add custom logic here if needed (e.g., filtering, modifying events)
    // For now, send all events as-is
    return event;
  },

  // Configure transaction sampling
  tracesSampler(samplingContext) {
    // Sample 100% of transactions for edge functions
    // You can customize this based on transaction name, operation, etc.
    return 1.0;
  },

  // Attach stack traces to pure capture messages
  attachStacktrace: true,

  // Maximum breadcrumbs to store
  maxBreadcrumbs: 50,

  // Send session data
  autoSessionTracking: true,

  // Release tracking (if using Sentry releases)
  release: process.env.VERCEL_GIT_COMMIT_SHA,
});