#!/bin/bash

# Скрипт для деплоя Reflectly на VPS
# Использование: ./deploy.sh

set -e

echo "=== Деплой Reflectly ==="

# Проверка .env файла
if [ ! -f ../.env ]; then
    echo "Ошибка: файл .env не найден!"
    echo "Скопируйте .env.example в .env и заполните нужные значения"
    exit 1
fi

# Загрузка переменных окружения
export $(cat ../.env | grep -v '^#' | xargs)

# Проверка обязательных переменных
if [ -z "$DOMAIN" ]; then
    echo "Ошибка: DOMAIN не указан в .env"
    exit 1
fi

cd ..

# Выбор действия
case "${1:-deploy}" in
    "init")
        echo "=== Первоначальная настройка ==="

        # Запуск только nginx и certbot для получения сертификата
        echo "Запуск Nginx..."
        docker compose up -d nginx

        sleep 5

        # Получение SSL сертификата
        echo "Получение SSL сертификата для $DOMAIN..."
        docker compose run --rm certbot certonly \
            --webroot \
            --webroot-path=/var/www/certbot \
            --email $EMAIL \
            --agree-tos \
            --no-eff-email \
            -d $DOMAIN

        # Обновление конфига с реальным доменом
        sed -i.bak "s/YOUR_DOMAIN/$DOMAIN/g" deploy/nginx/conf.d/reflectly.conf
        rm -f deploy/nginx/conf.d/reflectly.conf.bak

        # Перезапуск nginx
        docker compose restart nginx

        echo "SSL сертификат получен! Теперь запустите: ./deploy/deploy.sh"
        ;;

    "deploy")
        echo "=== Обновление приложения ==="

        # Получение последних изменений
        if [ -d .git ]; then
            echo "Получение обновлений из Git..."
            git pull
        fi

        # Сборка Vue фронтенда
        echo "Сборка Vue фронтенда..."
        cd frontend
        if [ ! -d "node_modules" ]; then
            echo "Установка npm зависимостей..."
            npm install
        fi
        npm run build
        cd ..

        # Пересборка и перезапуск
        echo "Пересборка контейнеров..."
        docker compose build

        echo "Запуск сервисов..."
        docker compose up -d

        # Ожидание запуска БД
        echo "Ожидание БД..."
        sleep 10

        # Миграции
        echo "Применение миграций..."
        docker compose exec -T server uv run alembic upgrade head

        echo "=== Деплой завершен! ==="
        docker compose ps
        ;;

    "logs")
        docker compose logs -f "${2:-server}"
        ;;

    "restart")
        docker compose restart "${2:-server}"
        ;;

    "stop")
        docker compose down
        ;;

    *)
        echo "Использование:"
        echo "  ./deploy.sh init     - Первоначальная настройка и получение SSL"
        echo "  ./deploy.sh deploy   - Деплой/обновление приложения (по умолчанию)"
        echo "  ./deploy.sh logs     - Просмотр логов"
        echo "  ./deploy.sh restart  - Перезапуск сервисов"
        echo "  ./deploy.sh stop     - Остановка всех сервисов"
        exit 1
        ;;
esac
