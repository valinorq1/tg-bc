import { React, useState } from "react";
import { useNavigate } from "react-router-dom";
import API from '../utils/API';

const Authentication = () => {
    const navigate = useNavigate();
    const [isSubmitted, setIsSubmitted] = useState(false);

    const [isActive, setActive] = useState(false);


    /* useEffect(() => {
        let token = localStorage.getItem('tkn')

        API.post(`token/verify/`, { token }).then((response) => {
            navigate("/profile");

        }).catch(function (error) {
            console.log("ERROR")
            console.log(error);
        });
    }, []); */



    const handleLoginSubmit = (event) => {
        event.preventDefault();
        var { uname, pass } = document.forms[1];

        var email = uname.value;
        var password = pass.value;



        API.post('token/', { email, password })
            .then((result) => {
                console.log(result);
                if (result['status'] == 200) {
                    localStorage.setItem('tkn', result['data']['access']);
                    console.log(result['data']['access']);
                    setIsSubmitted(true);
                    navigate("/profile");

                }
            })
            .catch(function (error) {
                console.log(error);
                console.log(error['response']['status']);
                if (error['response']['status'] == 401) {
                    console.log("не авторизованы");
                    setActive(isActive = false);
                }

            });



    };
    return (
        <div class="login-container">

            <div className="row form justify-content-center align-items-center">

                <form onSubmit={handleLoginSubmit} className="mb-5 mt-3 col" id="login_form">
                    <div className="mb-4">
                        <label for="username" className="form-label">Логин</label>
                        <input type="email" className={isActive ? "form-control is-invalid" : "form-control"} name="uname" />
                        <div id="validationServerUsernameFeedback" className="invalid-feedback">
                            Логин или пароль не совпадают
                        </div>


                    </div>
                    <div className="mb-4">
                        <label for="password" className="form-label is-invalid ">Пароль</label>
                        <input type="password" name="pass" className="form-control" />

                    </div>

                    <div className="row">
                        <div className="text-center">
                            <input type="submit" className="btn btn-primary main-bg col-4 mb-4" value="Войти" />

                        </div>

                    </div>
                </form>



            </div>

        </div>



    )

}

export { Authentication };
