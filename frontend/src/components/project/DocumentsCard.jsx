import { FileText } from "lucide-react";

export default function DocumentsCard({ documents = [] }) {
  return (
    <div className="card">
      <h3 className="pd-section-title">Recent Files</h3>

      <ul className="recent-files">
        {documents.slice(0,3).map((doc)=>(
          <li key={doc.name} className="recent-file">

            <FileText size={18}/>

            <span>{doc.name}</span>

          </li>
        ))}
      </ul>

      {documents.length>3 && (
        <a href="#" className="view-files">
          View {documents.length-3} more files →
        </a>
      )}
    </div>
  );
}