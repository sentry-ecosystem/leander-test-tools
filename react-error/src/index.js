import React from "react";
import ReactDOM from "react-dom";
import * as Sentry from "@sentry/browser";
import "./index.css";
import App from "./App";

Sentry.init({
  dsn: "http://c2f5f4bd6b024244bdcaa092117475f1@localhost:8000/4",
});

ReactDOM.render(<App />, document.getElementById("root"));
