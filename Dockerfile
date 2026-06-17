FROM node:20-alpine

# Install build dependencies for compiling native node modules if needed
RUN apk add --no-cache python3 make g++

WORKDIR /usr/src/app

# Copy package configuration
COPY package.json ./

# Install dependencies
RUN npm install

# Copy project files
COPY . .

# Build TypeScript code
RUN npm run build

# Expose ports
EXPOSE 3000
EXPOSE 5001

# Automatically populate data on first boot, then start the server
CMD ["sh", "-c", "npm run populate || echo 'Database already populated or error ignored' && npm run start"]
