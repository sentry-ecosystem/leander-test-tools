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
  dsn: "https://6338209daaba4a868fca858e3f7ebfc2@o951660.ingest.sentry.io/6507927",
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
