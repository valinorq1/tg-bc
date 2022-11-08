import axios from 'axios';
import { React, useState } from "react";

const ProfilePage = () => {


    const [tasksDetail, setTasksDetail] = useState();




    const loadProfileInfo = () => {

        let token = localStorage.getItem('tkn');

        let axiosConfig = {
            headers: {
                "Authorization": `Bearer ${token}`
            }
        };
        axios.get('http://127.0.0.1:8000/api/v1/all-tasks/', axiosConfig)
            .then((result) => {
                //console.log(result['data']);
                const responseData = result.data;

                setTasksDetail(responseData);
                const { sub_task, view_task, comment_task, vote_task, react_task } = tasksDetail;
            })
            .catch(function (error) {

                console.log(error);


            });
    };
    loadProfileInfo();
    return (
        <div className="container">

            <h3>{`taskls: ${sub_task}`}</h3>

        </div>



    )

}

export { ProfilePage };
