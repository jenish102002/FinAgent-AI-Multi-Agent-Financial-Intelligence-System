import axios from "axios";

const API = axios.create({
    baseURL: "http://127.0.0.1:8000"
});

export const evaluateUser = async (data) => {
    return await API.post("/evaluate", data);
};