import { useState } from "react";
import { useParams } from "react-router-dom";
import { useQuery } from "@tanstack/react-query";

import { getProject } from "../services/projectService";

import ProjectHeader from "../components/project/ProjectHeader";
import BeneficiaryCard from "../components/project/BeneficiaryCard";
import ProjectOwnerCard from "../components/project/ProjectOwnerCard";
import SponsorCard from "../components/project/SponsorCard";
import DocumentsCard from "../components/project/DocumentsCard";
import Gallery from "../components/project/Gallery";

import "../styles/projectDetails.css";

const TAG_COLORS = {
  Lead: "#1e293b",
  Ops: "#2563eb",
  Training: "#7c3aed",
  Partner: "#0d9488",
};

const initials = (name = "") =>
  name
    .split(" ")
    .filter(Boolean)
    .slice(0, 2)
    .map((word) => word[0])
    .join("")
    .toUpperCase();
const TEAM_IMAGES = {
  "Priya Sharma": "/images/team/priya.png",
  "Rohan Mehta": "/images/team/rohan.png",
  "Anita Desai": "/images/team/anita.png",
  "Vikram Rao": "/images/team/vikram.png",
};

const decorateTeam = (team = []) =>
  team.map((member) => ({
    ...member,
    initials: initials(member.name),
    color: TAG_COLORS[member.tag] ?? "#64748b",
    image: TEAM_IMAGES[member.name] || "/images/team/default-avatar.png",
  }));  
const formatMetrics = (metrics = []) =>
  metrics.map((metric) => ({
    ...metric,
    value: Number(metric.value).toLocaleString(),
    target: Number(metric.target).toLocaleString(),
  }));

export default function ProjectDetails() {
  const { id } = useParams();
  const [activeTab, setActiveTab] = useState("overview");

  const {
    data: project,
    isLoading,
    isError,
  } = useQuery({
    queryKey: ["project", id],
    queryFn: () => getProject(id),
    enabled: Boolean(id),
  });

  if (isLoading) {
    return (
      <div className="project-details pd-state">
        Loading project...
      </div>
    );
  }

  if (isError || !project) {
    return (
      <div className="project-details pd-state">
        Could not load this project.
      </div>
    );
  }

  return (
    <div className="project-details">
      <ProjectHeader
        name={project.project_name}
        activeTab={activeTab}
        onTabChange={setActiveTab}
      />

      {activeTab === "overview" ? (
        <>
          {/* Beneficiaries */}
          <section className="card pd-section">

            <BeneficiaryCard
              metrics={formatMetrics(project.beneficiaries)}
              locations={project.locations}
            />

          </section>

          {/* Bottom Three Cards */}
          <section className="pd-info-grid">

            {/* Sponsor */}
            <SponsorCard sponsor={project.sponsor} />

            {/* Project Owner */}
            <ProjectOwnerCard
    members={decorateTeam(project.team)}
/>

            {/* Recent Files */}
            <DocumentsCard
              documents={project.documents}
            />

          </section>
        </>
      ) : (
        <Gallery images={project.gallery ?? []} />
      )}
    </div>
  );
}