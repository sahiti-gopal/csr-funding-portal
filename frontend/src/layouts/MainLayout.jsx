import { Outlet } from "react-router-dom";
import { Bot } from "lucide-react";

import Sidebar from "../components/layout/Sidebar";
import Header from "../components/layout/Header";

export default function MainLayout() {
  return (
    <div className="app-shell">
      <Sidebar />

      <div className="app-main">
        <Header />

        <main className="app-content">
          <Outlet />
        </main>
      </div>

      <button className="ai-fab" aria-label="AI assistant">
        <Bot size={22} />
      </button>
    </div>
  );
}
