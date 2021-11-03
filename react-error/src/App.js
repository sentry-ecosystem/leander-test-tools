import React, { useState } from "react";
import styled from "styled-components";
// import * as FullStory from "@fullstory/browser";
import * as Sentry from "@sentry/react";

import Breaker from "./components/Breaker";
import Pinger from "./components/Pinger";

const App = () => {
  const [throwErrors, setThrowErrors] = useState(false);
  const [sendRequests, setSendRequests] = useState(false);
  return (
    <StylishPage>
      {throwErrors && <Breaker />}
      {!throwErrors && (
        <div>
          <button
            onClick={() => {
              // FullStory.getCurrentSessionURL(true);
              setThrowErrors(true);
            }}
          >
            Throw some errors!
          </button>
        </div>
      )}
      {sendRequests && <Pinger />}
      {!sendRequests && (
        <div>
          <button
            onClick={() => {
              // FullStory.getCurrentSessionURL();
              setSendRequests(true);
            }}
          >
            Send some requests!
          </button>
        </div>
      )}
    </StylishPage>
  );
};

const StylishPage = styled.div`
  div {
    border-radius: 44px;
    background: #ceb4d4;
    box-shadow: 20px 20px 60px #af99b4, -20px -20px 60px #edcff4;
    margin: 50px auto;
    text-align: center;
    color: #8f7e93;
    max-width: 50vw;
    font-family: "Space Mono", "Courier New", Courier, monospace;
    font-weight: bold;
    padding: 100px 200px;
  }
  button {
    outline: 0;
    border: 0;
    background: transparent;
    font-family: inherit;
    font-weight: bold;
    font-size: 1rem;
    color: #8f7e93;
    cursor: pointer;
    padding: 1rem 2rem;
    border-radius: inherit;
    :hover {
      box-shadow: 20px 20px 60px #af99b4, -20px -20px 60px #edcff4;
    }
  }
`;

export default Sentry.withProfiler(App);
// export default App;
