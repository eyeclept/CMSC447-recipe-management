# dockerfile

FROM node:18-alpine

WORKDIR /usr/src/app

COPY reactapp/package*.json ./


RUN npm install

COPY . .

# Build the React application
RUN npm run build

# Expose the port the app runs on
EXPOSE 3000

# Command to run the app
CMD ["npm", "start"]
