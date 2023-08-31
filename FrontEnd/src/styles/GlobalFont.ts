import reset from "styled-reset";
import { createGlobalStyle } from "styled-components";
import DOHYUN from "../assets/BMDOHYEON_ttf.woff";
// const GlobalFont = createGlobalStyle`
//      @font-face {
//         font-family: 'BM_DOHYUN';
//         src: url('../assets/BMDOHYEON_ttf.ttf') format('woff');
//   }

// `;

const GlobalFont = createGlobalStyle`    
     @font-face {
        font-family: "DOHYUN";
        src: local("DOHYUN"), url(${DOHYUN}) format('woff'); 
    }
  
`;

export default GlobalFont;
