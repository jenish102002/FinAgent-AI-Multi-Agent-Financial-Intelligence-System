import axios from "axios";

const API = axios.create({
    baseURL: "https://finagent-ai-multi-agent-financial.onrender.com",
    timeout: 120000  // 2 min — Render free tier cold starts take ~30-60s
});

export const evaluateUser = async (data) => {
    return await API.post("/evaluate", data);
};