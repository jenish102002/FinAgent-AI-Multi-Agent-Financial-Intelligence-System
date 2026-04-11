export default function ExplainPanel({ reasons, decision }) {
    if (!reasons) return null;

    const isPositive = decision === 'APPROVAL';

    return (
        <div className="panel explain-panel">
            <h2 className="panel-title">
                <span style={{ fontSize: '1.5rem' }}>🔍</span> Explainability & Audit Trail
            </h2>

            <ul className="reasons-list">
                {reasons.length === 0 ? (
                    <li className="reason-item positive">
                        Clean profile: No risk signals detected
                    </li>
                ) : (
                    reasons.map((r, i) => (
                        <li key={i} className={`reason-item ${isPositive ? 'positive' : ''}`}>
                            {r}
                        </li>
                    ))
                )}
            </ul>
        </div>
    );
}