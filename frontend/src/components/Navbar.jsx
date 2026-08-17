import {
    downloadJson,
    downloadHtml,
    downloadPdf
} from "../api/api";

function Navbar() {
    const now = new Date();

    const time = now.toLocaleTimeString([], {
        hour: "2-digit",
        minute: "2-digit"
    });

    return (
        <header className="navbar">

            <div className="navbar-brand">
                <div className="navbar-brand-title">
                    BugHunter AI
                </div>

                <div className="navbar-brand-subtitle">
                    AI Security Reasoning Platform
                </div>
            </div>

            <div className="navbar-actions">

                <div className="status-chip status-ready">
                    <span className="status-dot"></span>
                    Investigation Ready
                </div>

                <div className="status-chip status-loaded">
                    <span className="status-dot"></span>
                    Repository Loaded
                </div>

                <div className="navbar-downloads">

                    <button
                        className="navbar-download"
                        onClick={downloadJson}
                    >
                        <span>JSON</span>
                    </button>

                    <button
                        className="navbar-download"
                        onClick={downloadHtml}
                    >
                        <span>HTML</span>
                    </button>

                    <button
                        className="navbar-download"
                        onClick={downloadPdf}
                    >
                        <span>PDF</span>
                    </button>

                </div>

                <div className="navbar-clock">
                    <span className="clock-label">LOCAL TIME</span>
                    <span className="clock-value">{time}</span>
                </div>

            </div>

        </header>
    );
}

export default Navbar;