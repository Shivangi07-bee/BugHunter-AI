import { HashRouter, Routes, Route } from "react-router-dom";

import Dashboard from "./pages/Dashboard";
import Investigation from "./pages/Investigation";
import Sidebar from "./components/Sidebar";

function App() {
    return (
        <HashRouter>
            <div className="app-layout">
                <Sidebar />

                <main className="main-content">
                    <Routes>
                        <Route path="/" element={<Dashboard />} />
                        <Route
                            path="/investigation"
                            element={<Investigation />}
                        />
                    </Routes>
                </main>
            </div>
        </HashRouter>
    );
}

export default App;