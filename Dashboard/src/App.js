import React from "react";
import "./App.css";
import { Footer, Navbar, Sidebar, ThemeSettings } from "./components";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import { FiSave, FiSettings } from "react-icons/fi";
import { TooltipComponent } from "@syncfusion/ej2-react-popups";
import { useStateContext } from "./contexts/ContextProvider";
import MainPage from "./pages/MainPage";

const App = () => {
  const { activeMenu } = useStateContext();

  return (
    <div>
      <MainPage />
    </div>
  );
};

export default App;
