import React, { useEffect, useState } from "react";
import * as Sentry from "@sentry/react";
import { SpanStatus } from "@sentry/tracing";

const Pinger = () => {
  const [fact, setFact] = useState("This is supposed to be a cat face! 🙀");
  useEffect(() => {
    const transaction = Sentry.startTransaction({ name: "get-fact" });
    Sentry.getCurrentHub().configureScope((scope) =>
      scope.setSpan(transaction)
    );
    async function getFact() {
      const factResponse = await fetch("https://catfact.ninja/fact", {
        method: "GET",
        mode: "cors",
        headers: { "Access-Control-Allow-Headers": "sentry-trace" },
      });

      const result = await factResponse.json();
      const span = transaction.startChild({
        data: {
          result,
        },
        op: "task",
        description: "Fetches a new cat fact.",
      });
      setFact(result.fact);
      span.setStatus(SpanStatus.Ok);
      span.finish();
      transaction.finish();
    }

    // setInterval(() => {
    //   getFact();
    // }, 1000);
    getFact();
    transaction.finish();
  }, []);

  return <div>{fact}</div>;
};

export default Pinger;
