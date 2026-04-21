export default function CompliancePanel({ data }) {
    if (!data) return null;

    const s = data.screening || {};
    const rows = [
        { check: "OFAC SDN", result: s.ofac || "Clear", ok: s.ofac === "Clear" || !s.ofac, reg: "Sanctions List" },
        { check: "Fuzzy Match", result: `${s.fuzzy_score ?? 0}%`, ok: (s.fuzzy_score ?? 0) < 80, reg: "Name Similarity" },
        { check: "AML Check", result: s.aml || "Clear", ok: s.aml === "Clear" || !s.aml, reg: "BSA/FinCEN" },
        { check: "FATF Country", result: s.country || "Clear", ok: s.country === "Clear" || !s.country, reg: "Jurisdiction Risk" },
    ];

    const sBadge = data.status === "passed" ? "tag-green" : data.status === "review" ? "tag-amber" : "tag-red";
    const rBadge = data.risk_level === "CRITICAL" || data.risk_level === "HIGH" ? "tag-red" :
                   data.risk_level === "MEDIUM" ? "tag-amber" : "tag-green";

    return (
        <div className="a-card compliance anim-up">
            <div className="a-card-head">
                <span className="a-card-name">Compliance</span>
                <div style={{ display: "flex", gap: 6 }}>
                    <span className={`tag ${rBadge}`}>{data.risk_level}</span>
                    <span className={`tag ${sBadge}`}>{data.status?.toUpperCase()}</span>
                </div>
            </div>

            <table className="dtable">
                <thead>
                    <tr><th>Check</th><th>Result</th><th></th><th>Regulation</th></tr>
                </thead>
                <tbody>
                    {rows.map(({ check, result, ok, reg }) => (
                        <tr key={check}>
                            <td style={{ fontWeight: 600, color: "var(--text)" }}>{check}</td>
                            <td className="mono">{result}</td>
                            <td><span className={`ck ${ok ? "ck-ok" : "ck-bad"}`}>{ok ? "✓" : "✕"}</span></td>
                            <td style={{ color: "var(--text-3)", fontSize: 11 }}>{reg}</td>
                        </tr>
                    ))}
                </tbody>
            </table>

            {data.flags?.length > 0 && (
                <div style={{ marginTop: 10, paddingTop: 10, borderTop: "1px solid var(--border)" }}>
                    <div className="a-box-label">Flags</div>
                    {data.flags.map((f, i) => (
                        <div key={i} className="flag">
                            <span className="ck ck-bad" style={{ flexShrink: 0 }}>!</span>
                            <span>{f}</span>
                        </div>
                    ))}
                </div>
            )}

            {data.analysis && (
                <div className="a-box">
                    <div className="a-box-label">LLM Report</div>
                    <div className={`a-box-text ${data.status === "passed" ? "ok" : "bad"}`}>{data.analysis}</div>
                </div>
            )}
        </div>
    );
}
