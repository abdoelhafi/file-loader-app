export interface UploadedFile {
  id: number;
  name: string;
  size: string;
  uploadDate: string;
}

export interface FileValidationResult {
  isValid: boolean;
  error?: string;
}
