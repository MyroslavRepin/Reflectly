from authx import AuthX, AuthXConfig

from server.core.config import settings

config = AuthXConfig(
    JWT_ALGORITHM="HS256",
    JWT_SECRET_KEY=settings.jwt_secret_key,
    JWT_TOKEN_LOCATION=settings.jwt_token_location,
    JWT_ACCESS_TOKEN_EXPIRES=settings.jwt_access_token_expire_seconds,
    JWT_REFRESH_TOKEN_EXPIRES=False,
    JWT_ACCESS_COOKIE_NAME=settings.jwt_access_cookie_name,
    JWT_REFRESH_COOKIE_NAME=settings.jwt_refresh_cookie_name
)

auth = AuthX(config)

# auth.handle_errors(app)  # Register error handlers for proper responses
