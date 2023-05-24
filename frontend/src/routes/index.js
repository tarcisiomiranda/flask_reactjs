import { Fragment } from "react";
import { BrowserRouter, Route, Routes } from "react-router-dom";
import Home from "../pages/Home";
import Escolha from "../pages/Escolha";

const Private = ({ Item }) => {
    const signed = true;

    return signed > 0 ? <Item /> : <Home />;
  };

const RoutesApp = () => {
    return (
        <BrowserRouter>
        <Fragment>
            <Routes>
                <Route exact path="/home" element={<Private Item={Home} />} />
                <Route path="/" element={<Home />} />
                <Route exact path="/escolha" element={<Escolha />} />
                <Route path="*" element={<Home />} />
            </Routes>
        </Fragment>
        </BrowserRouter>
    )
}

export default RoutesApp;
