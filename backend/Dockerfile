# Add the necessary commands to create a Docker image for the backend service

FROM node:20-alpine

RUN mkdir -p /app
WORKDIR /app

COPY ./ ./

RUN npm install
RUN npx prisma generate
RUN npm run build

EXPOSE 7000

CMD ["npm", "run", "start:prod"]

