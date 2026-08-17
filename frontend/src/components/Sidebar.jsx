import { Link, useLocation } from "react-router-dom";

function Sidebar() {
    const location = useLocation();

    const menu = [
        {
            title: "Dashboard",
            path: "/",
            icon: "◈"
        },
        {
            title: "Investigation",
            path: "/investigation",
            icon: "◎"
        }
    ];

    return (
        <aside className="sidebar">

            {/* BRAND */}
            <div className="sidebar-logo">

                <div className="logo-circle">
                    <img
                       src="./bughunter-logo.png"
                       alt="BugHunter AI"
                    />
                </div>

                <div className="sidebar-brand">
                    <h2>BugHunter AI</h2>
                    <span>Security Reasoning Platform</span>
                </div>

            </div>


            {/* NAVIGATION */}
            <nav className="sidebar-menu">

                {menu.map((item) => {

                    const active =
                        location.pathname === item.path;

                    return (
                        <Link
                            key={item.path}
                            to={item.path}
                            className={
                                active
                                    ? "sidebar-link active"
                                    : "sidebar-link"
                            }
                        >

                            <span className="sidebar-icon">
                                {item.icon}
                            </span>

                            <span className="sidebar-link-text">
                                {item.title}
                            </span>

                        </Link>
                    );
                })}

            </nav>


            {/* FOOTER STATUS */}
            <div className="sidebar-footer">

                <span className="sidebar-status-dot"></span>

                <span>AI Engine Online</span>

            </div>

        </aside>
    );
}

export default Sidebar;