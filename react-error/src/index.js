import React from "react";
import ReactDOM from "react-dom";
import * as Sentry from "@sentry/react";
// import * as FullStory from "@fullstory/browser";
// import SentryFullStory from "@sentry/fullstory";
import { Integrations as TracingIntegrations } from "@sentry/tracing";
import "./index.css";
import App from "./App";

// FullStory.init({ orgId: "164KVD" });

Sentry.init({
  dsn: "https://4bb8adf9789742c590395533a427a0e1@leeandher.ngrok.io/8",
  integrations: [
    // new SentryFullStory("leander-test"),
    new TracingIntegrations.BrowserTracing({
      tracingOrigins: ["localhost", "catfact.ninja", /^\//],
      shouldCreateSpanForRequest: (_url) => true,
    }),
  ],
  tracesSampleRate: 1.0,
  allowUrls: [/localhost/, /127\.0\.0\.1/],
  beforeSend(event) {
    // Filter out synthetic errors injected by external tools like error-generator.sentry.dev.
    // Real app errors will have stack frames referencing local source files;
    // synthetic errors from the error generator have no such frames.
    if (event.exception && event.exception.values) {
      const hasAppFrames = event.exception.values.some((ex) => {
        const frames = (ex.stacktrace && ex.stacktrace.frames) || [];
        return frames.some(
          (frame) =>
            frame.filename &&
            (frame.filename.includes("localhost") ||
              frame.filename.includes("/src/") ||
              frame.filename.includes("webpack"))
        );
      });
      if (!hasAppFrames) {
        return null;
      }
    }
    return event;
  },
});

Sentry.setContext("session_id", "12123");

ReactDOM.render(<App />, document.getElementById("root"));
