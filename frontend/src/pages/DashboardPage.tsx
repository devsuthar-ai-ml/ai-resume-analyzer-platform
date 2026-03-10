import { useEffect, useState } from "react";
import { Link } from "react-router-dom";

import { useAuth } from "../hooks/useAuth";
import { getResumeHistory } from "../services/resumeService";
import { ResumeHistoryItem } from "../types/resume";
import { formatDateTime, formatFileSize } from "../utils/format";

function DashboardPage() {
  const { user } = useAuth();
  const [history, setHistory] = useState<ResumeHistoryItem[]>([]);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    const fetchHistory = async () => {
      try {
        const result = await getResumeHistory();
        setHistory(result.items);
      } finally {
        setIsLoading(false);
      }
    };

    fetchHistory();
  }, []);

  return (
    <section className="space-y-6">
      <div className="card">
        <h1 className="section-title">Welcome, {user?.full_name}</h1>
        <p className="mt-2 text-slate-600">Track uploads and run targeted resume-to-job analysis.</p>
        <Link to="/upload" className="mt-4 inline-block rounded-lg bg-accent px-4 py-2 text-white">
          Upload New Resume
        </Link>
      </div>

      <div className="card">
        <h2 className="mb-4 text-xl font-semibold">Upload History</h2>
        {isLoading ? (
          <p className="text-slate-600">Loading...</p>
        ) : history.length === 0 ? (
          <p className="text-slate-600">No resumes uploaded yet.</p>
        ) : (
          <div className="overflow-x-auto">
            <table className="min-w-full text-left text-sm">
              <thead>
                <tr className="border-b border-slate-200 text-slate-600">
                  <th className="px-2 py-2">File</th>
                  <th className="px-2 py-2">Type</th>
                  <th className="px-2 py-2">Size</th>
                  <th className="px-2 py-2">Uploaded</th>
                </tr>
              </thead>
              <tbody>
                {history.map((item) => (
                  <tr key={item.id} className="border-b border-slate-100">
                    <td className="px-2 py-2">{item.original_filename}</td>
                    <td className="px-2 py-2 uppercase">{item.file_type.replace(".", "")}</td>
                    <td className="px-2 py-2">{formatFileSize(item.file_size)}</td>
                    <td className="px-2 py-2">{formatDateTime(item.created_at)}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </section>
  );
}

export default DashboardPage;
