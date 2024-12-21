// src/App.test.tsx
import { screen, waitFor } from '@testing-library/react';
import { render } from './test-utils';
import App from './App';
import { useFileManager } from './hooks/useFileManager';

jest.mock('./hooks/useFileManager');
const mockUseFileManager = useFileManager as jest.MockedFunction<typeof useFileManager>;

describe('App Component', () => {
  beforeEach(() => {
    jest.clearAllMocks();
    
    // Suppress React 18 console errors/warnings
    jest.spyOn(console, 'error').mockImplementation(() => {});
    
    mockUseFileManager.mockReturnValue({
      files: [],
      error: null,
      loading: false,
      handleFileUpload: jest.fn(),
      deleteFile: jest.fn(),
      fetchFiles: jest.fn()
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
    const mockFiles = [
      {
        id: 1,
        name: 'test.txt',
        size: '1.5',
        uploadDate: '2024-12-21'
      }
    ];

    mockUseFileManager.mockReturnValue({
      files: mockFiles,
      error: null,
      loading: false,
      handleFileUpload: jest.fn(),
      deleteFile: jest.fn(),
      fetchFiles: jest.fn()
    });

    render(<App />);
    const fileElement = await screen.findByText('test.txt');
    expect(fileElement).toBeInTheDocument();
  });
});