import { useState, useCallback, useEffect } from "react";
import { toast } from "react-toastify";
import { fileService } from "../services/fileService";
import type { UploadedFile, FileValidationResult } from "../types/api";

export const useFileManager = () => {
  const [files, setFiles] = useState<UploadedFile[]>([]);
  const [error, setError] = useState<string>("");
  const [loading, setLoading] = useState(true);

  // Fetch files on component mount
  useEffect(() => {
    fetchFiles();
  }, []);

  const fetchFiles = async () => {
    try {
      const data = await fileService.getFiles();
      setFiles(data);
    } catch (err) {
      toast.error("Failed to fetch files");
    } finally {
      setLoading(false);
    }
  };

  const validateFile = (file: File): FileValidationResult => {
    if (file.type !== "text/plain") {
      return {
        isValid: false,
        error: "Only .txt files are allowed",
      };
    }

    const fileSize = file.size / 1024;
    if (fileSize < 0.5 || fileSize > 2) {
      return {
        isValid: false,
        error: "File size must be between 0.5KB and 2KB",
      };
    }

    return { isValid: true };
  };

  const handleFileUpload = useCallback(async (file: File) => {
    const validation = validateFile(file);

    if (!validation.isValid) {
      setError(validation.error || "Invalid file");
      toast.error("Invalid file");
      return;
    }

    try {
      setLoading(true);
      const uploadedFile = await fileService.uploadFile(file);
      setFiles((prev) => [...prev, uploadedFile]);
      toast.success("File uploaded successfully!");
      setError("");
    } catch (err: any) {
      toast.error("Failed to upload file");
      setError("Failed to upload file");
    } finally {
      setLoading(false);
    }
  }, []);

  const deleteFile = useCallback(async (id: number) => {
    try {
      setLoading(true);
      await fileService.deleteFile(id);
      setFiles((prev) => prev.filter((file) => file.id !== id));
      toast.success("File deleted successfully!");
    } catch (err) {
      toast.error("Failed to delete file");
    } finally {
      setLoading(false);
    }
  }, []);

  return {
    files,
    error,
    loading,
    handleFileUpload,
    deleteFile,
  };
};
