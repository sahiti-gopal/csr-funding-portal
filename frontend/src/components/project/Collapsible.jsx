import { useState } from "react";
import { ChevronDown, ChevronUp } from "lucide-react";

export default function Collapsible({
  title,
  defaultOpen = false,
  wrapperClassName = "card",
  children,
}) {
  const [open, setOpen] = useState(defaultOpen);

  return (
    <div className={wrapperClassName}>
      <button
        type="button"
        className="pd-collapse-header"
        onClick={() => setOpen((prev) => !prev)}
        aria-expanded={open}
      >
        <h3 className="pd-section-title">{title}</h3>
        <span className="pd-collapse-right">
          {open ? <ChevronUp size={18} /> : <ChevronDown size={18} />}
        </span>
      </button>

      {open && <div className="pd-collapse-body">{children}</div>}
    </div>
  );
}
