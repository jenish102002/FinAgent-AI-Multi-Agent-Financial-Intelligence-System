export default function DecisionPanel({ decision, reasons, loading }) {
    const map = {
        APPROVAL: { cls: "ok",   note: "All agents cleared" },
        REVIEW:   { cls: "warn", note: "Manual review required" },
        ALERT:    { cls: "bad",  note: "Transaction blocked" },
    };

    const cfg = decision ? map[decision] : null;

    return (
        <div className="card">
            <div className="card-h">
                <span className="card-t">Final Verdict</span>
                <span className="tag tag-blue">Consensus</span>
            </div>

            {loading ? (
                <div className="loading-wrap">
                    <div className="spin" style={{ width: 28, height: 28 }}></div>
                    <div className="loading-t">agents computing...</div>
                </div>
            ) : cfg ? (
                <div className="verdict-wrap">
                    <div className={`verdict-chip ${cfg.cls}`}>{decision}</div>
                    <div className="verdict-note">{cfg.note}</div>

                    {reasons && reasons.length > 0 && (
                        <div style={{ width: "100%", marginTop: 14 }}>
                            {reasons.map((r, i) => (
                                <div key={i} className="sr">
                                    <span className={`ck ${cfg.cls === "ok" ? "ck-ok" : "ck-bad"}`}>
                                        {cfg.cls === "ok" ? "✓" : "!"}
                                    </span>
                                    <span style={{ flex: 1, marginLeft: 8, fontSize: 13, color: "var(--text-2)" }}>{r}</span>
                                </div>
                            ))}
                        </div>
                    )}

                    {reasons && reasons.length === 0 && (
                        <div style={{
                            marginTop: 10, padding: "8px 12px",
                            background: "var(--green-bg)", borderRadius: "var(--radius-sm)",
                            fontSize: 12, color: "var(--green)", fontWeight: 600
                        }}>
                            No risk signals detected
                        </div>
                    )}
                </div>
            ) : (
                <div className="empty">
                    <div className="empty-dot">?</div>
                    Submit a query to run the agents
                </div>
            )}
        </div>
    );
}