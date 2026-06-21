# Use Node.js base image
FROM node:18-alpine

# Set the working directory
WORKDIR /app

# Copy package files and install dependencies
COPY package*.json ./
RUN npm install

# Copy the rest of the frontend code
COPY . .

# Expose the port used by Vite
EXPOSE 5173

# Run the development server
CMD ["npm", "run", "dev", "--", "--host"]