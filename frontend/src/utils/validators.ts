import type { ApiFile, ApiResponse } from "../types/api";

export class ValidationError extends Error {
    constructor(message: string) {
      super(message);
      this.name = 'ValidationError';
    }
  }
  
export  const validateApiResponse = <T>(response: ApiResponse<T>): T => {
    if (!response.success || !response.data) {
      throw new ValidationError(response.error || 'Invalid API response');
    }
    return response.data;
  };
  
export  const validateFileData = (file: ApiFile): void => {
    if (!file.id || typeof file.id !== 'number') {
      throw new ValidationError('Invalid file ID');
    }
    if (!file.name || typeof file.name !== 'string') {
      throw new ValidationError('Invalid file name');
    }
    if (typeof file.size !== 'number' || file.size < 0) {
      throw new ValidationError('Invalid file size');
    }
    if (!Date.parse(file.uploaded_at)) {
      throw new ValidationError('Invalid upload date');
    }
  };