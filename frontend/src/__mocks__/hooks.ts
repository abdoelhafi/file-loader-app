export const useFileManager = jest.fn(() => ({
    files: [],
    loading: false,
    fetchFiles: jest.fn(),
    uploadFile: jest.fn(),
    deleteFile: jest.fn(),
  }));