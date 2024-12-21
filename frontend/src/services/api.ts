// services/api.ts
import axios from "axios";
import { UploadedFile } from "../types/file";

const API_URL = "http://localhost:8000/api";

interface ApiResponse<T> {
  success: boolean;
  data: T;
  error: string | null;
  message: string | null;
  timestamp: string;
}

const api = axios.create({
  baseURL: API_URL,
});

export const fileService = {
  async uploadFile(file: File): Promise<UploadedFile> {
    const formData = new FormData();
    formData.append("file", file);

    const response = await api.post<ApiResponse<{
      id: number;
      name: string;
      size: number;
      uploaded_at: string;
    }>>("/files/", formData, {
      headers: {
        "Content-Type": "multipart/form-data",
      },
    });

    const fileData = response.data.data;
    return {
      id: fileData.id,
      name: fileData.name,
      size: fileData.size.toFixed(2),
      uploadDate: new Date(fileData.uploaded_at).toLocaleString(),
    };
  },

  async getFiles(): Promise<UploadedFile[]> {
    const response = await api.get<ApiResponse<Array<{
      id: number;
      name: string;
      size: number;
      uploaded_at: string;
    }>>>("/files/");
    
    return response.data.data.map((file) => ({
      id: file.id,
      name: file.name,
      size: file.size.toFixed(2),
      uploadDate: new Date(file.uploaded_at).toLocaleString(),
    }));
  },

  async deleteFile(id: number): Promise<void> {
    await api.delete(`/files/${id}/`);
  },

  // Optional: Helper method to handle errors
  handleApiError(error: any): string {
    if (axios.isAxiosError(error) && error.response) {
      return error.response.data.error || 'An unexpected error occurred';
    }
    return 'Network error occurred';
  }
};