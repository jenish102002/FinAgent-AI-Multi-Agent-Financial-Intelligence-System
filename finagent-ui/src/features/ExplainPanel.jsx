export default function ExplainPanel({ reasons, decision }) {
    if (!reasons) return null;

    const ok = decision === "APPROVAL";
    const items = reasons.length > 0
        ? reasons.map(r => ({ text: r, type: ok ? "ok" : "bad" }))
        : [{ text: "No adverse signals detected", type: "ok" }];

    return (
        <div className="card anim-up">
            <div className="card-b">
                {items.map(({ text, type }, i) => (
                    <div key={i} className="tl-item">
                        <div className="tl-left">
                            <div className={`tl-dot ${type}`} />
                            {i < items.length && <div className="tl-line" />}
                        </div>
                        <div className="tl-text">
                            <div className="tl-title" style={{ color: type === "ok" ? "var(--green)" : "var(--red)" }}>
                                {type === "ok" ? "Cleared" : "Risk Signal"}
                            </div>
                            <div className="tl-desc">{text}</div>
                        </div>
                    </div>
                ))}

                <div className="tl-item">
                    <div className="tl-left">
                        <div className={`tl-dot ${ok ? "ok" : decision === "REVIEW" ? "warn" : "bad"}`} />
                    </div>
                    <div className="tl-text">
                        <div className="tl-title" style={{
                            color: ok ? "var(--green)" : decision === "REVIEW" ? "var(--amber)" : "var(--red)"
                        }}>
                            Verdict: {decision}
                        </div>
                        <div className="tl-desc">
                            {ok ? "All checks passed." : decision === "REVIEW" ? "Flagged for human review." : "Transaction blocked."}
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
}