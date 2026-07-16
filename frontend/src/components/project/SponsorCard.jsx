import { Building2 } from "lucide-react";

export default function SponsorCard({ sponsor }) {
  if (!sponsor) return null;

  return (
    <div className="card">
      <h3 className="pd-section-title">Sponsoring Company</h3>

      <div className="pd-sponsor">
        <span className="pd-sponsor-icon">
          <Building2 size={26} />
        </span>
        <div>
          <p className="pd-sponsor-name">{sponsor.name}</p>
          <p className="pd-sponsor-meta">{sponsor.meta}</p>
        </div>
      </div>
    </div>
  );
}
