FROM node:22-alpine
LABEL maintainer="B24Sdk <github.com/bitrix24>"

RUN apk add --no-cache openssl

WORKDIR /usr/src/app

RUN corepack enable

# Копируем package.json и package-lock.json
COPY .npmrc .nuxtrc package.json pnpm-lock.yaml pnpm-workspace.yaml ./
COPY docs/package.json ./docs/
COPY playgrounds/demo/package.json ./playgrounds/demo/
COPY playgrounds/nuxt/package.json ./playgrounds/nuxt/
COPY playgrounds/vue/package.json ./playgrounds/vue/
COPY docs/.output ./docs/.output/

# Устанавливаем зависимости для production
RUN pnpm install --prod --frozen-lockfile

# Создаем не-root пользователя для безопасности
RUN addgroup -g 1001 -S nodejs
RUN adduser -S nuxtuser -u 1001

# Меняем владельца файлов
RUN chown -R nuxtuser:nodejs /usr/src/app

# Переключаемся на не-root пользователя
USER nuxtuser

EXPOSE 80

# Запускаем серверную чать
CMD ["node", "/usr/src/app/docs/.output/server/index.mjs"]
