import { useState } from "react";

export default function InputPanel({ onSubmit, loading }) {
    const [form, setForm] = useState({
        user_query: "",
        user_name: "",
        amount: "",
        credit_score: "",
        income: "",
        debt: "",
        country: "",
        usual_location: ""
    });

    const handleChange = (e, key) => {
        setForm({ ...form, [key]: e.target.value });
    };

    const submitHandler = () => {
        const cleanedForm = {};
        for (const [key, value] of Object.entries(form)) {
            if (value !== "") {
                if (["credit_score", "income", "debt", "amount"].includes(key)) {
                    cleanedForm[key] = Number(value);
                } else {
                    cleanedForm[key] = value;
                }
            }
        }
        onSubmit(cleanedForm);
    };

    return (
        <div className="panel">
            <h2 className="panel-title">
                <span style={{ fontSize: '1.5rem' }}>💬</span> User Request
            </h2>

            <div className="form-group">
                <label className="form-label">Natural Language Query *</label>
                <textarea
                    placeholder="E.g., I want to apply for a $50,000 personal loan..."
                    className="form-input"
                    value={form.user_query}
                    onChange={(e) => handleChange(e, "user_query")}
                />
            </div>

            <div className="form-group">
                <label className="form-label">Known User Information (Optional)</label>
                <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '1rem' }}>
                    <input
                        placeholder="User Name"
                        className="form-input"
                        value={form.user_name}
                        onChange={(e) => handleChange(e, "user_name")}
                    />
                    <input
                        placeholder="ISO Country (e.g., US, KP)"
                        className="form-input"
                        value={form.country}
                        onChange={(e) => handleChange(e, "country")}
                    />
                    <input
                        type="number"
                        placeholder="Credit Score"
                        className="form-input"
                        value={form.credit_score}
                        onChange={(e) => handleChange(e, "credit_score")}
                    />
                    <input
                        type="number"
                        placeholder="Annual Income ($)"
                        className="form-input"
                        value={form.income}
                        onChange={(e) => handleChange(e, "income")}
                    />
                    <input
                        type="number"
                        placeholder="Existing Debt ($)"
                        className="form-input"
                        value={form.debt}
                        onChange={(e) => handleChange(e, "debt")}
                    />
                    <input
                        placeholder="Usual Location (City)"
                        className="form-input"
                        value={form.usual_location}
                        onChange={(e) => handleChange(e, "usual_location")}
                    />
                </div>
            </div>

            <button
                onClick={submitHandler}
                className="btn-primary"
                disabled={loading || !form.user_query}
            >
                {loading ? "Orchestrating Agents..." : "Run Evaluation"}
            </button>
        </div>
    );
}