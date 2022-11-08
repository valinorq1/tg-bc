import axios from 'axios';
import 'bootstrap/dist/css/bootstrap.min.css';
import { React, useState } from "react";
import { Route, Routes } from "react-router-dom";

import NaviBar from './components/Navibar';
import { Authentication } from './pages/Auth';
function App() {
    // React States
    const [errorMessages, setErrorMessages] = useState({});
    const [isSubmitted, setIsSubmitted] = useState(false);




    const errors = {
        uname: "invalid username",
        pass: "invalid password"
    };

    const handleSubmit = (event) => {
        //Prevent page reload
        event.preventDefault();
        /* console.log(localStorage.getItem('tkn'));
        return 0; */
        var { uname, pass } = document.forms[0];
        var username = uname.value;
        var password = pass.value;
        //http://127.0.0.1:8000/api/v1/users/
        //http://127.0.0.1:8000/api/v1/token/
        var token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjY2ODE4NzU5LCJpYXQiOjE2NjY4MTgxNTksImp0aSI6IjY5NzcwNzljZmJjNTQwODA5Y2FmNjg3ZDhiMjU5NDFmIiwidXNlcl9pZCI6MX0.WykX_jjx_GyXfh4zsiaPi6ENPoXxUhzPWvZUQeSjM08'
        axios.defaults.headers = {
            Authorization: 'Bearer ' + token
        }
        axios.post('http://127.0.0.1:8000/api/v1/token/', { username, password })
            .catch(function (error) {
                console.log(error);
                console.log(error['response']['status']);
                if (error['response']['status'] == 401) {
                    setErrorMessages({ name: "pass", message: errors.pass });
                }
            })
            .then((result) => {
                console.log(result['status']);
                if (result['status'] == 200) {
                    localStorage.setItem('tkn', result['data']['access']);
                    setIsSubmitted(true);

                }

                //var retrievedObject = localStorage.getItem('testObject');
                console.log(result);
                //console.log('retrievedObject: ', retrievedObject);
                //  console.log(result['data']['access']);
            });


    };

    // Generate JSX code for error message
    const renderErrorMessage = (name) =>
        name === errorMessages.name && (
            <div className="error">{errorMessages.message}</div>
        );

    // JSX code for login form
    const renderForm = (
        <div className="form">
            <form onSubmit={handleSubmit}>
                <div className="input-container">
                    <label>Username </label>
                    <input type="text" name="uname" required />
                    {renderErrorMessage("uname")}
                </div>
                <div className="input-container">
                    <label>Password </label>
                    <input type="password" name="pass" required />
                    {renderErrorMessage("pass")}
                </div>
                <div className="button-container">
                    <input type="submit" />
                </div>
            </form>
        </div>
    );

    return (
        <div className="app">
            <NaviBar />
            <Routes>

                <Route path="/" exact element={<Authentication />} > </Route>

            </Routes>
            <div className="login-form">

                <div className="title">Sign In</div>
                {isSubmitted ? <div>User is successfully logged in</div> : renderForm}
            </div>
        </div>
    );
}

export default App;