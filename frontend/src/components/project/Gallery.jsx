import { useEffect, useState } from "react";
import { createPortal } from "react-dom";
import { ImageIcon, X, ChevronLeft, ChevronRight } from "lucide-react";

const formatCurrency = (value) => {
  if (value == null) return "—";
  return new Intl.NumberFormat("en-IN", {
    style: "currency",
    currency: "INR",
    maximumFractionDigits: 0,
  }).format(Number(value));
};

export default function Gallery({ images = [], project }) {
  const [activeIndex, setActiveIndex] = useState(null);
  const isOpen = activeIndex !== null;
  const activeImage = isOpen ? images[activeIndex] : null;

  useEffect(() => {
    if (!isOpen) return;

    const handleKeyDown = (event) => {
      if (event.key === "Escape") setActiveIndex(null);
      if (event.key === "ArrowRight") {
        setActiveIndex((prev) => (prev + 1) % images.length);
      }
      if (event.key === "ArrowLeft") {
        setActiveIndex((prev) => (prev - 1 + images.length) % images.length);
      }
    };

    document.addEventListener("keydown", handleKeyDown);
    return () => document.removeEventListener("keydown", handleKeyDown);
  }, [isOpen, images.length]);

  const showPrev = () =>
    setActiveIndex((prev) => (prev - 1 + images.length) % images.length);
  const showNext = () => setActiveIndex((prev) => (prev + 1) % images.length);

  return (
    <div className="card">
      <h3 className="pd-section-title">Project Gallery</h3>

      {images.length === 0 ? (
        <div className="pd-gallery-empty">
          <ImageIcon size={32} />
          <p>No photos uploaded yet.</p>
        </div>
      ) : (
        <div className="pd-gallery-grid">
          {images.map((image, index) => (
            <figure
              className="pd-gallery-item"
              key={image.id}
              onClick={() => setActiveIndex(index)}
            >
              <img src={image.url} alt={image.caption} />
              <figcaption>{image.caption}</figcaption>
            </figure>
          ))}
        </div>
      )}

      {isOpen &&
        createPortal(
          <div
            className="pd-lightbox-overlay"
            onClick={() => setActiveIndex(null)}
          >
            <div
              className="pd-lightbox"
              role="dialog"
              aria-modal="true"
              onClick={(event) => event.stopPropagation()}
            >
              <button
                type="button"
                className="pd-lightbox-close"
                aria-label="Close"
                onClick={() => setActiveIndex(null)}
              >
                <X size={16} />
              </button>

              <div className="pd-lightbox-image">
                {images.length > 1 && (
                  <button
                    type="button"
                    className="pd-lightbox-nav pd-lightbox-prev"
                    aria-label="Previous image"
                    onClick={showPrev}
                  >
                    <ChevronLeft size={20} />
                  </button>
                )}

                <img src={activeImage.url} alt={activeImage.caption} />

                {images.length > 1 && (
                  <button
                    type="button"
                    className="pd-lightbox-nav pd-lightbox-next"
                    aria-label="Next image"
                    onClick={showNext}
                  >
                    <ChevronRight size={20} />
                  </button>
                )}

                {activeImage.caption && (
                  <figcaption className="pd-lightbox-caption">
                    {activeImage.caption}
                  </figcaption>
                )}
              </div>

              {project && (
                <div className="pd-lightbox-summary">
                  <span className="pd-lightbox-summary-eyebrow">
                    Project Summary
                  </span>

                  <h3>{project.project_name}</h3>

                  {project.status && (
                    <span className="pd-badge pd-badge-outline">
                      {project.status}
                    </span>
                  )}

                  <dl className="pd-lightbox-summary-list">
                    {project.sponsor?.name && (
                      <div>
                        <dt>Sponsor</dt>
                        <dd>{project.sponsor.name}</dd>
                      </div>
                    )}

                    <div>
                      <dt>Budget</dt>
                      <dd>{formatCurrency(project.budget)}</dd>
                    </div>

                    {project.locations?.length > 0 && (
                      <div>
                        <dt>Location</dt>
                        <dd>{project.locations.join(", ")}</dd>
                      </div>
                    )}

                    {(project.start_date || project.end_date) && (
                      <div>
                        <dt>Timeline</dt>
                        <dd>
                          {project.start_date} – {project.end_date}
                        </dd>
                      </div>
                    )}
                  </dl>
                </div>
              )}
            </div>
          </div>,
          document.body
        )}
    </div>
  );
}
