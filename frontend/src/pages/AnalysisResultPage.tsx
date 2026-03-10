import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";

import ScoreBreakdownChart from "../components/ScoreBreakdownChart";
import { getAnalysisResult } from "../services/analysisService";
import { AnalysisResult } from "../types/analysis";
import { formatDateTime } from "../utils/format";

function AnalysisResultPage() {
  const { id } = useParams();
  const [result, setResult] = useState<AnalysisResult | null>(null);
  const [error, setError] = useState("");

  useEffect(() => {
    const loadData = async () => {
      try {
        if (!id) {
          return;
        }
        const data = await getAnalysisResult(Number(id));
        setResult(data);
      } catch (err: any) {
        setError(err?.response?.data?.detail || "Failed to load analysis");
      }
    };

    loadData();
  }, [id]);

  if (error) {
    return <p className="text-red-600">{error}</p>;
  }

  if (!result) {
    return <p className="text-slate-600">Loading analysis...</p>;
  }

  return (
    <section className="space-y-6">
      <div className="grid gap-4 md:grid-cols-3">
        <div className="card">
          <p className="text-sm text-slate-500">Resume Score</p>
          <p className="mt-2 text-4xl font-bold text-slateBrand">{result.resume_score}/100</p>
        </div>
        <div className="card">
          <p className="text-sm text-slate-500">Match Percentage</p>
          <p className="mt-2 text-4xl font-bold text-success">{result.match_percentage}%</p>
        </div>
        <div className="card">
          <p className="text-sm text-slate-500">Generated</p>
          <p className="mt-2 text-lg font-semibold">{formatDateTime(result.created_at)}</p>
        </div>
      </div>

      <ScoreBreakdownChart breakdown={result.score_breakdown} />

      <div className="grid gap-6 md:grid-cols-2">
        <div className="card">
          <h2 className="mb-3 text-lg font-semibold">Skills Detected</h2>
          <div className="flex flex-wrap gap-2">
            {result.detected_skills.map((skill) => (
              <span key={skill} className="rounded-full bg-slate-100 px-3 py-1 text-sm text-slate-700">
                {skill}
              </span>
            ))}
          </div>
        </div>

        <div className="card">
          <h2 className="mb-3 text-lg font-semibold">Missing Skills</h2>
          <div className="flex flex-wrap gap-2">
            {result.missing_skills.length === 0 ? (
              <span className="text-sm text-slate-600">No major skill gaps detected.</span>
            ) : (
              result.missing_skills.map((skill) => (
                <span key={skill} className="rounded-full bg-amber-100 px-3 py-1 text-sm text-amber-800">
                  {skill}
                </span>
              ))
            )}
          </div>
        </div>
      </div>

      <div className="card">
        <h2 className="mb-3 text-lg font-semibold">Improvement Suggestions</h2>
        <ul className="space-y-2 text-slate-700">
          {result.suggestions.map((item, index) => (
            <li key={item}> {index + 1}. {item}</li>
          ))}
        </ul>
      </div>
    </section>
  );
}

export default AnalysisResultPage;
