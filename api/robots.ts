import * as Sentry from "@sentry/nextjs";

export const config = {
  runtime: "edge",
};

export default function handler(request: Request): Response {
  try {
    throw new Error("robo");
  } catch (error) {
    Sentry.captureException(error);
    return new Response(JSON.stringify({ error: "robo" }), {
      status: 500,
      headers: { "Content-Type": "application/json" },
    });
  }
}