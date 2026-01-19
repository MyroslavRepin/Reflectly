# Quick Start - Деплой на VPS

## Быстрая установка (5 минут)

### 1. Подготовка VPS
```bash
# Установка Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER
newgrp docker

# Установка Node.js (для сборки Vue фронтенда)
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt-get install -y nodejs
```

### 2. Клонирование проекта
```bash
cd ~
git clone <ваш-репозиторий>
cd Reflectly
```

### 3. Настройка
```bash
cp .env.example .env
nano .env
```

Измените:
```env
DOMAIN=вашдомен.ru
EMAIL=ваш@email.com
POSTGRES_PASSWORD=СИЛЬНЫЙ_ПАРОЛЬ
DATABASE_URL=postgresql+asyncpg://reflectly_user:СИЛЬНЫЙ_ПАРОЛЬ@db:5432/reflectly
JWT_SECRET_KEY=СЛУЧАЙНАЯ_СТРОКА_64_СИМВОЛА
```

Генерация секрета:
```bash
openssl rand -hex 32
```

### 4. Запуск
```bash
# Первый раз: получение SSL
chmod +x deploy/deploy.sh
./deploy/deploy.sh init

# Деплой приложения
./deploy/deploy.sh deploy
```

### 5. Проверка
```bash
# Статус
docker compose ps

# Логи
./deploy/deploy.sh logs

# Открыть в браузере
https://вашдомен.ru
```

## Управление

```bash
./deploy/deploy.sh deploy    # Обновить приложение
./deploy/deploy.sh logs      # Логи
./deploy/deploy.sh restart   # Перезапуск
./deploy/deploy.sh stop      # Остановка
```

## Firewall

```bash
sudo ufw allow 22/tcp
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw enable
```

## Бэкап БД

```bash
docker compose exec db pg_dump -U reflectly_user reflectly > backup.sql
```

## Проблемы?

См. [deploy/README.ru.md](README.ru.md)
