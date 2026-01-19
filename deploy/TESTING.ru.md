# Тестирование деплоя

## Локальное тестирование

### 1. Сборка фронтенда
```bash
cd frontend
npm install
npm run build
ls -la dist/
```

Должны увидеть:
- `index.html`
- `assets/` (с .js и .css файлами)

### 2. Проверка Docker Compose конфигурации
```bash
docker compose config
```

### 3. Запуск локально (без SSL)
```bash
# Временно закомментируйте HTTPS server в nginx конфиге
# Оставьте только HTTP redirect

docker compose up -d nginx server

# Проверка
curl http://localhost/
curl http://localhost/api/
```

## После деплоя на VPS

### 1. Проверка DNS
```bash
dig вашдомен.ru +short
# Должен вернуть IP вашего VPS
```

### 2. Проверка портов
```bash
# На VPS
sudo netstat -tulpn | grep -E ':(80|443)'
# Должны быть открыты 80 и 443
```

### 3. Проверка контейнеров
```bash
docker compose ps
# Все контейнеры должны быть UP
```

### 4. Проверка Nginx конфигурации
```bash
docker compose exec nginx nginx -t
# Должно быть: syntax is ok, test is successful
```

### 5. Проверка логов
```bash
# Nginx логи
docker compose logs nginx --tail=50

# Server логи
docker compose logs server --tail=50

# Если ошибки
docker compose logs --tail=100
```

### 6. Проверка SSL сертификата
```bash
# На VPS
sudo ls -la deploy/certbot/conf/live/вашдомен.ru/

# Должны быть файлы:
# - fullchain.pem
# - privkey.pem
# - chain.pem
# - cert.pem
```

### 7. Проверка работы сайта
```bash
# HTTP → HTTPS redirect
curl -I http://вашдомен.ru
# Должен быть: Location: https://вашдомен.ru/

# HTTPS работает
curl -I https://вашдомен.ru
# Должен быть: 200 OK

# API работает
curl https://вашдомен.ru/api/
```

### 8. Проверка в браузере
1. Откройте `https://вашдомен.ru`
2. Проверьте SSL сертификат (замочек в адресной строке)
3. Откройте Dev Tools → Network
4. Проверьте, что статика загружается с вашего домена
5. Проверьте, что API запросы идут на `/api/*`

## Troubleshooting

### Nginx не стартует
```bash
docker compose logs nginx
docker compose exec nginx nginx -t
```

### 502 Bad Gateway
```bash
# Проверить, что server запущен
docker compose ps server

# Проверить логи сервера
docker compose logs server

# Проверить сеть
docker network inspect reflectly_reflectly
```

### Статика не отдается
```bash
# Проверить, что dist собран
ls -la frontend/dist/

# Проверить mount в контейнере
docker compose exec nginx ls -la /var/www/html/

# Должны быть файлы из dist
```

### SSL не работает
```bash
# Проверить сертификаты
docker compose exec nginx ls -la /etc/letsencrypt/live/

# Перезапустить nginx
docker compose restart nginx

# Проверить логи certbot
docker compose logs certbot
```

## Полезные команды

```bash
# Перезапуск всего
docker compose restart

# Только nginx
docker compose restart nginx

# Пересборка и перезапуск
docker compose up -d --build

# Остановка всего
docker compose down

# Очистка всего (ОСТОРОЖНО!)
docker compose down -v
```
