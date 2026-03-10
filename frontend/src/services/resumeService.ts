import api from "./api";
import { ResumeHistoryResponse, ResumeUploadResponse } from "../types/resume";

export const uploadResume = async (file: File): Promise<ResumeUploadResponse> => {
  const formData = new FormData();
  formData.append("file", file);

  const response = await api.post<ResumeUploadResponse>("/resume/upload", formData, {
    headers: { "Content-Type": "multipart/form-data" }
  });
  return response.data;
};

export const getResumeHistory = async (): Promise<ResumeHistoryResponse> => {
  const response = await api.get<ResumeHistoryResponse>("/resume/history");
  return response.data;
};
