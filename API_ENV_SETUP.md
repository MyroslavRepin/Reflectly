# API Environment Setup Documentation

## Overview
All Vue components now use environment variables to access API endpoints instead of hardcoded URLs. This allows for easy configuration across different environments (development, production, etc.).

## Environment Configuration

### Global `.env` File (Root Directory)
Located at `/Users/myroslavrepin/Documents/Development/Projects/Reflectly/.env`

```dotenv
# API URLs
VITE_API_URL=http://localhost:8080/api/v1          # Development
VITE_API_BASE_URL=https://reflectly.myroslavrepin.com/api/v1  # Production
```

## Updated Vue Components

All Vue components now use `import.meta.env.VITE_API_BASE_URL` to fetch the API base URL at runtime.

### 1. LoginPage.vue
- **Function**: `sendLoginRequest()`
- **Endpoint**: `${apiBaseUrl}/auth/login`
- **Change**: Replaced hardcoded URL with environment variable

### 2. SignupPage.vue
- **Function**: `sendSignupRequest()`
- **Endpoint**: `${apiBaseUrl}/auth/signup`
- **Change**: Replaced hardcoded URL with environment variable

### 3. DashboardEntries.vue
- **Variable**: `serverUrl`
- **Endpoint**: `${apiBaseUrl}/timer/`
- **Change**: Replaced hardcoded URL with environment variable

### 4. DashboardTimerSection.vue
- **Function**: `initTimerFromApi()`
  - **Endpoint**: `${apiBaseUrl}/timer/current`
  
- **Function**: `startTimerRequest()`
  - **Endpoint**: `${apiBaseUrl}/timer/start`
  
- **Function**: `stopTimerRequest()`
  - **Endpoint**: `${apiBaseUrl}/timer/stop`

- **Change**: All functions now read API base URL from environment variables

## Vite Configuration

### vite.config.js
Updated to load `.env` from parent directory:

```javascript
envDir: path.resolve(__dirname, '..')
```

This allows Vite to read environment variables from `/Users/myroslavrepin/Documents/Development/Projects/Reflectly/.env`

## Build and Deployment

### Development Build
```bash
cd frontend
npm run dev
```
- Uses `VITE_API_URL` or `VITE_API_BASE_URL` from `.env`
- Development server proxies `/api` requests to `http://localhost:8080`

### Production Build
```bash
cd frontend
npm run build
```
- Uses `VITE_API_BASE_URL` from `.env` (set to production URL)
- Built files are in `frontend/dist/`
- All API calls go directly to the production domain

## Configuration Changes

To change the API endpoint for different environments:

1. **Local Development**: Set in `.env`
   ```
   VITE_API_BASE_URL=http://localhost:8080/api/v1
   ```

2. **Production**: Set in `.env`
   ```
   VITE_API_BASE_URL=https://reflectly.myroslavrepin.com/api/v1
   ```

3. **Other Domains**: Modify `.env` accordingly
   ```
   VITE_API_BASE_URL=https://your-custom-domain.com/api/v1
   ```

Then rebuild:
```bash
npm run build
```

## How It Works

1. When the frontend builds, Vite reads the `.env` file from the root directory
2. The variable `VITE_API_BASE_URL` is embedded into the JavaScript bundle
3. At runtime, Vue components access it via `import.meta.env.VITE_API_BASE_URL`
4. All API requests use this URL dynamically

## API Endpoints Structure

All endpoints follow this pattern:
```
${VITE_API_BASE_URL}/[service]/[action]
```

### Available Endpoints
- `POST ${VITE_API_BASE_URL}/auth/login` - Login
- `POST ${VITE_API_BASE_URL}/auth/signup` - Registration
- `GET ${VITE_API_BASE_URL}/timer/current` - Get current timer state
- `POST ${VITE_API_BASE_URL}/timer/start` - Start timer
- `POST ${VITE_API_BASE_URL}/timer/stop` - Stop timer
- `GET ${VITE_API_BASE_URL}/timer/` - Get all entries

## Notes

- Environment variables must start with `VITE_` to be accessible in the frontend
- The `.env` file should NOT be committed to version control (already in `.gitignore`)
- When deploying to `/dist`, ensure the `.env` file is updated with the correct production URL before building
