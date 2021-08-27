import React from "react";
import styled from "styled-components";

import Breaker from "./components/Breaker";

const App = () => {
  return (
    <StylishPage>
      <Breaker />
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
`;

export default App;
