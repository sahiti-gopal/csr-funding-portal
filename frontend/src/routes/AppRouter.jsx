import { BrowserRouter, Routes, Route } from "react-router-dom";

import MainLayout from "../layouts/MainLayout";

import Login from "../pages/Login";
import Dashboard from "../pages/Dashboard";
import Projects from "../pages/Projects";
import Alerts from "../pages/Alerts";
import Reports from "../pages/Reports";
import Analytics from "../pages/Analytics";
import Settings from "../pages/Settings";
import Donors from "../pages/Donors";
import DonorDetail from "../pages/DonorDetail";
import ProjectDetails from "../pages/ProjectDetails";
import Chat from "../pages/Chat";
import GenerateReport from "../pages/GenerateReport";
import ReportReview from "../pages/ReportReview";

export default function AppRouter() {
  return (
    <BrowserRouter>
      <Routes>

        <Route path="/login" element={<Login />} />

        <Route element={<MainLayout />}>

          <Route path="/" element={<Dashboard />} />

          <Route path="/projects" element={<Projects />} />
          <Route path="/projects/:id" element={<ProjectDetails />} />

          <Route path="/alerts" element={<Alerts />} />

          <Route path="/donors" element={<Donors />} />
          <Route path="/donors/:id" element={<DonorDetail />} />

          <Route path="/chat" element={<Chat />} />

          <Route path="/reports" element={<Reports />} />
          <Route path="/reports/generate" element={<GenerateReport />} />
          <Route path="/reports/:id" element={<ReportReview />} />

          <Route path="/analytics" element={<Analytics />} />

          <Route path="/settings" element={<Settings />} />
          

        </Route>

      </Routes>
    </BrowserRouter>
  );
}