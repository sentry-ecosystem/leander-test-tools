import { NextRequest, NextResponse } from "next/server";
import * as Sentry from "@sentry/nextjs";

export const config = {
  runtime: "edge",
};

export default async function handler(req: NextRequest) {
  const transaction = Sentry.startTransaction({
    name: "robots-complete",
    op: "http.server",
  });

  try {
    Sentry.setCurrentClient(
      Sentry.getClient() || new Sentry.Client({})
    );

    // Simulate some work
    const span = transaction.startChild({
      description: "Process robots request",
      op: "task",
    });

    // Add some delay to simulate processing
    await new Promise((resolve) => setTimeout(resolve, 10));

    span.finish();

    const response = {
      status: "success",
      message: "Robots endpoint completed successfully",
      timestamp: new Date().toISOString(),
    };

    transaction.finish();

    return NextResponse.json(response, { status: 200 });
  } catch (error) {
    transaction.captureException(error);
    transaction.finish();

    return NextResponse.json(
      { status: "error", message: "An error occurred" },
      { status: 500 }
    );
  }
}