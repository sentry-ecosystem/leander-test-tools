import React from "react";
import ReactDOM from "react-dom";
import * as Sentry from "@sentry/browser";
import "./index.css";
import App from "./App";

Sentry.init({
  dsn: "http://b4ac771c9a324728abf8ea7bcde34fca@localhost:8000/2"
});

ReactDOM.render(<App />, document.getElementById("root"));
