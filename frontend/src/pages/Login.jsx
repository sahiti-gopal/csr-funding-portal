import { useState } from "react";
import { useForm } from "react-hook-form";
import { useNavigate } from "react-router-dom";
import { z } from "zod";
import {
  Mail,
  Lock,
  Eye,
  EyeOff,
  Leaf,
  HeartHandshake,
  FolderKanban,
  ShieldCheck,
  BarChart3,
} from "lucide-react";

import { login } from "../services/authService";

import "../styles/login.css";

const loginSchema = z.object({
  email: z.string().min(1, "Email is required").email("Enter a valid email address"),
  password: z.string().min(1, "Password is required"),
});

const FEATURES = [
  { icon: HeartHandshake, label: "Track Donations & Utilisation" },
  { icon: FolderKanban, label: "Manage Projects & Performance" },
  { icon: ShieldCheck, label: "Ensure Compliance & Transparency" },
  { icon: BarChart3, label: "Measure & Maximize Impact" },
];

const STATS = [
  { value: "500+", label: "Projects Managed" },
  { value: "250+", label: "Partner Organizations" },
  { value: "1M+", label: "Lives Impacted" },
  { value: "100%", label: "Transparency" },
];

export default function Login() {
  const navigate = useNavigate();
  const [showPassword, setShowPassword] = useState(false);
  const [serverError, setServerError] = useState("");
  const [submitting, setSubmitting] = useState(false);

  const {
    register,
    handleSubmit,
    setError,
    formState: { errors },
  } = useForm({ defaultValues: { email: "", password: "" } });

  const onSubmit = async (values) => {
    setServerError("");

    const result = loginSchema.safeParse(values);
    if (!result.success) {
      result.error.issues.forEach((issue) => {
        setError(issue.path[0], { message: issue.message });
      });
      return;
    }

    setSubmitting(true);
    try {
      await login(result.data.email, result.data.password);
      navigate("/");
    } catch (err) {
      setServerError(
        err.response?.data?.message || "Unable to sign in. Please check your credentials and try again."
      );
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <div className="login-shell">
      <div className="login-visual">
        <img
          src="/images/gallery/maternalcare/mc_2.webp"
          alt=""
          className="login-visual-photo"
        />
        <div className="login-visual-overlay" />

        <div className="login-visual-content">
          <div className="login-brand">
            <span className="login-brand-mark">
              <Leaf size={20} />
            </span>
            <div>
              <p className="login-brand-name">Seva Impact</p>
              <p className="login-brand-tagline">Measure. Manage. Maximize Impact.</p>
            </div>
          </div>

          <h1 className="login-headline">
            Empowering Change.
            <br />
            <span>Creating Lasting Impact.</span>
          </h1>

          <p className="login-subcopy">
            A unified platform to manage CSR partnerships, track projects, ensure
            compliance, and measure social impact that matters.
          </p>

          <div className="login-features">
            {FEATURES.map(({ icon: Icon, label }) => (
              <span key={label} className="login-feature-pill">
                <Icon size={14} />
                {label}
              </span>
            ))}
          </div>
        </div>

        <div className="login-stats">
          <p className="login-stats-caption">Trusted by NGOs and CSR Partners</p>
          <div className="login-stats-row">
            {STATS.map((stat) => (
              <div key={stat.label} className="login-stat">
                <p className="login-stat-value">{stat.value}</p>
                <p className="login-stat-label">{stat.label}</p>
              </div>
            ))}
          </div>
        </div>
      </div>

      <div className="login-panel">
        <div className="login-card">
          <h2 className="login-title">Welcome Back!</h2>
          <p className="login-subtitle">Sign in to continue to Seva Impact</p>

          <form className="login-form" onSubmit={handleSubmit(onSubmit)} noValidate>
            <label className="login-field">
              <span className="login-field-label">Email Address</span>
              <span className="login-input-wrap">
                <Mail size={17} className="login-input-icon" />
                <input
                  type="email"
                  placeholder="Enter your email"
                  autoComplete="email"
                  {...register("email")}
                />
              </span>
              {errors.email && <span className="login-field-error">{errors.email.message}</span>}
            </label>

            <label className="login-field">
              <span className="login-field-label">Password</span>
              <span className="login-input-wrap">
                <Lock size={17} className="login-input-icon" />
                <input
                  type={showPassword ? "text" : "password"}
                  placeholder="Enter your password"
                  autoComplete="current-password"
                  {...register("password")}
                />
                <button
                  type="button"
                  className="login-input-toggle"
                  onClick={() => setShowPassword((prev) => !prev)}
                  aria-label={showPassword ? "Hide password" : "Show password"}
                >
                  {showPassword ? <EyeOff size={17} /> : <Eye size={17} />}
                </button>
              </span>
              {errors.password && <span className="login-field-error">{errors.password.message}</span>}
            </label>

            <div className="login-form-row">
              <span />
              <a href="#" className="login-forgot">Forgot Password?</a>
            </div>

            {serverError && <p className="login-server-error">{serverError}</p>}

            <button type="submit" className="login-submit" disabled={submitting}>
              {submitting ? "Signing In…" : "Sign In"}
              {!submitting && <span aria-hidden>→</span>}
            </button>

            <div className="login-divider">
              <span />
              <p>or continue with</p>
              <span />
            </div>

            <div className="login-oauth-row">
              <button type="button" className="login-oauth-btn">
                <GoogleGlyph />
                Sign in with Google
              </button>
              <button type="button" className="login-oauth-btn">
                <MicrosoftGlyph />
                Sign in with Microsoft
              </button>
            </div>

            <p className="login-signup-hint">
              Don&rsquo;t have an account? <a href="#">Contact Admin</a>
            </p>
          </form>
        </div>
      </div>
    </div>
  );
}

function GoogleGlyph() {
  return (
    <svg width="16" height="16" viewBox="0 0 48 48" aria-hidden="true">
      <path fill="#FFC107" d="M43.6 20.5H42V20H24v8h11.3c-1.6 4.7-6.1 8-11.3 8-6.6 0-12-5.4-12-12s5.4-12 12-12c3.1 0 5.9 1.2 8 3.1l5.7-5.7C34.5 6 29.5 4 24 4 12.9 4 4 12.9 4 24s8.9 20 20 20 20-8.9 20-20c0-1.3-.1-2.7-.4-3.5z"/>
      <path fill="#FF3D00" d="M6.3 14.7l6.6 4.8C14.6 15.6 18.9 12 24 12c3.1 0 5.9 1.2 8 3.1l5.7-5.7C34.5 6 29.5 4 24 4c-7.5 0-13.9 4.2-17.7 10.7z"/>
      <path fill="#4CAF50" d="M24 44c5.4 0 10.3-1.9 14.1-5.2l-6.5-5.5c-2 1.5-4.7 2.7-7.6 2.7-5.2 0-9.6-3.3-11.3-7.9l-6.6 5.1C9.9 39.6 16.4 44 24 44z"/>
      <path fill="#1976D2" d="M43.6 20.5H42V20H24v8h11.3c-.8 2.3-2.2 4.2-4.1 5.7l6.5 5.5C41.4 36 44 30.4 44 24c0-1.3-.1-2.7-.4-3.5z"/>
    </svg>
  );
}

function MicrosoftGlyph() {
  return (
    <svg width="16" height="16" viewBox="0 0 23 23" aria-hidden="true">
      <path fill="#F35325" d="M1 1h10v10H1z"/>
      <path fill="#81BC06" d="M12 1h10v10H12z"/>
      <path fill="#05A6F0" d="M1 12h10v10H1z"/>
      <path fill="#FFBA08" d="M12 12h10v10H12z"/>
    </svg>
  );
}
