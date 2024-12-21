import axios, { AxiosError, AxiosInstance, AxiosResponse } from 'axios';
import { API_CONFIG } from '../config/api';
import { ValidationError, validateApiResponse, validateFileData } from '../utils/validators';
import type { UploadedFile, ApiFile, ApiResponse, ApiError } from '../types/api';

interface ErrorResponse {
  error?: string;
}

class FileService {
  private api: AxiosInstance;

  constructor() {
    this.api = axios.create(API_CONFIG);
    
    this.api.interceptors.response.use(
      (response) => response,
      this.handleAxiosError.bind(this)
    );
  }

  private handleAxiosError(error: AxiosError<ErrorResponse>): never {
    if (error.response) {
      const apiError: ApiError = {
        message: error.response.data?.error || 'Server error',
        code: error.response.status.toString(),
        details: error.response.data,
      };
      throw apiError;
    }
    
    if (error.request) {
      throw new Error('No response received from server');
    }
    
    throw new Error('Error setting up request');
  }

  private transformFileData(file: ApiFile): UploadedFile {
    validateFileData(file);
    return {
      id: file.id,
      name: file.name,
      size: file.size.toFixed(2),
      uploadDate: new Date(file.uploaded_at).toLocaleString(),
    };
  }

  async uploadFile(file: File): Promise<UploadedFile> {
    try {
      if (!file || !(file instanceof File)) {
        throw new ValidationError('Invalid file object');
      }

      const formData = new FormData();
      formData.append('file', file);

      const response = await this.api.post<ApiResponse<ApiFile>>('/files/', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });

      const validatedData = validateApiResponse(response.data);
      return this.transformFileData(validatedData);
    } catch (error) {
      if (error instanceof ValidationError) {
        throw error;
      }
      if (axios.isAxiosError(error)) {
        throw this.handleAxiosError(error);
      }
      throw new Error('Failed to upload file');
    }
  }

  async getFiles(): Promise<UploadedFile[]> {
    try {
      const response = await this.api.get<ApiResponse<ApiFile[]>>('/files/');
      const validatedData = validateApiResponse(response.data);
      if ( Object.keys(validatedData).length === 0 ) {
        return []
      }
      return validatedData.map((file) => {
        validateFileData(file);
        return this.transformFileData(file);
      });
    } catch (error) {
      if (error instanceof ValidationError) {
        throw error;
      }
      if (axios.isAxiosError(error)) {
        throw this.handleAxiosError(error);
      }
      throw new Error('Failed to fetch files');
    }
  }

  async deleteFile(id: number): Promise<void> {
    try {
      if (!id || typeof id !== 'number') {
        throw new ValidationError('Invalid file ID');
      }

      await this.api.delete(`/files/${id}/`);
    } catch (error) {
      if (error instanceof ValidationError) {
        throw error;
      }
      if (axios.isAxiosError(error)) {
        throw this.handleAxiosError(error);
      }
      throw new Error('Failed to delete file');
    }
  }
}

export const fileService = new FileService();
