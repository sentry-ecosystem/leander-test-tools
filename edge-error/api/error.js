import * as Sentry from "@sentry/vercel-edge";

export const config = {
  runtime: "edge",
};

const GEN_DSN =
  "https://234c699ac7f8b1dfd98765149a65b9fd@o4506792933130240.ingest.us.sentry.io/4509407223152640";

Sentry.init({
  dsn: process.env.SENTRY_DSN || GEN_DSN,
  tracesSampleRate: 1.0,
});

const errorScenarios = {
  "gotcha 1": {
    generate: () => new TypeError("gotcha 1"),
    level: "error",
  },
  "gotcha 2": {
    generate: () => new Error("gotcha 2"),
    level: "error",
  },
  "gotcha 3": {
    generate: () => new RangeError("gotcha 3"),
    level: "warning",
  },
};

export default async function handler(request) {
  const url = new URL(request.url);
  const scenarioName = url.searchParams.get("scenario") || "gotcha 1";
  const txnSuffix = url.searchParams.get("txn") || Date.now();
  const transactionName = `test-transaction-0-${txnSuffix}`;

  return Sentry.startSpan(
    { name: transactionName, op: "test.scenario" },
    async () => {
      const scenario = errorScenarios[scenarioName];

      if (!scenario) {
        return new Response(
          JSON.stringify({ error: `Unknown scenario: ${scenarioName}` }),
          { status: 400, headers: { "Content-Type": "application/json" } }
        );
      }

      const error = scenario.generate();
      Sentry.captureException(error, {
        level: scenario.level,
        tags: {
          scenario: scenarioName,
          transaction: transactionName,
          runtime: "edge",
        },
      });

      await Sentry.flush(2000);

      return new Response(
        JSON.stringify({
          status: "captured",
          scenario: scenarioName,
          transaction: transactionName,
          level: scenario.level,
        }),
        { status: 200, headers: { "Content-Type": "application/json" } }
      );
    }
  );
}
