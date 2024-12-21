// src/App.test.tsx
import { screen } from '@testing-library/react';
import { render } from './test-utils';
import App from './App';
import { useFileManager } from './hooks/useFileManager';
import type { UploadedFile } from './types/api';

jest.mock('./hooks/useFileManager');
const mockUseFileManager = useFileManager as jest.MockedFunction<typeof useFileManager>;

// Mock react-toastify
jest.mock('react-toastify', () => ({
  toast: {
    error: jest.fn(),
    success: jest.fn(),
  },
  ToastContainer: () => null,
}));

describe('App Component', () => {
  beforeEach(() => {
    jest.clearAllMocks();
    
    // Default mock implementation
    mockUseFileManager.mockReturnValue({
      files: [],
      error: "",
      loading: false,
      handleFileUpload: jest.fn().mockImplementation(async () => {}),
      deleteFile: jest.fn().mockImplementation(async () => {}),
    });
  });

  afterEach(() => {
    jest.restoreAllMocks();
  });

  it('renders without crashing', async () => {
    render(<App />);
    const element = await screen.findByText('File Upload Dashboard');
    expect(element).toBeInTheDocument();
  });

  it('displays files when loaded', async () => {
    const mockFiles: UploadedFile[] = [
      {
        id: 1,
        name: 'test.txt',
        size: '1.5',
        uploadDate: '2024-12-21',
      }
    ];

    mockUseFileManager.mockReturnValue({
      files: mockFiles,
      error: "",
      loading: false,
      handleFileUpload: jest.fn().mockImplementation(async () => {}),
      deleteFile: jest.fn().mockImplementation(async () => {}),
    });

    render(<App />);
    const fileElement = await screen.findByText('test.txt');
    expect(fileElement).toBeInTheDocument();
  });

  it('handles file upload', async () => {
    const mockHandleFileUpload = jest.fn().mockImplementation(async () => {});
    
    mockUseFileManager.mockReturnValue({
      files: [],
      error: "",
      loading: false,
      handleFileUpload: mockHandleFileUpload,
      deleteFile: jest.fn().mockImplementation(async () => {}),
    });

    render(<App />);
    // Additional upload testing logic here
  });
});