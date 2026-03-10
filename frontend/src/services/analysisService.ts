import api from "./api";
import { AnalysisResult, AnalyzePayload } from "../types/analysis";

export const analyzeResume = async (payload: AnalyzePayload): Promise<AnalysisResult> => {
  const response = await api.post<AnalysisResult>("/analyze", payload);
  return response.data;
};

export const getAnalysisResult = async (id: number): Promise<AnalysisResult> => {
  const response = await api.get<AnalysisResult>(`/results/${id}`);
  return response.data;
};
