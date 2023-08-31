import { createGlobalStyle } from "styled-components";
import reset from "styled-reset";

const GlobalStyle = createGlobalStyle`
  ${reset}
  body { 
    background-color:rgb(30,30,30);
  }
`;
