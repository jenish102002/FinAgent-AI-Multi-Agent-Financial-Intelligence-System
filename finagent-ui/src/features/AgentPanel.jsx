function ScoreBar({ score, max = 100 }) {
    const pct = Math.min((score / max) * 100, 100);
    const c = score >= 60 ? "var(--red)" : score >= 30 ? "var(--amber)" : "var(--green)";
    return (
        <div className="sbar">
            <div className="sbar-track">
                <div className="sbar-fill" style={{ width: `${pct}%`, background: c }} />
            </div>
            <span className="sbar-num" style={{ color: c }}>{score}/{max}</span>
        </div>
    );
}

const CFG = {
    fraud: {
        name: "Fraud Detection",
        css: "fraud",
        stats: (d) => [
            { k: "Score", v: <ScoreBar score={d.score ?? 0} /> },
            { k: "Flag", v: d.flag
                ? <span className="mono fw7" style={{ color: "var(--red)" }}>DETECTED</span>
                : <span className="mono fw7" style={{ color: "var(--green)" }}>CLEAR</span>
            },
            ...((d.reasons || []).length ? [{ k: "Triggers", v: (d.reasons || []).join(", ") }] : []),
        ],
        analysis: d => d.analysis,
        aClass: d => d.flag ? "bad" : "ok",
        badge: d => d.flag ? "tag-red" : "tag-green",
        badgeText: d => d.flag ? "FLAGGED" : "CLEAR",
    },
    risk: {
        name: "Credit Risk",
        css: "risk",
        stats: (d) => [
            { k: "Score", v: <ScoreBar score={d.score ?? 0} /> },
            { k: "Eligible", v: d.eligible
                ? <span className="mono fw7" style={{ color: "var(--green)" }}>YES</span>
                : <span className="mono fw7" style={{ color: "var(--red)" }}>NO</span>
            },
            ...((d.reasons || []).length ? [{ k: "Factors", v: (d.reasons || []).join(", ") }] : []),
        ],
        analysis: d => d.analysis,
        aClass: d => d.eligible ? "ok" : "warn",
        badge: d => d.eligible ? "tag-green" : "tag-amber",
        badgeText: d => d.eligible ? "ELIGIBLE" : "DENIED",
    },
    advisory: {
        name: "Advisory",
        css: "advisory",
        stats: (d) => [
            ...(d.market_data?.ticker ? [
                { k: "Ticker", v: <span className="mono fw7">{d.market_data.ticker}</span> },
                { k: "Price", v: <span className="mono fw7" style={{ color: "var(--accent)", fontSize: 16 }}>${d.market_data.price}</span> },
            ] : []),
            ...((d.reasons || []).map((r, i) => ({ k: `Signal ${i+1}`, v: r }))),
        ],
        analysis: d => d.recommendation,
        aClass: () => "",
        badge: () => "tag-blue",
        badgeText: () => "ACTIVE",
    },
};

export default function AgentPanel({ agentKey, data }) {
    const c = CFG[agentKey];
    if (!c || !data) return null;

    const stats = c.stats(data);
    const analysis = c.analysis(data);

    return (
        <div className={`a-card ${c.css} anim-up`}>
            <div className="a-card-head">
                <span className="a-card-name">{c.name}</span>
                <span className={`tag ${c.badge(data)}`}>{c.badgeText(data)}</span>
            </div>

            {stats.map(({ k, v }, i) => (
                <div key={i} className="sr">
                    <span className="sr-k">{k}</span>
                    <span className="sr-v">{typeof v === "string" ? <span style={{ fontFamily: "var(--font)", fontSize: 12, color: "var(--text-2)" }}>{v}</span> : v}</span>
                </div>
            ))}

            {analysis && (
                <div className="a-box">
                    <div className="a-box-label">LLM Analysis</div>
                    <div className={`a-box-text ${c.aClass(data)}`}>{analysis}</div>
                </div>
            )}
        </div>
    );
}