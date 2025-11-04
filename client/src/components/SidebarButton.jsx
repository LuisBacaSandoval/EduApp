import { Link } from "react-router-dom";

export default function SidebarButton({ icon: Icon, children, to, isCollapsed }) {
    return (
        <Link
            to={to || "#"}
            className="sidebar-button group relative"
        >
            <Icon className="w-5 h-5 shrink-0" />
            <span className={`sidebar-button-text transition-all duration-300 ${isCollapsed ? 'opacity-0 w-0 overflow-hidden' : 'opacity-100'}`}>
                {children}
            </span>
            {isCollapsed && (
                <div className="absolute left-full ml-2 px-2 py-1 bg-gray-800 text-white text-sm rounded opacity-0 group-hover:opacity-100 transition-opacity whitespace-nowrap pointer-events-none z-10">
                    {children}
                </div>
            )}
        </Link>
    );
}