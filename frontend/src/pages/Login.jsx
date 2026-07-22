import { useState } from "react";
import { useNavigate } from "react-router-dom";
import {
  Mail,
  Lock,
  Eye,
  EyeOff,
  HeartHandshake,
  FolderKanban,
  ShieldCheck,
  BarChart3,
} from "lucide-react";

import { login } from "../services/authService";

import "../styles/login.css";

const FEATURES = [
  { icon: HeartHandshake, label: "Track Donations & Utilisation" },
  { icon: FolderKanban, label: "Manage Projects & Performance" },
  { icon: ShieldCheck, label: "Ensure Compliance & Transparency" },
  { icon: BarChart3, label: "Measure & Maximize Impact" },
];

const EMAIL_REGEX = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

/**
 * Complete, self-contained login screen (hero panel + form).
 * Owns its own field state, validation, loading state and login logic.
 */
export default function Login() {
  const navigate = useNavigate();
  const [formData, setFormData] = useState({
    email: "",
    password: "",
    rememberMe: false,
  });
  const [fieldErrors, setFieldErrors] = useState({});
  const [showPassword, setShowPassword] = useState(false);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");

  const handleChange = (event) => {
    const { name, value, type, checked } = event.target;
    setFormData((prev) => ({
      ...prev,
      [name]: type === "checkbox" ? checked : value,
    }));

    // Clear the field-level error as soon as the user starts fixing it
    if (fieldErrors[name]) {
      setFieldErrors((prev) => ({ ...prev, [name]: "" }));
    }
  };

  const validate = () => {
    const errors = {};

    if (!formData.email.trim()) {
      errors.email = "Email is required";
    } else if (!EMAIL_REGEX.test(formData.email.trim())) {
      errors.email = "Enter a valid email address";
    }

    if (!formData.password) {
      errors.password = "Password is required";
    }

    setFieldErrors(errors);
    return Object.keys(errors).length === 0;
  };

  const handleLogin = async ({ email, password, rememberMe }) => {
    setError("");
    setSuccess("");
    setLoading(true);

    try {
      await login(email, password);

      if (rememberMe) {
        localStorage.setItem("seva-user-email", email);
      } else {
        localStorage.removeItem("seva-user-email");
      }
      setSuccess("Login successful");
      navigate("/");
    } catch (err) {
      if (err.response) {
        setError(err.response.data?.message || "Unable to sign in. Please try again.");
      } else {
        setError("Unable to reach the login service. Please try again later.");
      }
    } finally {
      setLoading(false);
    }
  };

  const handleSubmit = (event) => {
    event.preventDefault();

    if (loading) return;
    if (!validate()) return;

    handleLogin({
      email: formData.email.trim(),
      password: formData.password,
      rememberMe: formData.rememberMe,
    });
  };

  return (
    <div className="login-shell">
      <aside className="hero-panel">
        <img src="/images/login-hero.jpg" alt="" className="hero-photo" />
        <div className="hero-overlay" />

        <div className="hero-panel-content">
          <div className="hero-brand">
            <div className="hero-logo">
              <img src="/images/logo.png" alt="" />
            </div>
            <div>
              <div className="hero-brand-name">Seva Impact</div>
              <div className="hero-brand-tag">Measure. Manage. Maximize Impact.</div>
            </div>
          </div>

          <div className="hero-copy">
            <h2>
              Empowering Change.
              <br />
              <span>Creating Lasting Impact.</span>
            </h2>
            <p>
              A unified platform to manage CSR partnerships, track projects,
              ensure compliance and measure social impact that matters.
            </p>
          </div>

          <div className="hero-features">
            {FEATURES.map(({ icon: Icon, label }) => (
              <div key={label} className="hero-feature">
                <Icon size={14} className="hero-feature-icon" />
                {label}
              </div>
            ))}
          </div>

          <p className="hero-footnote">
            Together with our partners, we build a better tomorrow for
            communities and the planet.
          </p>
        </div>
      </aside>

      <main className="form-panel">
        <div className="form-panel-content">
          <div className="login-surface">
            <div className="login-card">
              <div className="login-header">
                <h1 className="login-title">Welcome Back!</h1>
                <p className="login-subtitle">Sign in to continue to Seva Impact</p>
              </div>

              {error && <div className="login-error" role="alert">{error}</div>}
              {success && <div className="login-success" role="status">{success}</div>}

              <form className="login-form" onSubmit={handleSubmit} noValidate>
                <div className="form-group">
                  <label htmlFor="email">Email Address</label>
                  <div className="input-wrapper">
                    <Mail size={16} className="input-icon" />
                    <input
                      id="email"
                      name="email"
                      type="email"
                      placeholder="Enter your email"
                      value={formData.email}
                      onChange={handleChange}
                      disabled={loading}
                      className={fieldErrors.email ? "input-error" : ""}
                      autoComplete="email"
                    />
                  </div>
                  {fieldErrors.email && (
                    <span className="field-error">{fieldErrors.email}</span>
                  )}
                </div>

                <div className="form-group">
                  <label htmlFor="password">Password</label>
                  <div className="input-wrapper password-wrapper">
                    <Lock size={16} className="input-icon" />
                    <input
                      id="password"
                      name="password"
                      type={showPassword ? "text" : "password"}
                      placeholder="Enter your password"
                      value={formData.password}
                      onChange={handleChange}
                      disabled={loading}
                      className={fieldErrors.password ? "input-error" : ""}
                      autoComplete="current-password"
                    />
                    <button
                      type="button"
                      className="toggle-password"
                      onClick={() => setShowPassword((prev) => !prev)}
                      tabIndex={-1}
                      aria-label={showPassword ? "Hide password" : "Show password"}
                    >
                      {showPassword ? <EyeOff size={16} /> : <Eye size={16} />}
                    </button>
                  </div>
                  {fieldErrors.password && (
                    <span className="field-error">{fieldErrors.password}</span>
                  )}
                </div>

                <div className="form-row">
                  <label className="remember-me">
                    <input
                      type="checkbox"
                      name="rememberMe"
                      checked={formData.rememberMe}
                      onChange={handleChange}
                      disabled={loading}
                    />
                    <span>Remember Me</span>
                  </label>
                  <a href="#forgot-password" className="forgot-link">
                    Forgot Password?
                  </a>
                </div>

                <button type="submit" className="login-button" disabled={loading}>
                  {loading ? "Logging in…" : "Sign In"}
                  {!loading && <span className="arrow">→</span>}
                </button>
              </form>
            </div>

            <div className="trust-strip">
              <p className="trust-strip-title">Trusted by NGOs and CSR Partners</p>

              <div className="trust-strip-cards">
                <div>
                  <strong>500+</strong>
                  <span>Projects Managed</span>
                </div>
                <div>
                  <strong>250+</strong>
                  <span>Partner Organizations</span>
                </div>
                <div>
                  <strong>1M+</strong>
                  <span>Lives Impacted</span>
                </div>
                <div>
                  <strong>100%</strong>
                  <span>Transparency</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </main>
    </div>
  );
}
