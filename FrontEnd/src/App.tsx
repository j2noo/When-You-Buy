import React from "react";
import Header from "./Components/Header";
import Nav from "./Components/Nav";
import Main from "./Components/Main";
import Footer from "./Components/Footer";
const add = (a: number, b: number): number => a + b;
const App = () => {
  return (
    <>
      <Header></Header>
      <Nav></Nav>
      <Main></Main>
      <Footer></Footer>
    </>
  );
};

export default App;
