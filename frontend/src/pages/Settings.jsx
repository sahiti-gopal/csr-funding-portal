import { useState } from "react";
import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import {
  Tag,
  Users,
  Shield,
  Plus,
  Pencil,
  Trash2,
  GraduationCap,
  Heart,
  Leaf,
  Award,
  Briefcase,
  Target,
  Sprout,
  Baby,
  X,
} from "lucide-react";

import {
  getProjectTypes,
  createProjectType,
  updateProjectType,
  deleteProjectType,
} from "../services/projectTypeService";
import {
  getBeneficiaryCategories,
  createBeneficiaryCategory,
  updateBeneficiaryCategory,
  deleteBeneficiaryCategory,
} from "../services/beneficiaryCategoryService";
import {
  getRoles,
  createRole,
  updateRole,
  deleteRole,
} from "../services/roleService";

import { formatCount } from "../utils/format";

import "../styles/dashboard.css";
import "../styles/settings.css";

const PROJECT_TYPE_ICONS = {
  Education: GraduationCap,
  Healthcare: Heart,
  Environment: Leaf,
  "Women Empowerment": Award,
  Livelihood: Briefcase,
  "Skill Development": Target,
  "Rural Development": Sprout,
};

const BENEFICIARY_ICONS = {
  Students: GraduationCap,
  Farmers: Leaf,
  Women: Award,
  Children: Baby,
  Elderly: Heart,
  Youth: Target,
};

const SWATCHES = [
  { bg: "#dbeafe", fg: "#2563eb" },
  { bg: "#fee2e2", fg: "#dc2626" },
  { bg: "#dcfce7", fg: "#16a34a" },
  { bg: "#fce7f3", fg: "#db2777" },
  { bg: "#fef3c7", fg: "#b45309" },
  { bg: "#ede9fe", fg: "#7c3aed" },
  { bg: "#ccfbf1", fg: "#0d9488" },
];

const swatchFor = (name = "") => {
  let hash = 0;
  for (let i = 0; i < name.length; i++) hash = name.charCodeAt(i) + ((hash << 5) - hash);
  return SWATCHES[Math.abs(hash) % SWATCHES.length];
};

const TABS = [
  { key: "project-types", label: "Project Types", icon: Tag },
  { key: "beneficiary-categories", label: "Beneficiary Categories", icon: Users },
  { key: "user-roles", label: "User Roles", icon: Shield },
];

export default function Settings() {
  const [activeTab, setActiveTab] = useState("project-types");
  const [modal, setModal] = useState(null); // { mode: 'add' | 'edit', item }
  const queryClient = useQueryClient();

  const projectTypesQuery = useQuery({
    queryKey: ["project-types"],
    queryFn: getProjectTypes,
  });

  const categoriesQuery = useQuery({
    queryKey: ["beneficiary-categories"],
    queryFn: getBeneficiaryCategories,
  });

  const rolesQuery = useQuery({
    queryKey: ["roles"],
    queryFn: getRoles,
  });

  const invalidate = (key) => queryClient.invalidateQueries({ queryKey: [key] });

  const projectTypeMutations = {
    create: useMutation({
      mutationFn: createProjectType,
      onSuccess: () => invalidate("project-types"),
    }),
    update: useMutation({
      mutationFn: ({ id, payload }) => updateProjectType(id, payload),
      onSuccess: () => invalidate("project-types"),
    }),
    remove: useMutation({
      mutationFn: deleteProjectType,
      onSuccess: () => invalidate("project-types"),
    }),
  };

  const categoryMutations = {
    create: useMutation({
      mutationFn: createBeneficiaryCategory,
      onSuccess: () => invalidate("beneficiary-categories"),
    }),
    update: useMutation({
      mutationFn: ({ id, payload }) => updateBeneficiaryCategory(id, payload),
      onSuccess: () => invalidate("beneficiary-categories"),
    }),
    remove: useMutation({
      mutationFn: deleteBeneficiaryCategory,
      onSuccess: () => invalidate("beneficiary-categories"),
    }),
  };

  const roleMutations = {
    create: useMutation({
      mutationFn: createRole,
      onSuccess: () => invalidate("roles"),
    }),
    update: useMutation({
      mutationFn: ({ id, payload }) => updateRole(id, payload),
      onSuccess: () => invalidate("roles"),
    }),
    remove: useMutation({
      mutationFn: deleteRole,
      onSuccess: () => invalidate("roles"),
    }),
  };

  const tabConfig = {
    "project-types": {
      title: "Project Types",
      itemLabel: "Type",
      subtitle: "Define categories for CSR projects",
      addLabel: "Add Type",
      query: projectTypesQuery,
      mutations: projectTypeMutations,
      icons: PROJECT_TYPE_ICONS,
      countLabel: (item) => `${item.project_count ?? 0} active project${item.project_count === 1 ? "" : "s"}`,
      layout: "list",
    },
    "beneficiary-categories": {
      title: "Beneficiary Categories",
      itemLabel: "Category",
      subtitle: "Define who the projects serve",
      addLabel: "Add Category",
      query: categoriesQuery,
      mutations: categoryMutations,
      icons: BENEFICIARY_ICONS,
      countLabel: (item) => `${formatCount(item.beneficiaries_total)} individuals`,
      layout: "grid",
    },
    "user-roles": {
      title: "User Roles & Permissions",
      itemLabel: "Role",
      subtitle: "Control access levels",
      addLabel: "Add Role",
      query: rolesQuery,
      mutations: roleMutations,
      icons: {},
      countLabel: (item) => `${item.user_count ?? 0} users`,
      layout: "roles",
    },
  };

  const config = tabConfig[activeTab];
  const items = config.query.data ?? [];

  const handleDelete = (item) => {
    if (!window.confirm(`Delete "${item.name}"? This cannot be undone.`)) return;
    config.mutations.remove.mutate(item.id, {
      onError: (err) => {
        window.alert(err?.response?.data?.message || "Unable to delete this item.");
      },
    });
  };

  const handleSubmit = (payload) => {
    if (modal.mode === "add") {
      config.mutations.create.mutate(payload, { onSuccess: () => setModal(null) });
    } else {
      config.mutations.update.mutate(
        { id: modal.item.id, payload },
        { onSuccess: () => setModal(null) }
      );
    }
  };

  return (
    <div className="dashboard settings-page">
      <div className="dashboard-head">
        <div className="dashboard-title">
          <span className="eyebrow">Settings</span>
          <h4 className="section-heading">Settings</h4>
          <p className="dashboard-subtitle">Configure master data and system settings</p>
        </div>
      </div>

      <div className="settings-layout">
        <div className="settings-sidebar">
          {TABS.map((tab) => {
            const Icon = tab.icon;
            return (
              <button
                key={tab.key}
                className={`settings-nav-item ${activeTab === tab.key ? "active" : ""}`}
                onClick={() => setActiveTab(tab.key)}
              >
                <Icon size={16} />
                {tab.label}
              </button>
            );
          })}
        </div>

        <div className="settings-content">
          <div className="settings-content-head">
            <div>
              <h3>{config.title}</h3>
              <p>{config.subtitle}</p>
            </div>
            <button
              className="settings-add-btn"
              onClick={() => setModal({ mode: "add" })}
            >
              <Plus size={16} />
              {config.addLabel}
            </button>
          </div>

          {config.query.isLoading ? (
            <div className="settings-empty">Loading…</div>
          ) : items.length === 0 ? (
            <div className="settings-empty">No items yet. Add one to get started.</div>
          ) : config.layout === "roles" ? (
            <div className="settings-role-list">
              {items.map((item) => {
                const swatch = swatchFor(item.name);
                return (
                  <div key={item.id} className="settings-role-row">
                    <span
                      className="settings-role-badge"
                      style={{ background: swatch.bg, color: swatch.fg }}
                    >
                      {item.name}
                    </span>
                    <span className="settings-role-desc">{item.description}</span>
                    <span className="settings-role-count">
                      <strong>{item.user_count ?? 0}</strong> users
                    </span>
                    <span className="settings-item-actions">
                      <button onClick={() => setModal({ mode: "edit", item })}>
                        <Pencil size={14} />
                      </button>
                      <button onClick={() => handleDelete(item)}>
                        <Trash2 size={14} />
                      </button>
                    </span>
                  </div>
                );
              })}
            </div>
          ) : (
            <div className={config.layout === "grid" ? "settings-item-grid" : "settings-item-list"}>
              {items.map((item) => {
                const Icon = config.icons[item.name] || Tag;
                const swatch = swatchFor(item.name);
                return (
                  <div key={item.id} className="settings-item-card">
                    <span
                      className="settings-item-icon"
                      style={{ background: swatch.bg, color: swatch.fg }}
                    >
                      <Icon size={18} />
                    </span>
                    <div className="settings-item-text">
                      <div className="settings-item-name">{item.name}</div>
                      <div className="settings-item-meta">{config.countLabel(item)}</div>
                    </div>
                    <span className="settings-item-actions">
                      <button onClick={() => setModal({ mode: "edit", item })}>
                        <Pencil size={14} />
                      </button>
                      <button onClick={() => handleDelete(item)}>
                        <Trash2 size={14} />
                      </button>
                    </span>
                  </div>
                );
              })}
            </div>
          )}
        </div>
      </div>

      {modal && (
        <SettingsFormModal
          mode={modal.mode}
          item={modal.item}
          title={config.itemLabel}
          onClose={() => setModal(null)}
          onSubmit={handleSubmit}
          submitting={config.mutations.create.isPending || config.mutations.update.isPending}
        />
      )}
    </div>
  );
}

function SettingsFormModal({ mode, item, title, onClose, onSubmit, submitting }) {
  const [name, setName] = useState(item?.name ?? "");
  const [description, setDescription] = useState(item?.description ?? "");

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!name.trim()) return;
    onSubmit({ name: name.trim(), description: description.trim() || null });
  };

  return (
    <div className="settings-modal-overlay" onClick={onClose}>
      <div className="settings-modal" onClick={(e) => e.stopPropagation()}>
        <button className="settings-modal-close" onClick={onClose}>
          <X size={16} />
        </button>
        <h3>{mode === "add" ? `Add ${title}` : `Edit ${title}`}</h3>

        <form onSubmit={handleSubmit}>
          <label className="settings-modal-field">
            <span>Name</span>
            <input
              value={name}
              onChange={(e) => setName(e.target.value)}
              placeholder={`e.g. ${title}`}
              autoFocus
              required
            />
          </label>

          <label className="settings-modal-field">
            <span>Description</span>
            <textarea
              value={description}
              onChange={(e) => setDescription(e.target.value)}
              placeholder="Optional description"
              rows={3}
            />
          </label>

          <div className="settings-modal-actions">
            <button type="button" className="settings-modal-cancel" onClick={onClose}>
              Cancel
            </button>
            <button type="submit" className="settings-modal-submit" disabled={submitting}>
              {submitting ? "Saving…" : mode === "add" ? "Add" : "Save changes"}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}
