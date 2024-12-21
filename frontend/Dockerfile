# Use Node.js LTS version
FROM node:20-slim

# Set working directory
WORKDIR /app

# Set build arguments
ARG FRONTEND_URL
ENV FRONTEND_URL=$FRONTEND_URL

# Copy package files
COPY package*.json ./

# Install dependencies with legacy peer deps to handle conflicts
RUN npm install --legacy-peer-deps

# Copy project files
COPY . .

# Expose port
EXPOSE 3000

# Start the app
CMD ["npm", "start"]