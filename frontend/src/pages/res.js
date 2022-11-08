import axios from 'axios';
import { React, useState } from "react";

const Authentication = () => {





    const [isSubmitted, setIsSubmitted] = useState(false);

    const [isActive, setActive] = useState(false);






    const handleLoginSubmit = (event) => {
        //Prevent page reload
        event.preventDefault();
        /* console.log(localStorage.getItem('tkn'));
        return 0; */
        var { uname, pass } = document.forms[1];

        var username = uname.value;
        var password = pass.value;
        //http://127.0.0.1:8000/api/v1/users/
        //http://127.0.0.1:8000/api/v1/token/


        axios.post('http://127.0.0.1:8000/api/v1/token/', { username, password })
            .then((result) => {
                console.log(result['status']);
                if (result['status'] == 200) {
                    localStorage.setItem('tkn', result['data']['access']);
                    setIsSubmitted(true);
                }


                //var retrievedObject = localStorage.getItem('testObject');

                //console.log('retrievedObject: ', retrievedObject);
                //  console.log(result['data']['access']);
            })
            .catch(function (error) {

                console.log(error['response']['status']);
                if (error['response']['status'] == 401) {
                    console.log("не авторизованы");
                    setActive(!isActive);
                }

            });



    };



    return (
        <div class="container">

            <div className="d-flex justify-content-around form " id="login_form">

                <form onSubmit={handleLoginSubmit}>
                    <div class="mb-4">
                        <label for="username" class="form-label">Логин</label>
                        <input type="text" className={isActive ? "form-control is-invalid" : "form-control"} name="uname" />
                        <div id="validationServerUsernameFeedback" className="invalid-feedback">
                            Логин или пароль не совпадают
                        </div>


                    </div>
                    <div class="mb-4">
                        <label for="password" className="form-label is-invalid ">Пароль</label>
                        <input type="password" name="pass" class="form-control" />

                    </div>

                    <div class="row">
                        <div className="text-center">
                            <input type="submit" class="btn btn-primary main-bg col-4" value="Войти" />

                        </div>

                    </div>
                </form>

            </div>


        </div>



    )

}

export { Authentication };
