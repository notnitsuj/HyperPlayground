FROM node:18-alpine

WORKDIR /app

COPY package.json yarn.lock* package-lock.json* pnpm-lock.yaml* ./

RUN ["npm", "install"]

COPY . .

CMD ["npm", "run", "dev"]