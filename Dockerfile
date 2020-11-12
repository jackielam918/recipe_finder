FROM node:latest

COPY ./web-app /home/web-app
WORKDIR /home/web-app

RUN npm install && npm run build