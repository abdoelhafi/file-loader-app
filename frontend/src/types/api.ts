export interface UploadedFile {
  id: number;
  name: string;
  size: string;
  uploadDate: string;
}

export interface ApiFile {
  id: number;
  name: string;
  size: number;
  uploaded_at: string;
}

export interface ApiResponse<T> {
  success: boolean;
  data: T;
  error: string | null;
  message: string | null;
  timestamp: string;
}

export interface ApiError {
  message: string;
  code?: string;
  details?: unknown;
}

export interface FileValidationResult {
  isValid: boolean;
  error?: string;
}
