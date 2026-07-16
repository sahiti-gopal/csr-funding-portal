import {
  getProjectTypes,
  getBeneficiaryCategories,
} from "../../services/projectService";
import { useEffect, useState } from "react";

export default function ProjectForm({ onSubmit, project }) {
  const [projectTypes, setProjectTypes] = useState([]);
  const [beneficiaries, setBeneficiaries] = useState([]);

  const [form, setForm] = useState({
    project_name: "",
    project_type_id: "",
    beneficiary_category_id: "",
    budget: "",
    location: "",
    status: "Planning",
    start_date: "",
    end_date: "",
  });

  useEffect(() => {
    getProjectTypes().then(setProjectTypes);
    getBeneficiaryCategories().then(setBeneficiaries);
  }, []);

  // Populate form when editing
  useEffect(() => {
    if (project) {
      setForm({
        project_name: project.project_name || "",
        project_type_id: project.project_type_id || "",
        beneficiary_category_id:
          project.beneficiary_category_id || "",
        budget: project.budget || "",
        location: project.location || "",
        status: project.status || "Planning",
        start_date: project.start_date || "",
        end_date: project.end_date || "",
      });
    } else {
      setForm({
        project_name: "",
        project_type_id: "",
        beneficiary_category_id: "",
        budget: "",
        location: "",
        status: "Planning",
        start_date: "",
        end_date: "",
      });
    }
  }, [project]);

  const handleChange = (e) => {
    setForm({
      ...form,
      [e.target.name]: e.target.value,
    });
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    onSubmit(form);
  };

  return (
    <form onSubmit={handleSubmit}>

      <input
        name="project_name"
        placeholder="Project Name"
        value={form.project_name}
        onChange={handleChange}
      />

      <select
        name="project_type_id"
        value={form.project_type_id}
        onChange={handleChange}
      >
        <option value="">Select Project Type</option>

        {projectTypes.map((type) => (
          <option key={type.id} value={type.id}>
            {type.name}
          </option>
        ))}
      </select>

      <select
        name="beneficiary_category_id"
        value={form.beneficiary_category_id}
        onChange={handleChange}
      >
        <option value="">Select Beneficiary</option>

        {beneficiaries.map((category) => (
          <option key={category.id} value={category.id}>
            {category.name}
          </option>
        ))}
      </select>

      <input
        type="number"
        name="budget"
        placeholder="Budget"
        value={form.budget}
        onChange={handleChange}
      />

      <input
        name="location"
        placeholder="Location"
        value={form.location}
        onChange={handleChange}
      />

      <select
        name="status"
        value={form.status}
        onChange={handleChange}
      >
        <option>Planning</option>
        <option>Active</option>
        <option>Completed</option>
        <option>Delayed</option>
        <option>On Hold</option>
      </select>

      <input
        type="date"
        name="start_date"
        value={form.start_date}
        onChange={handleChange}
      />

      <input
        type="date"
        name="end_date"
        value={form.end_date}
        onChange={handleChange}
      />

      <button type="submit">
        {project ? "Update Project" : "Save Project"}
      </button>

    </form>
  );
}