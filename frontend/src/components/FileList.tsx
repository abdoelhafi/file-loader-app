// components/FileList.tsx
import React, { useCallback, useRef } from "react";
import { FileText, Trash2, Upload, Plus } from "lucide-react";
import type { UploadedFile } from "../types/api";
import { Loading } from "./ui/Loading";

interface FileListProps {
  files: UploadedFile[];
  searchQuery: string;
  loading: boolean;
  dragActive: boolean;
  error?: string;
  onDragOver: (e: React.DragEvent) => void;
  onDragLeave: () => void;
  onDrop: (e: React.DragEvent) => void;
  onFileSelect: (e: React.ChangeEvent<HTMLInputElement>) => void;
  onDelete?: (id: number) => void;
}

export const FileList: React.FC<FileListProps> = ({
  files,
  searchQuery,
  loading,
  dragActive,
  error,
  onDragOver,
  onDragLeave,
  onDrop,
  onFileSelect,
  onDelete,
}) => {
  const dragCounterRef = useRef(0);

  const handleDragOver = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
  }, []);

  const handleDragEnter = useCallback(
    (e: React.DragEvent) => {
      e.preventDefault();
      e.stopPropagation();
      dragCounterRef.current++;
      onDragOver(e);
    },
    [onDragOver]
  );

  const handleDragLeave = useCallback(
    (e: React.DragEvent) => {
      e.preventDefault();
      e.stopPropagation();
      dragCounterRef.current--;
      if (dragCounterRef.current === 0) {
        onDragLeave();
      }
    },
    [onDragLeave]
  );

  const handleDrop = useCallback(
    (e: React.DragEvent) => {
      e.preventDefault();
      e.stopPropagation();
      dragCounterRef.current = 0;
      onDrop(e);
    },
    [onDrop]
  );

  if (loading) {
    return <Loading />;
  }

  return (
    <div
      className="relative min-h-[400px] transition-all duration-200 ease-in-out rounded-lg border border-gray-200"
      onDragOver={handleDragOver}
      onDragEnter={handleDragEnter}
      onDragLeave={handleDragLeave}
      onDrop={handleDrop}
    >
      {/* Upload Button */}
      <div className="mb-4 flex justify-end p-4">
        <label className="inline-flex items-center gap-2 bg-blue-500 text-white px-4 py-2 rounded-lg cursor-pointer hover:bg-blue-600 transition-colors">
          <Plus size={20} />
          Upload File
          <input
            type="file"
            className="hidden"
            accept=".txt"
            onChange={onFileSelect}
          />
        </label>
      </div>

      {/* Drag Overlay */}
      <div
        className={`absolute inset-0 bg-blue-50 bg-opacity-90 flex items-center justify-center pointer-events-none transition-opacity duration-200 ${
          dragActive ? "opacity-100" : "opacity-0"
        }`}
      >
        <div className="text-center">
          <Upload className="mx-auto text-blue-500 mb-2" size={48} />
          <p className="text-lg font-medium text-blue-700">
            Drop your file here
          </p>
          <p className="text-sm text-blue-600">
            Only .txt files between 0.5KB and 2KB
          </p>
        </div>
      </div>

      {/* File List */}
      <div className="px-4">
        <div className="divide-y divide-gray-200">
          {files.length > 0 ? (
            files.map((file) => (
              <div
                key={file.id}
                className="py-4 flex items-center justify-between hover:bg-gray-50 transition-colors"
              >
                <div className="flex items-center min-w-0">
                  <FileText
                    className="flex-shrink-0 text-blue-500 mr-3"
                    size={24}
                  />
                  <div className="min-w-0">
                    <h4 className="font-medium text-gray-900 truncate">
                      {file.name}
                    </h4>
                    <p className="text-sm text-gray-500">
                      {file.size}KB • Uploaded on {file.uploadDate}
                    </p>
                  </div>
                </div>
                {onDelete && (
                  <button
                    onClick={() => onDelete(file.id)}
                    className="ml-4 flex-shrink-0 text-gray-400 hover:text-red-500 p-2 rounded-full hover:bg-red-50 transition-colors"
                    title="Delete file"
                  >
                    <Trash2 size={20} />
                  </button>
                )}
              </div>
            ))
          ) : (
            <div className="text-center py-12">
              {searchQuery ? (
                <p className="text-gray-500">
                  No files found matching your search.
                </p>
              ) : (
                <div>
                  <FileText className="mx-auto h-12 w-12 text-gray-400 mb-4" />
                  <p className="text-gray-500">No files uploaded yet</p>
                  <p className="text-gray-400 text-sm mt-1">
                    Drag and drop a file or use the upload button
                  </p>
                </div>
              )}
            </div>
          )}
        </div>
      </div>

      {error && <p className="text-sm text-red-500 mt-2 px-4">{error}</p>}
    </div>
  );
};
