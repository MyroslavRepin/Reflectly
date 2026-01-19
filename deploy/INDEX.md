# Deploy Documentation Index

## Быстрый старт (для спешащих)

**[QUICKSTART.ru.md](QUICKSTART.ru.md)** - установка за 5 минут

## Основная документация

### На русском
- **[README.ru.md](README.ru.md)** - полная инструкция по деплою
- **[ARCHITECTURE.ru.md](ARCHITECTURE.ru.md)** - архитектура и схема работы
- **[TESTING.ru.md](TESTING.ru.md)** - тестирование и troubleshooting

### In English  
- **[README.md](README.md)** - full deployment guide

## Файлы конфигурации

```
deploy/
├── nginx/
│   └── conf.d/
│       └── reflectly.conf          # Конфигурация Nginx
├── certbot/
│   ├── conf/                       # SSL сертификаты (генерируются автоматически)
│   └── www/                        # ACME challenge
├── deploy.sh                       # Скрипт деплоя
└── .gitignore                      # Исключения для Git
```

## Быстрая навигация

### Первый раз разворачиваете?
1. Прочитайте [QUICKSTART.ru.md](QUICKSTART.ru.md)
2. Если нужны детали → [README.ru.md](README.ru.md)

### Хотите понять как это работает?
→ [ARCHITECTURE.ru.md](ARCHITECTURE.ru.md)

### Что-то не работает?
→ [TESTING.ru.md](TESTING.ru.md) - раздел Troubleshooting

### Уже настроили, нужно обновить?
```bash
./deploy/deploy.sh deploy
```

## Основные команды

```bash
# Первоначальная настройка (один раз)
./deploy/deploy.sh init

# Деплой/обновление
./deploy/deploy.sh deploy

# Просмотр логов
./deploy/deploy.sh logs

# Перезапуск
./deploy/deploy.sh restart

# Остановка
./deploy/deploy.sh stop
```

## Структура сервисов

```
Internet
   ↓
Nginx:80,443
   ├─→ /api/*  → FastAPI:8080
   └─→ /*      → Vue SPA (dist/)
```

## Требования

- Docker + Docker Compose
- Node.js >= 18.0.0
- Домен с A-записью на ваш VPS
- Открытые порты 80, 443

## Поддержка

При возникновении проблем:
1. Проверьте логи: `./deploy/deploy.sh logs`
2. См. раздел Troubleshooting в [TESTING.ru.md](TESTING.ru.md)
3. Проверьте статус: `docker compose ps`
