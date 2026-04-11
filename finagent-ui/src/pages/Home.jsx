import { useState } from "react";
import Container from "../layout/Container";
import InputPanel from "../features/InputPanel";
import DecisionPanel from "../features/DecisionPanel";
import AgentPanel from "../features/AgentPanel";
import ExplainPanel from "../features/ExplainPanel";
import { evaluateUser } from "../services/api";

export default function Home() {
    const [data, setData] = useState(null);
    const [loading, setLoading] = useState(false);

    const handleSubmit = async (form) => {
        setLoading(true);
        try {
            const res = await evaluateUser(form);
            setData(res.data.final_decision);
        } catch (err) {
            console.error(err);
            alert("Backend not running or CORS issue!");
        }
        setLoading(false);
    };

    return (
        <Container>
            <div className="dashboard-grid">
                <InputPanel onSubmit={handleSubmit} loading={loading} />
                <DecisionPanel
                    decision={data?.decision}
                    loading={loading}
                />
            </div>

            <AgentPanel details={data?.details} />
            <ExplainPanel reasons={data?.reasons} decision={data?.decision} />
        </Container>
    );
}