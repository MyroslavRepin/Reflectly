# API Configuration Setup

## Overview

The Vue.js application uses environment-based API URL configuration controlled by a single `.env` file in the project root. The configuration automatically switches between development and production API endpoints. Each component manages its own axios instances using the API_BASE_URL from the config.

## Environment Variables

### VITE_FRONTEND_ENV

Controls which API endpoint is used by the application.

- **dev** (development): `http://localhost:8080/api/v1`
- **prod** (production): `https://reflectly.myroslavrepin.com/api/v1`

## Setup Instructions

### Development Setup

1. Ensure `.env` file in project root contains:
   ```
   VITE_FRONTEND_ENV=dev
   ```

2. Start the development server:
   ```bash
   cd frontend
   npm run dev
   ```

3. The backend API should be running on `http://localhost:8080`

### Production Build

1. Update `.env` file:
   ```
   VITE_FRONTEND_ENV=prod
   ```

2. Build the application:
   ```bash
   cd frontend
   npm run build
   ```

3. The compiled application in `/dist` will use the production API URL

## File Structure

```
frontend/
├── src/
│   ├── config/
│   │   └── api.js           # API configuration based on environment
│   ├── components/
│   │   ├── LoginPage.vue    # Uses axios with API_BASE_URL from config
│   │   ├── SignupPage.vue   # Uses axios with API_BASE_URL from config
│   │   ├── DashboardTimerSection.vue  # Uses axios with API_BASE_URL from config
│   │   └── DashboardEntries.vue       # Uses axios with API_BASE_URL from config
│   └── main.js
├── vite.config.js           # Updated with @ alias for imports
└── package.json
```

## Configuration Files

### frontend/src/config/api.js

Exports environment-based API configuration:

```javascript
export const FRONTEND_ENV = import.meta.env.VITE_FRONTEND_ENV || 'dev';
export const API_BASE_URL = getApiBaseUrl();
export const IS_DEV = FRONTEND_ENV === 'dev';
export const IS_PROD = FRONTEND_ENV === 'prod';
```

## Usage in Components

Each component imports the `API_BASE_URL` from the config and uses it directly with axios:

```javascript
import axios from 'axios';
import { API_BASE_URL } from '@/config/api';

// Use the API_BASE_URL in axios calls
const response = await axios.get(`${API_BASE_URL}/timer/`, {
  headers: {
    'Content-Type': 'application/json'
  },
  withCredentials: true,
});
```

## Development Logging

When `VITE_FRONTEND_ENV=dev`, the console displays:
```javascript
API Configuration: {
  FRONTEND_ENV: 'dev',
  API_BASE_URL: 'http://localhost:8080/api/v1',
  IS_DEV: true,
  IS_PROD: false
}
```

This helps verify which API endpoint is being used.

## Updated Components

All components have been updated to use axios directly with `API_BASE_URL` from config:

### LoginPage.vue
- Endpoint: `POST /auth/login`
- Usage: `axios.post(\`${API_BASE_URL}/auth/login\`, ...)`

### SignupPage.vue
- Endpoint: `POST /auth/signup`
- Usage: `axios.post(\`${API_BASE_URL}/auth/signup\`, ...)`

### DashboardTimerSection.vue
- Endpoints: `GET /timer/current`, `POST /timer/start`, `POST /timer/stop`
- Usage: `axios.get(\`${API_BASE_URL}/timer/current\`, ...)`

### DashboardEntries.vue
- Endpoint: `GET /timer/`
- Usage: `axios.get(\`${API_BASE_URL}/timer/\`, ...)`

## Verification

To verify the setup is working:

1. Check console on app load:
   ```javascript
   API Configuration: { FRONTEND_ENV: 'dev', API_BASE_URL: 'http://localhost:8080/api/v1', ... }
   ```

2. Check for remaining hardcoded URLs:
   ```bash
   grep -r "localhost:8080" frontend/src/components/
   # Should return no results (only in config/api.js)
   
   grep -r "reflectly.myroslavrepin.com" frontend/src/components/
   # Should return no results (only in config/api.js)
   ```

3. Test in browser DevTools Network tab:
   - Requests should go to correct API endpoint based on VITE_FRONTEND_ENV

## Switching Environments

To switch from dev to prod:

1. Edit `.env`:
   ```
   VITE_FRONTEND_ENV=prod
   ```

2. For development: No rebuild needed, reload page in browser
3. For production: Run `npm run build` to create optimized dist folder

## Vite Configuration

The `vite.config.js` includes:
- `envDir: path.resolve(__dirname, '..')` - Reads `.env` from project root
- `resolve.alias: { '@': './src' }` - Enables @/ imports for clean imports

## Troubleshooting

### API requests to wrong URL
- Verify VITE_FRONTEND_ENV value in `.env`
- Check API Configuration log in console on app load
- Ensure frontend dev server is restarted after changing `.env`

### Import errors with @/
- Verify vite.config.js has `resolve.alias` configured
- Clear browser cache and rebuild: `npm run build`

### Network errors
- Verify backend API is running on the correct endpoint
- Check browser DevTools Network tab for actual request URLs
