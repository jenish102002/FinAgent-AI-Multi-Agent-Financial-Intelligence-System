import axios from "axios";

const API = axios.create({
    baseURL: import.meta.env.VITE_API_URL || "https://finagent-ai-multi-agent-financial.onrender.com"
});

export const evaluateUser = async (data) => {
    return await API.post("/evaluate", data);
};