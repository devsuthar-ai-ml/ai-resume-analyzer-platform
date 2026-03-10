import {
  Bar,
  BarChart,
  CartesianGrid,
  Cell,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis
} from "recharts";

import { ScoreBreakdown } from "../types/analysis";

const colors = ["#0ea5e9", "#22c55e", "#f59e0b", "#6366f1"];

function ScoreBreakdownChart({ breakdown }: { breakdown: ScoreBreakdown }) {
  const data = [
    { name: "Skill", value: breakdown.skill_coverage },
    { name: "Semantic", value: breakdown.semantic_similarity },
    { name: "Experience", value: breakdown.experience_strength },
    { name: "Education", value: breakdown.education_strength }
  ];

  return (
    <div className="card h-80">
      <h3 className="mb-4 text-lg font-semibold">Score Breakdown</h3>
      <ResponsiveContainer width="100%" height="90%">
        <BarChart data={data}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="name" />
          <YAxis domain={[0, 100]} />
          <Tooltip />
          <Bar dataKey="value" radius={[8, 8, 0, 0]}>
            {data.map((entry, index) => (
              <Cell key={entry.name} fill={colors[index % colors.length]} />
            ))}
          </Bar>
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
}

export default ScoreBreakdownChart;
