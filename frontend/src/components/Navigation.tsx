import { NavLink } from "react-router-dom";

/**
 * Global navigation component with React Router integration.
 * Uses NavLink for automatic active state management.
 */
export default function Navigation() {
  const linkClass = ({ isActive }: { isActive: boolean }) =>
    `px-4 py-2 rounded-lg font-medium transition-colors ${
      isActive
        ? "bg-blue-600 text-white shadow-lg"
        : "bg-white dark:bg-gray-800 text-gray-700 dark:text-gray-300 border border-gray-300 dark:border-gray-600 hover:bg-gray-50 dark:hover:bg-gray-700"
    }`;

  return (
    <nav className="fixed top-4 right-4 z-50 flex gap-2" aria-label="Main navigation">
      <NavLink to="/dashboard" className={linkClass}>
        Dashboard
      </NavLink>
      <NavLink to="/cli" className={linkClass}>
        CLI
      </NavLink>
      <NavLink to="/chat" className={linkClass}>
        Chat Demo
      </NavLink>
    </nav>
  );
}
