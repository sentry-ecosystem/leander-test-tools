import React, { useEffect, useState } from "react";
import { captureException, configureScope } from "@sentry/browser";

// import * as FullStory from "@fullstory/browser";
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
      const bestFriend = names.randomElement();
      const isCool = Math.random() > 0.5;
      configureScope((scope) => {
        scope.setUser(user);
        scope.setTag("best_friend", bestFriend);
        scope.setTag("is_cool", isCool);
      });
      // Send exception to Sentry
      captureException(new SyntaxError("🔥🔥🔥 Error 5"));
      // Send event to FullStory
      // FullStory.event("Started Errors", {
      //   user,
      //   best_friend: bestFriend,
      //   is_cool: isCool,
      // });
      updateTimes(times + 1);
    }, 1000);
    return () => clearInterval(interval);
  });

  return <div>I've broken my code {times} times</div>;
};

export default Breaker;
