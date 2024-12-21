module.exports = {
    preset: 'ts-jest',
    testEnvironment: 'jsdom',
    moduleNameMapper: {
      '^@/(.*)$': '<rootDir>/src/$1',
    },
    transform: {
      '^.+\\.(ts|tsx)$': 'ts-jest',
    },
    transformIgnorePatterns: [
      '/node_modules/(?!axios)/'
    ],
    setupFilesAfterEnv: ['<rootDir>/src/setupTests.ts']
  };