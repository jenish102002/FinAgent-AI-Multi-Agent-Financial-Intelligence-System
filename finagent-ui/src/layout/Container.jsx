export default function Sidebar({ activeAgent, onAgentSelect, result }) {
    const agents = [
        { key: "fraud",      icon: "🛡️", label: "Fraud Engine" },
        { key: "risk",       icon: "📊", label: "Credit Risk" },
        { key: "compliance", icon: "⚖️", label: "Compliance" },
        { key: "advisory",   icon: "📈", label: "Advisory" },
    ];

    const getAgentStatus = (key) => {
        if (!result?.final_decision?.details) return null;
        return result.final_decision.details[key];
    };

    const getAgentRun = (key) => {
        const d = getAgentStatus(key);
        if (!d) return false;
        return d.status !== "not_run" || d.score !== undefined || d.recommendation !== undefined;
    };

    return (
        <aside className="sidebar">
            <div className="sidebar-logo">
                <div className="sidebar-logo-mark">
                    <div className="logo-icon">🧠</div>
                    <div>
                        <div className="logo-text">FinAgent</div>
                        <div className="logo-sub">AI Orchestrator</div>
                    </div>
                </div>
            </div>

            <nav className="sidebar-nav">
                <div className="nav-section-label">Workspace</div>
                <button className="nav-item active">
                    <span className="nav-item-icon">⚡</span>
                    Intelligence Console
                </button>

                {result && (
                    <>
                        <div className="nav-section-label" style={{ marginTop: 16 }}>Agents Executed</div>
                        {agents.map(a => (
                            getAgentRun(a.key) && (
                                <button
                                    key={a.key}
                                    className={`nav-item ${activeAgent === a.key ? "active" : ""}`}
                                    onClick={() => onAgentSelect(a.key)}
                                >
                                    <span className="nav-item-icon">{a.icon}</span>
                                    {a.label}
                                </button>
                            )
                        ))}
                    </>
                )}

                <div className="nav-section-label" style={{ marginTop: 16 }}>System</div>
                <a className="nav-item" href="http://127.0.0.1:8000/docs" target="_blank" rel="noreferrer">
                    <span className="nav-item-icon">📡</span>
                    API Docs
                </a>
            </nav>

            <div className="sidebar-footer">
                <div className="status-dot">
                    <span className="dot"></span>
                    Backend Connected
                </div>
            </div>
        </aside>
    );
}