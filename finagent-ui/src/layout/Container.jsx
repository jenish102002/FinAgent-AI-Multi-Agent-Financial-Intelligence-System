export default function Container({ children }) {
    return (
        <div className="container">
            <header className="header">
                <h1>FinAgent AI Orchestrator</h1>
                <p>Advanced Multi-Agent Financial Intelligence Dashboard</p>
            </header>
            <main>
                {children}
            </main>
        </div>
    );
}