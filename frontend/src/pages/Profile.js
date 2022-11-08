import { React, useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import API from '../utils/API';


const ProfilePage = () => {
    const navigate = useNavigate();
    const [tasksDetail, setTasksDetail] = useState();

    let total_task = 0;
    useEffect(() => {


        API.get(`all-tasks/`).then((response) => {
            const responseTasks = response.data;

            for (var key in responseTasks) {
                total_task += responseTasks[key].length;
                console.log(key, responseTasks[key].length);

            }

            setTasksDetail(responseTasks);
            console.log("TOTAL ", total_task);
        }).catch(function (error) {
            console.log(error);
            navigate("/login");
        });
    }, []);
    //const { sub_task, view_task, comment_task, vote_task, react_task } = tasksDetail;
    //console.log(tasksDetail);

    return (
        <>
            {tasksDetail ? (
                <><div className="container"><div> Заданий: {total_task}</div></div></>
            ) : (
                <h3>Null</h3>
            )}
        </>

    );

}

export { ProfilePage };
