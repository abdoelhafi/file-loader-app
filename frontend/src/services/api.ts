// services/api.ts
import axios from "axios";
import { UploadedFile } from "../types/file";

const API_URL = "http://localhost:8000/api";

const api = axios.create({
  baseURL: API_URL,
});

export const fileService = {
  async uploadFile(file: File): Promise<UploadedFile> {
    const formData = new FormData();
    formData.append("file", file);

    const response = await api.post("/files/", formData, {
      headers: {
        "Content-Type": "multipart/form-data",
      },
    });

    return {
      id: response.data.id,
      name: response.data.name,
      size: response.data.size.toFixed(2),
      uploadDate: new Date(response.data.uploaded_at).toLocaleString(),
    };
  },

  async getFiles(): Promise<UploadedFile[]> {
    const response = await api.get("/files/");
    return response.data.map((file: any) => ({
      id: file.id,
      name: file.name,
      size: file.size.toFixed(2),
      uploadDate: new Date(file.uploaded_at).toLocaleString(),
    }));
  },

  async deleteFile(id: number): Promise<void> {
    await api.delete(`/files/${id}/`);
  },
};
