FROM node:20-alpine
WORKDIR /app
COPY package.json tsconfig.json next-env.d.ts next.config.js ./
RUN npm install
COPY app ./app
COPY components ./components
ENV NEXT_PUBLIC_API_URL=http://localhost:8000
CMD ["npm", "run", "dev"]
