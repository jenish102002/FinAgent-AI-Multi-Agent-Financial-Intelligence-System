import { useState } from "react";

const SECTIONS = [
    {
        key: "query",
        label: "Query",
        fields: [
            { key: "user_query", label: "Natural Language Query", type: "textarea", required: true,
              placeholder: "I want to apply for a $50,000 personal loan..." },
            { key: "user_name", label: "Full Name", type: "text", placeholder: "John Doe" },
        ]
    },
    {
        key: "fin",
        label: "Financial Profile",
        cols: 4,
        fields: [
            { key: "credit_score", label: "Credit Score",  type: "number", placeholder: "720" },
            { key: "income",       label: "Income ($)",     type: "number", placeholder: "90000" },
            { key: "debt",         label: "Debt ($)",       type: "number", placeholder: "15000" },
            { key: "risk_profile", label: "Risk Profile",   type: "text",   placeholder: "moderate" },
        ]
    },
    {
        key: "txn",
        label: "Transaction",
        cols: 4,
        fields: [
            { key: "amount",          label: "Amount ($)",   type: "number", placeholder: "50000" },
            { key: "avg_amount",      label: "Avg Amt ($)",  type: "number", placeholder: "2000" },
            { key: "frequency",       label: "Freq (/hr)",   type: "number", placeholder: "3" },
            { key: "usual_frequency", label: "Usual (/hr)",  type: "number", placeholder: "1" },
        ]
    },
    {
        key: "loc",
        label: "Location & Market",
        cols: 4,
        fields: [
            { key: "location",       label: "Location",       type: "text", placeholder: "Mumbai" },
            { key: "usual_location", label: "Usual Location",  type: "text", placeholder: "New York" },
            { key: "country",        label: "Country (ISO)",   type: "text", placeholder: "US" },
            { key: "market_ticker",  label: "Ticker",          type: "text", placeholder: "NVDA" },
        ]
    },
];

const NUMS = new Set(["credit_score","income","debt","amount","avg_amount","frequency","usual_frequency"]);

export default function InputPanel({ onSubmit, loading, error }) {
    const [form, setForm] = useState(
        Object.fromEntries(SECTIONS.flatMap(s => s.fields).map(f => [f.key, ""]))
    );

    const set = (k, v) => setForm(f => ({ ...f, [k]: v }));

    const submit = () => {
        const out = {};
        for (const [k, v] of Object.entries(form)) {
            if (v !== "") out[k] = NUMS.has(k) ? Number(v) : v;
        }
        onSubmit(out);
    };

    return (
        <div className="card">
            <div className="card-h">
                <span className="card-t">Query Console</span>
                <span className="tag tag-blue">POST /evaluate</span>
            </div>
            <div className="card-b">
                {error && <div className="err">{error}</div>}

                {SECTIONS.map(({ key, label, fields, cols }) => (
                    <div key={key} className="form-sec">
                        <div className="form-lbl">{label}</div>
                        <div className={`fg ${cols === 4 ? "g-4" : cols === 2 ? "g-2" : ""}`}>
                            {fields.map(({ key: fk, label: fl, type, placeholder, required }) =>
                                type === "textarea" ? (
                                    <div key={fk} className="col-span-full">
                                        <div className="field-l">{fl}{required ? " *" : ""}</div>
                                        <textarea
                                            className="field-i"
                                            placeholder={placeholder}
                                            value={form[fk]}
                                            onChange={e => set(fk, e.target.value)}
                                            rows={2}
                                        />
                                    </div>
                                ) : (
                                    <div key={fk}>
                                        <div className="field-l">{fl}</div>
                                        <input
                                            type={type}
                                            className="field-i"
                                            placeholder={placeholder}
                                            value={form[fk]}
                                            onChange={e => set(fk, e.target.value)}
                                        />
                                    </div>
                                )
                            )}
                        </div>
                    </div>
                ))}
            </div>
            <div className="card-f">
                <button className="btn" onClick={submit} disabled={loading || !form.user_query.trim()}>
                    {loading ? <><span className="spin"></span> Processing...</> : "Run Analysis"}
                </button>
            </div>
        </div>
    );
}