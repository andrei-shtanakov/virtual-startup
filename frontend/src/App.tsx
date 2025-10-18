import React from "react";
import Dashboard from "./pages/Dashboard";
import ChatDemo from "./pages/ChatDemo";
import CLI from "./pages/CLI";
import "./App.css";

type PageType = "dashboard" | "demo" | "cli";

function App() {
  // For now, show Dashboard by default
  // In the future, add proper routing with React Router
  const [currentPage, setCurrentPage] = React.useState<PageType>("dashboard");

  const handleNavigate = (page: string) => {
    if (page === "dashboard" || page === "demo" || page === "cli") {
      setCurrentPage(page as PageType);
    }
  };

  return (
    <div className="App">
      {/* Simple navigation */}
      <div className="fixed top-4 right-4 z-50 flex gap-2">
        <button
          onClick={() => setCurrentPage("dashboard")}
          className={`px-4 py-2 rounded-lg font-medium transition-colors ${
            currentPage === "dashboard"
              ? "bg-blue-600 text-white"
              : "bg-white dark:bg-gray-800 text-gray-700 dark:text-gray-300 border border-gray-300 dark:border-gray-600"
          }`}
        >
          Dashboard
        </button>
        <button
          onClick={() => setCurrentPage("cli")}
          className={`px-4 py-2 rounded-lg font-medium transition-colors ${
            currentPage === "cli"
              ? "bg-blue-600 text-white"
              : "bg-white dark:bg-gray-800 text-gray-700 dark:text-gray-300 border border-gray-300 dark:border-gray-600"
          }`}
        >
          CLI
        </button>
        <button
          onClick={() => setCurrentPage("demo")}
          className={`px-4 py-2 rounded-lg font-medium transition-colors ${
            currentPage === "demo"
              ? "bg-blue-600 text-white"
              : "bg-white dark:bg-gray-800 text-gray-700 dark:text-gray-300 border border-gray-300 dark:border-gray-600"
          }`}
        >
          Chat Demo
        </button>
      </div>

      {/* Page content */}
      {currentPage === "dashboard" && <Dashboard onNavigate={handleNavigate} />}
      {currentPage === "cli" && <CLI />}
      {currentPage === "demo" && <ChatDemo />}
    </div>
  );
}

export default App;
