import React from "react";
import Header from "src/Components/Header";
import Nav from "src/Components/Nav";
import Main from "src/Components/Main";
import Footer from "src/Components/Footer";
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
