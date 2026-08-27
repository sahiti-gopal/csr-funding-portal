import Collapsible from "./Collapsible";
import { formatCurrency as formatCurrencyValue } from "../../utils/format";

const initials = (name = "") =>
  name
    .split(" ")
    .filter(Boolean)
    .slice(0, 2)
    .map((word) => word[0])
    .join("")
    .toUpperCase();

const formatCurrency = (value) =>
  value == null ? null : formatCurrencyValue(value);

const SPONSOR_LOGOS = {
  "Aditya Birla CSR": "/images/gallery/abg-renewable-logo.png",
};

export default function SponsorCard({ sponsor }) {
  if (!sponsor) return null;

  const logo = SPONSOR_LOGOS[sponsor.name];

  return (
    <Collapsible
      title="Sponsoring Company"
      wrapperClassName="card sponsor-card"
    >
      <div className="pd-sponsor">
        {logo ? (
          <span className="pd-sponsor-icon pd-sponsor-logo">
            <img src={logo} alt={sponsor.name} />
          </span>
        ) : (
          <span className="pd-sponsor-icon pd-sponsor-avatar">
            {initials(sponsor.name)}
          </span>
        )}
        <div>
          <p className="pd-sponsor-name">{sponsor.name}</p>
          <p className="pd-sponsor-meta">{sponsor.meta}</p>
        </div>
      </div>

      {(sponsor.grant_amount != null || sponsor.contract_period) && (
        <>
          <div className="owner-divider pd-sponsor-details" />

          {sponsor.grant_amount != null && (
            <div className="owner-row">
              <span>Grant Amount</span>
              <strong>{formatCurrency(sponsor.grant_amount)}</strong>
            </div>
          )}

          {sponsor.contract_period && (
            <div className="owner-row">
              <span>Contract Period</span>
              <strong>{sponsor.contract_period}</strong>
            </div>
          )}
        </>
      )}
    </Collapsible>
  );
}
