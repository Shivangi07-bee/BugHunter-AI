import { useState } from "react";
import { useNavigate } from "react-router-dom";
import api from "../api/api";

function RepositoryUploader() {
    const [repository, setRepository] = useState("");
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState("");

    const navigate = useNavigate();

    async function analyzeRepository() {
        const value = repository.trim();

        if (!value) {
            setError("Enter a repository path before starting analysis.");
            return;
        }

        try {
            setLoading(true);
            setError("");

            const response = await api.post("/analyze", {
                repository: value
            });

            localStorage.setItem(
                "investigation",
                JSON.stringify(response.data)
            );

            navigate("/investigation");

        } catch (err) {
            console.error("Repository analysis failed:", err);

            setError(
                err?.response?.data?.detail ||
                "Repository analysis failed. Check the repository path and backend."
            );
        } finally {
            setLoading(false);
        }
    }

    function handleKeyDown(event) {
        if (event.key === "Enter" && !loading) {
            analyzeRepository();
        }
    }

    return (
        <div className="repository-form">

            <label htmlFor="repository-path">
                Repository Path
            </label>

            <div className="repository-input-row">

                <input
                    id="repository-path"
                    type="text"
                    value={repository}
                    onChange={(e) => {
                        setRepository(e.target.value);
                        setError("");
                    }}
                    onKeyDown={handleKeyDown}
                    disabled={loading}
                    placeholder="e.g. D:\bughunter-ai\sample_projects\shopping_app"
                />

                <button
                    type="button"
                    onClick={analyzeRepository}
                    disabled={loading || !repository.trim()}
                >
                    {loading
                        ? "Analyzing..."
                        : "Analyze Repository"}
                </button>

            </div>

            <div className="repository-help">
                <span>●</span>
                <span>
                    Local source repository used to build the application model.
                </span>
            </div>

            {error && (
                <div className="repository-error">
                    {error}
                </div>
            )}

        </div>
    );
}

export default RepositoryUploader;