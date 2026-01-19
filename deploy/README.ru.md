# Деплой на VPS

> **Быстрый старт:** [QUICKSTART.ru.md](QUICKSTART.ru.md) - установка за 5 минут

Быстрая инструкция по деплою Reflectly на VPS с Nginx и SSL.

## Что нужно

- VPS с установленными Docker и Docker Compose
- Node.js >= 18.0.0 (для сборки Vue фронтенда)
- Домен, направленный на IP вашего VPS
- Открытые порты 80 и 443

## Быстрый старт

### 1. Клонирование и настройка

```bash
git clone <ваш-репозиторий>
cd Reflectly
cp .env.example .env
nano .env
```

Заполните в `.env`:
```env
DOMAIN=вашдомен.ru
EMAIL=ваш@email.com
POSTGRES_PASSWORD=сильный_пароль
DATABASE_URL=postgresql+asyncpg://reflectly_user:сильный_пароль@db:5432/reflectly
```

### 2. Получение SSL сертификата

```bash
chmod +x deploy/deploy.sh
./deploy/deploy.sh init
```

Это запустит Nginx и получит SSL сертификат от Let's Encrypt.

### 3. Запуск приложения

```bash
./deploy/deploy.sh deploy
```

Готово! Приложение доступно по адресу `https://вашдомен.ru`

## Команды

```bash
# Деплой/обновление
./deploy/deploy.sh deploy

# Просмотр логов
./deploy/deploy.sh logs
./deploy/deploy.sh logs nginx

# Перезапуск
./deploy/deploy.sh restart

# Остановка
./deploy/deploy.sh stop
```

## Структура

```
deploy/
├── nginx/conf.d/reflectly.conf  # Конфигурация Nginx
├── certbot/                     # SSL сертификаты
├── deploy.sh                    # Скрипт деплоя
└── README.md                    # Документация (English)
```

## Проблемы?

**Не получается SSL:**
```bash
dig вашдомен.ru +short  # Проверьте DNS
docker compose logs nginx
```

**502 Bad Gateway:**
```bash
docker compose logs server
```

**База не подключается:**
```bash
docker compose exec db psql -U reflectly_user reflectly
```

## Безопасность

- Никогда не коммитьте `.env` в Git
- Используйте сильные пароли
- Регулярно обновляйте Docker образы
- Настройте бэкапы БД

Подробная документация на английском: `deploy/README.md`
