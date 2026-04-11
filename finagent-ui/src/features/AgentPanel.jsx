export default function AgentPanel({ details }) {
    if (!details) return null;

    return (
        <div className="panel" style={{ marginTop: '2rem' }}>
            <h2 className="panel-title">
                <span style={{ fontSize: '1.5rem' }}>🤖</span> Agent Sub-Modules
            </h2>
            <div className="agents-grid">
                
                {/* Fraud Agent */}
                {details.fraud && (
                    <div className="agent-card">
                        <div className="agent-header">
                            <span className="agent-name">🛡️ Fraud Agent</span>
                            <span className="agent-status-icon">
                                {details.fraud.status === 'not_run' ? '⏸️' : (details.fraud.flag ? '🔴' : '🟢')}
                            </span>
                        </div>
                        {details.fraud.status === 'not_run' ? (
                            <p style={{ color: 'var(--text-secondary)' }}>Skipped by Orchestrator</p>
                        ) : (
                            <>
                                <div className="agent-stat">
                                    <span className="stat-label">Risk Score</span>
                                    <span className="stat-value">{details.fraud.score} / 100</span>
                                </div>
                                <div className="agent-stat">
                                    <span className="stat-label">Flagged</span>
                                    <span className="stat-value" style={{ color: details.fraud.flag ? 'var(--status-alert)' : 'var(--status-approve)'}}>
                                        {details.fraud.flag ? "Yes" : "No"}
                                    </span>
                                </div>
                            </>
                        )}
                    </div>
                )}

                {/* Risk Agent */}
                {details.risk && (
                    <div className="agent-card">
                        <div className="agent-header">
                            <span className="agent-name">📊 Risk Agent</span>
                            <span className="agent-status-icon">
                                {details.risk.status === 'not_run' ? '⏸️' : (details.risk.eligible ? '🟢' : '🔴')}
                            </span>
                        </div>
                        {details.risk.status === 'not_run' ? (
                            <p style={{ color: 'var(--text-secondary)' }}>Skipped by Orchestrator</p>
                        ) : (
                            <>
                                <div className="agent-stat">
                                    <span className="stat-label">Credit Score</span>
                                    <span className="stat-value">{details.risk.score || 'N/A'}</span>
                                </div>
                                <div className="agent-stat">
                                    <span className="stat-label">Eligible</span>
                                    <span className="stat-value" style={{ color: details.risk.eligible ? 'var(--status-approve)' : 'var(--status-alert)'}}>
                                        {details.risk.eligible ? "Yes" : "No"}
                                    </span>
                                </div>
                            </>
                        )}
                    </div>
                )}

                {/* Compliance Agent */}
                {details.compliance && (
                    <div className="agent-card">
                        <div className="agent-header">
                            <span className="agent-name">⚖️ Compliance Agent</span>
                            <span className="agent-status-icon">
                                {details.compliance.status === 'not_run' ? '⏸️' : (details.compliance.status === 'passed' ? '🟢' : '🔴')}
                            </span>
                        </div>
                        {details.compliance.status === 'not_run' ? (
                            <p style={{ color: 'var(--text-secondary)' }}>Skipped by Orchestrator</p>
                        ) : (
                            <div className="agent-stat">
                                <span className="stat-label">Status</span>
                                <span className="stat-value" style={{ 
                                    textTransform: 'capitalize',
                                    color: details.compliance.status === 'passed' ? 'var(--status-approve)' : 'var(--status-alert)'
                                }}>
                                    {details.compliance.status}
                                </span>
                            </div>
                        )}
                    </div>
                )}

                {/* Advisory Agent */}
                {details.advisory && details.advisory.status !== 'not_run' && (
                    <div className="agent-card" style={{ gridColumn: 'span 1' }}>
                        <div className="agent-header">
                            <span className="agent-name">📈 Advisory Agent</span>
                            <span className="agent-status-icon">🟢</span>
                        </div>
                        {details.advisory.market_data && (
                            <div className="agent-stat">
                                <span className="stat-label">{details.advisory.market_data.ticker} Market Price</span>
                                <span className="stat-value">${details.advisory.market_data.price}</span>
                            </div>
                        )}
                    </div>
                )}
                
                {/* Advisory Recommendation (Full Width) */}
                {details.advisory && details.advisory.recommendation && (
                    <div className="advisory-box">
                        <h4>💡 Financial Recommendation</h4>
                        <div className="advisory-text">
                            {details.advisory.recommendation}
                        </div>
                    </div>
                )}

            </div>
        </div>
    );
}