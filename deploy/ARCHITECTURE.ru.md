# Архитектура деплоя

## Структура

```
Browser
   ↓
Nginx (порты 80, 443)
   ├─→ /api/*      → FastAPI Server (порт 8080)
   └─→ /*          → Vue SPA (frontend/dist)
```

## Компоненты

### Nginx
- Слушает порты 80 (HTTP) и 443 (HTTPS)
- Редиректит HTTP → HTTPS
- Раздает статические файлы Vue из `/var/www/html` (смонтировано из `frontend/dist`)
- Проксирует `/api/*` запросы на FastAPI сервер
- Обрабатывает SSL сертификаты от Let's Encrypt

### Vue Frontend
- Собирается в `frontend/dist` командой `npm run build`
- Раздается напрямую через Nginx для максимальной производительности
- Использует client-side routing (Vue Router)
- При обращении к любому URL → возвращается `index.html`

### FastAPI Backend
- Работает на порту 8080 (только внутри Docker сети)
- Доступен извне только через Nginx по пути `/api/*`
- Обрабатывает API запросы
- Подключается к PostgreSQL

### Certbot
- Автоматически получает и обновляет SSL сертификаты
- Обновление каждые 12 часов

## Volumes (монтирование)

```yaml
nginx:
  - ./deploy/nginx/conf.d → /etc/nginx/conf.d       # Конфигурация Nginx
  - ./deploy/certbot/conf → /etc/letsencrypt        # SSL сертификаты
  - ./deploy/certbot/www → /var/www/certbot         # ACME challenge
  - ./frontend/dist → /var/www/html                 # Vue приложение
```

## Процесс деплоя

1. `git pull` - получение последнего кода
2. `npm run build` - сборка Vue фронтенда в `dist`
3. `docker compose build` - сборка Docker образов
4. `docker compose up -d` - запуск контейнеров
5. Nginx автоматически подхватывает новый `dist` через volume
6. `alembic upgrade head` - применение миграций БД

## Безопасность

- Порт 8080 (FastAPI) не открыт наружу
- Порт 5432 (PostgreSQL) не открыт наружу
- Доступ к API только через Nginx
- SSL сертификаты обновляются автоматически

## Логи

```bash
# Все логи
docker compose logs -f

# Только Nginx
docker compose logs -f nginx

# Только сервер
docker compose logs -f server
```
