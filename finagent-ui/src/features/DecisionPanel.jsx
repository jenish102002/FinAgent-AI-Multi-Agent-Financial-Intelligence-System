export default function DecisionPanel({ decision, loading }) {
    return (
        <div className="panel decision-panel">
            <h2 className="panel-title" style={{ alignSelf: 'flex-start', margin: '0 0 auto 0' }}>
                <span style={{ fontSize: '1.5rem' }}>🎯</span> Final Verdict
            </h2>
            
            <div style={{ margin: 'auto', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
                {loading ? (
                    <div className="loader">
                        <div className="spinner"></div>
                        <p style={{ color: 'var(--text-secondary)' }}>Agents are thinking...</p>
                    </div>
                ) : decision ? (
                    <div className="decision-result">
                        <div className={`decision-badge status-${decision}`}>
                            {decision}
                        </div>
                        <p style={{ color: 'var(--text-secondary)' }}>
                            Computed by Multi-Agent Consensus
                        </p>
                    </div>
                ) : (
                    <p style={{ color: 'var(--text-secondary)', opacity: 0.5 }}>
                        Enter a query to see the AI orchestrator in action
                    </p>
                )}
            </div>
        </div>
    );
}