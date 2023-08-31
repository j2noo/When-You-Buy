import { createGlobalStyle } from "styled-components";
import reset from "styled-reset";

const GlobalStyle = createGlobalStyle`
  ${reset}

  body {   
    background-color:#ecf0f1;
    font-family: "DOHYUN";
  }
`;

export default GlobalStyle;
