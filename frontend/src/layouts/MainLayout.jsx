import { useState } from "react";
import { Outlet } from "react-router-dom";
import { Bot } from "lucide-react";

import Sidebar from "../components/layout/Sidebar";
import Header from "../components/layout/Header";

export default function MainLayout() {
  const [filters, setFilters] = useState({
    region: "all",
    fy: "all",
  });

  const handleFilterChange = (key, value) => {
    setFilters((prev) => ({ ...prev, [key]: value }));
  };

  return (
    <div className="app-shell">
      <Sidebar />

      <div className="app-main">
        <Header
          filters={filters}
          onFilterChange={handleFilterChange}
        />

        <main className="app-content">
          <Outlet context={{ filters }} />
        </main>
      </div>

      <button className="ai-fab" aria-label="AI assistant">
        <Bot size={22} />
      </button>
    </div>
  );
}
