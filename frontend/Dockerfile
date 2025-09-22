#Dockerfile для React фронтенда
FROM node:18-alpine as build

WORKDIR /app

#Копируем package.json и package-lock.json
COPY package*.json ./

#Устанавливаем зависимости
RUN npm ci --only=production

#Копируем исходный код
COPY . .

#Собираем приложение
RUN npm run build

#Стадия production
FROM nginx:alpine

#Копируем собранное приложение в nginx
COPY --from=build /app/build /usr/share/nginx/html

COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]