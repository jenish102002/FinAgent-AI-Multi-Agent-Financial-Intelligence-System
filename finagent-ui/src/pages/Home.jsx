import { useState } from "react";
import InputPanel from "../features/InputPanel";
import DecisionPanel from "../features/DecisionPanel";
import AgentPanel from "../features/AgentPanel";
import CompliancePanel from "../features/CompliancePanel";
import ExplainPanel from "../features/ExplainPanel";
import { evaluateUser } from "../services/api";

export default function Home() {
    const [result, setResult] = useState(null);
    const [loading, setLoading] = useState(false);
    const [intent, setIntent] = useState(null);
    const [error, setError] = useState(null);

    const handleSubmit = async (form) => {
        setLoading(true);
        setResult(null);
        setError(null);
        setIntent(null);
        try {
            const res = await evaluateUser(form);
            setResult(res.data);
            setIntent(res.data.intent);
        } catch (err) {
            console.error(err);
            setError(err?.response?.data?.detail || "Backend unreachable — is it running on port 8000?");
        }
        setLoading(false);
    };

    const decision = result?.final_decision;
    const details = decision?.details;

    const ran = (k) => {
        const d = details?.[k];
        if (!d) return false;
        if (d.status === "not_run") return false;
        if (k === "advisory" && d.recommendation) return true;
        return d.score !== undefined || d.eligible !== undefined || d.status;
    };

    return (
        <>
            {/* Nav */}
            <nav className="topnav">
                <div className="topnav-left">
                    <div className="topnav-logo">F</div>
                    <span className="topnav-brand">FinAgent</span>
                    <span className="topnav-sep">/</span>
                    <span className="topnav-page">Intelligence Console</span>
                </div>
                <div className="topnav-right">
                    {intent && <span className="tag tag-blue">{intent}</span>}
                    {decision?.decision && (
                        <span className={`tag ${
                            decision.decision === "APPROVAL" ? "tag-green" :
                            decision.decision === "REVIEW" ? "tag-amber" : "tag-red"
                        }`}>
                            {decision.decision}
                        </span>
                    )}
                </div>
            </nav>

            <div className="page">
                {/* Row 1: Input + Verdict */}
                <div className="g-main">
                    <InputPanel onSubmit={handleSubmit} loading={loading} error={error} />
                    <DecisionPanel
                        decision={decision?.decision}
                        reasons={decision?.reasons}
                        loading={loading}
                    />
                </div>

                {/* Row 2: Agent cards */}
                {details && (
                    <>
                        <div className="sec-label">Agent Results</div>
                        <div className="g-agents">
                            {ran("fraud") && <AgentPanel agentKey="fraud" data={details.fraud} />}
                            {ran("risk") && <AgentPanel agentKey="risk" data={details.risk} />}
                            {ran("compliance") && <CompliancePanel data={details.compliance} />}
                            {ran("advisory") && <AgentPanel agentKey="advisory" data={details.advisory} />}
                        </div>
                    </>
                )}

                {/* Row 3: Audit trail */}
                {decision && (
                    <>
                        <div className="sec-label">Audit Trail</div>
                        <ExplainPanel reasons={decision.reasons} decision={decision.decision} />
                    </>
                )}
            </div>
        </>
    );
}