import 'bootstrap/dist/css/bootstrap.min.css';
import { React } from "react";
import { Route, Routes } from "react-router-dom";
import NaviBar from "./components/Navibar";
import { Authentication } from './pages/Auth';
import { HomePage } from './pages/Homepage';
import { ProfilePage } from './pages/Profile';


function App() {
  return (

    <>
      <NaviBar />

      <Routes>

        <Route path="/" element={<HomePage />} />

        <Route path="/login" element={<Authentication />} />
        <Route path="/profile" element={<ProfilePage />} />

      </Routes></>

  )
}

export default App;