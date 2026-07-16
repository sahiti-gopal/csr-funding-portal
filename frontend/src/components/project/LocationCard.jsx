import { MapPinned } from "lucide-react";

export default function LocationCard({ locations = [] }) {
  return (
    <div className="pd-panel">
      <h4 className="pd-panel-title">Project Locations</h4>

      <div className="pd-location-map">
        <MapPinned size={70} />
        <p>India Map (Coming Soon)</p>
      </div>

      <div className="pd-chips">
        {locations.map((location) => (
          <span key={location} className="pd-chip">
            📍 {location}
          </span>
        ))}
      </div>
    </div>
  );
}