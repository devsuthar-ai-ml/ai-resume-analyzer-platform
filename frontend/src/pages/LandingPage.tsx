import { Link } from "react-router-dom";

function LandingPage() {
  return (
    <section className="grid gap-8 md:grid-cols-2 md:items-center">
      <div className="space-y-6">
        <h1 className="text-4xl font-bold text-slate-900 md:text-5xl">
          Analyze resumes against job descriptions with AI precision.
        </h1>
        <p className="text-lg text-slate-600">
          Upload your resume, compare it with a target role, and get skill gap insights, score breakdown,
          and improvement suggestions in seconds.
        </p>
        <div className="flex gap-4">
          <Link to="/signup" className="rounded-lg bg-slateBrand px-5 py-3 font-medium text-white">
            Get Started
          </Link>
          <Link to="/login" className="rounded-lg border border-slate-300 px-5 py-3 font-medium">
            Login
          </Link>
        </div>
      </div>
      <div className="card space-y-4">
        <h2 className="text-xl font-semibold">What you get</h2>
        <ul className="space-y-2 text-slate-700">
          <li>- Resume score out of 100</li>
          <li>- Detected and missing skills</li>
          <li>- Keyword and semantic matching</li>
          <li>- Suggestions to improve interview readiness</li>
        </ul>
      </div>
    </section>
  );
}

export default LandingPage;
