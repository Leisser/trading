# Use Node.js 20 Alpine as base image
FROM node:20-alpine

# Set working directory
WORKDIR /app

# Copy package files
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy source code
COPY . .

# Clean any existing build cache and build the Next.js application
RUN rm -rf .next && npm run build

# Copy static files and public assets to the correct location for standalone
RUN cp -r .next/static .next/standalone/.next/static
RUN cp -r public .next/standalone/public

# Expose port 5173
EXPOSE 5173

# Set environment variables
ENV PORT=5173
ENV NODE_ENV=production

# Start the application using standalone server
CMD ["node", ".next/standalone/server.js"]
