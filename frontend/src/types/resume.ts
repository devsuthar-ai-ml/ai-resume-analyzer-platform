export interface ResumeUploadResponse {
  id: number;
  filename: string;
  original_filename: string;
  file_type: string;
  file_size: number;
  created_at: string;
}

export interface ResumeHistoryItem {
  id: number;
  original_filename: string;
  file_type: string;
  file_size: number;
  created_at: string;
}

export interface ResumeHistoryResponse {
  items: ResumeHistoryItem[];
}
