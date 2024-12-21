export class FileService {
    async uploadFile(file: File) {
      return {
        id: 1,
        name: file.name,
        size: '1.5',
        uploadDate: '2024-12-21'
      };
    }
  
    async getFiles() {
      return [
        {
          id: 1,
          name: 'test.txt',
          size: '1.5',
          uploadDate: '2024-12-21'
        }
      ];
    }
  
    async deleteFile(id: number) {
      return true;
    }
  }
  
  export const fileService = new FileService();