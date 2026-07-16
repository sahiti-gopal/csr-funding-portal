import { ImageIcon } from "lucide-react";

export default function Gallery({ images = [] }) {
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
          {images.map((image) => (
            <figure className="pd-gallery-item" key={image.id}>
              <img src={image.url} alt={image.caption} />
              <figcaption>{image.caption}</figcaption>
            </figure>
          ))}
        </div>
      )}
    </div>
  );
}
