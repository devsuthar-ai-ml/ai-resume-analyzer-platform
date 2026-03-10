import { FormEvent, useState } from "react";
import { useNavigate } from "react-router-dom";

import { analyzeResume } from "../services/analysisService";
import { uploadResume } from "../services/resumeService";

function UploadPage() {
  const navigate = useNavigate();
  const [file, setFile] = useState<File | null>(null);
  const [jobTitle, setJobTitle] = useState("");
  const [jobDescription, setJobDescription] = useState("");
  const [error, setError] = useState("");
  const [isLoading, setIsLoading] = useState(false);

  const handleSubmit = async (event: FormEvent) => {
    event.preventDefault();
    setError("");

    if (!file) {
      setError("Please select a PDF or DOCX resume.");
      return;
    }

    setIsLoading(true);
    try {
      const uploadResult = await uploadResume(file);
      const analysis = await analyzeResume({
        resume_id: uploadResult.id,
        job_title: jobTitle,
        job_description: jobDescription
      });
      navigate(`/analysis/${analysis.id}`);
    } catch (err: any) {
      setError(err?.response?.data?.detail || "Failed to process resume");
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <section className="mx-auto max-w-3xl">
      <div className="card">
        <h1 className="section-title">Upload Resume and Analyze</h1>
        <form className="mt-6 space-y-4" onSubmit={handleSubmit}>
          <div>
            <label className="mb-1 block text-sm font-medium">Resume (PDF or DOCX)</label>
            <input
              type="file"
              accept=".pdf,.docx"
              onChange={(e) => setFile(e.target.files?.[0] ?? null)}
              required
              className="w-full rounded-lg border border-slate-300 px-3 py-2"
            />
          </div>
          <div>
            <label className="mb-1 block text-sm font-medium">Job Title</label>
            <input
              type="text"
              value={jobTitle}
              onChange={(e) => setJobTitle(e.target.value)}
              required
              className="w-full rounded-lg border border-slate-300 px-3 py-2"
            />
          </div>
          <div>
            <label className="mb-1 block text-sm font-medium">Job Description</label>
            <textarea
              value={jobDescription}
              onChange={(e) => setJobDescription(e.target.value)}
              required
              minLength={20}
              rows={8}
              className="w-full rounded-lg border border-slate-300 px-3 py-2"
            />
          </div>
          {error && <p className="text-sm text-red-600">{error}</p>}
          <button
            type="submit"
            disabled={isLoading}
            className="rounded-lg bg-slateBrand px-5 py-2 font-medium text-white"
          >
            {isLoading ? "Analyzing..." : "Analyze Resume"}
          </button>
        </form>
      </div>
    </section>
  );
}

export default UploadPage;
