import { BrowserRouter, Routes, Route } from "react-router-dom";

import MainLayout from "../layouts/MainLayout";

import Dashboard from "../pages/Dashboard";
import Projects from "../pages/Projects";
import Alerts from "../pages/Alerts";
import Reports from "../pages/Reports";
import Analytics from "../pages/Analytics";
import Settings from "../pages/Settings";
import Donors from "../pages/Donors";
import ProjectDetails from "../pages/ProjectDetails";

export default function AppRouter() {
  return (
    <BrowserRouter>
      <Routes>

        <Route element={<MainLayout />}>

          <Route path="/" element={<Dashboard />} />

          <Route path="/projects" element={<Projects />} />
          <Route path="/projects/:id" element={<ProjectDetails />} />

          <Route path="/alerts" element={<Alerts />} />

          <Route path="/donors" element={<Donors />} />

          <Route path="/reports" element={<Reports />} />

          <Route path="/analytics" element={<Analytics />} />

          <Route path="/settings" element={<Settings />} />
          

        </Route>

      </Routes>
    </BrowserRouter>
  );
}