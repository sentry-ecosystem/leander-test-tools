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
  dsn: "http://c2f5f4bd6b024244bdcaa092117475f1@localhost:8000/4",
  integrations: [
    // new SentryFullStory("leander-test"),
    new TracingIntegrations.BrowserTracing({
      tracingOrigins: ["localhost", "catfact.ninja", /^\//],
      shouldCreateSpanForRequest: (_url) => true,
    }),
  ],
  tracesSampleRate: 1.0,
});

ReactDOM.render(<App />, document.getElementById("root"));
