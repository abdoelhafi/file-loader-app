export const API_CONFIG = {
    baseURL: process.env.FRONTEND_URL || 'http://localhost:8000/api',
    timeout: 10000,
    headers: {
      'Content-Type': 'application/json',
    },
  } as const;