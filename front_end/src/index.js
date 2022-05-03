import React from 'react';
import ReactDOM from 'react-dom/client';
import {Route, BrowserRouter, Routes} from 'react-router-dom';
import './index.css';
import '../node_modules/semantic-ui-css/semantic.min.css'
import LoginPage from "./LoginPage";
import MainView from "./MainView";
import Dashboard from "./Dashboard";


const root = ReactDOM.createRoot( document.getElementById('root') );
root.render(
    <BrowserRouter>
        <Routes>
            <Route exact path="/login" element={<LoginPage/>} />
            <Route exact path="/" element={<MainView/>} />
            <Route exact path="/Dashboard" element={<Dashboard/>} />
        </Routes>
    </BrowserRouter>
);
