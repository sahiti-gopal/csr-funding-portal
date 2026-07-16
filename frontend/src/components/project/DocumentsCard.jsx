import { FileText } from "lucide-react";

import Collapsible from "./Collapsible";

export default function DocumentsCard({ documents = [] }) {
  return (
    <Collapsible title="Recent Files" wrapperClassName="card">
      {documents.length === 0 ? (
        <p className="pd-empty-note">
          No files uploaded yet.
        </p>
      ) : (
        <ul className="recent-files">
          {documents.slice(0,3).map((doc)=>(
            <li key={doc.name} className="recent-file">

              <FileText size={18}/>

              <span>{doc.name}</span>

            </li>
          ))}
        </ul>
      )}

      {documents.length>3 && (
        <a href="#" className="view-files">
          View {documents.length-3} more files →
        </a>
      )}
    </Collapsible>
  );
}