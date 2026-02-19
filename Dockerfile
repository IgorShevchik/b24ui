# ---- этап сборки ----
FROM node:22-alpine AS builder

RUN apk add --no-cache openssl
RUN corepack enable

WORKDIR /app

# Копируем все файлы манифестов для кэширования зависимостей
COPY package.json pnpm-lock.yaml pnpm-workspace.yaml ./
COPY docs/package.json ./docs/
COPY playgrounds/nuxt/package.json ./playgrounds/nuxt/
COPY playgrounds/vue/package.json ./playgrounds/vue/
COPY playgrounds/demo/package.json ./playgrounds/demo/
COPY cli/package.json ./cli/

# Устанавливаем ВСЕ зависимости (включая dev)
RUN pnpm install --frozen-lockfile

# Теперь копируем остальные исходники (кроме node_modules, которые уже установлены)
COPY . .

# Готовим
RUN pnpm run dev:prepare

# Собираем локальный модуль (скрипт build в корневом package.json)
RUN pnpm run build

# Собираем документацию
RUN pnpm run docs:build

# ---- финальный образ ----
FROM node:22-alpine

RUN apk add --no-cache openssl
RUN corepack enable

WORKDIR /usr/src/app

# Копируем только собранный .output документации
COPY --from=builder /app/docs/.output ./docs/.output

# Создаём непривилегированного пользователя
RUN addgroup -g 1001 -S nodejs && adduser -S nuxtuser -u 1001
RUN chown -R nuxtuser:nodejs /usr/src/app
USER nuxtuser

EXPOSE 80
CMD ["node", "docs/.output/server/index.mjs"]
