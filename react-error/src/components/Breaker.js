import React, { useEffect, useState } from "react";
import { captureException, configureScope } from "@sentry/browser";
import info from "./info.json";

const { names, handles } = info;

/* eslint-disable-next-line */
Array.prototype.randomElement = function () {
  return this[Math.floor(Math.random() * this.length)];
};

const getNum = (min, max) => {
  return Math.floor(Math.random() * (max - min)) + min;
};

const getEmail = (name) => name + "@" + handles.randomElement() + ".com";

const Breaker = () => {
  const [times, updateTimes] = useState(0);
  useEffect(() => {
    const interval = setInterval(() => {
      const username = names.randomElement() + getNum(10, 99);
      const user = {
        id: getNum(10000000, 99999999),
        username,
        email: getEmail(username),
      };
      configureScope((scope) => {
        scope.setUser(user);
        scope.setTag("best_friend", names.randomElement());
        scope.setTag("is_cool", Math.random() > 0.5);
      });
      captureException(
        new SyntaxError("Oops, we let the intern make this feature 😬")
      );
      updateTimes(times + 1);
    }, 1000);
    return () => clearInterval(interval);
  });

  return <div>I've broken my code {times} times</div>;
};

export default Breaker;
