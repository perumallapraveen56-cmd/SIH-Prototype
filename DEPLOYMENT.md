# SIH26017 Production Deployment Guide
**Smart India Hackathon (SIH 2026)**  
**Team**: NEXORA_TAU  
**Project**: Predictive Analytics System for Early Detection of Land Acquisition Delays  

---

## 🏗️ 1. Architecture Overview

```
                      [ Internet / User Browsers ]
                                   │
                                   ▼ HTTPS (443)
                      ┌──────────────────────────┐
                      │    Nginx Reverse Proxy   │
                      │  (SSL Termination & gzip)│
                      └─────────────┬────────────┘
                                    │
            ┌───────────────────────┴───────────────────────┐
            │ / (Static assets)                             │ /api/* (API Reverse Proxy)
            ▼                                               ▼
┌──────────────────────────┐                   ┌──────────────────────────┐
│  Angular 21 SPA Bundle   │                   │    FastAPI Application   │
│  (Nginx Static Hosting)  │                   │    (Uvicorn / Gunicorn)  │
└──────────────────────────┘                   └────────────┬─────────────┘
                                                            │
                                                            ▼ PostgreSQL (5432)
                                               ┌──────────────────────────┐
                                               │   PostgreSQL Database    │
                                               │ (or SQLite fallback.db)  │
                                               └──────────────────────────┘
```

---

## ⚙️ 2. Environment Variables Configuration

Copy `.env.example` to `.env` in the production environment:

```bash
cp .env.example .env
```

Set the production parameters:

| Variable | Recommended Production Value | Description |
|---|---|---|
| `HOST` | `0.0.0.0` | Listen host for backend server |
| `PORT` | `8000` | Port for backend server |
| `ENVIRONMENT` | `production` | Enables production error filtering |
| `LOG_LEVEL` | `info` | Production logging level |
| `DATABASE_URL` | `postgresql+psycopg2://<USER>:<PASS>@<HOST>:5432/<DB>` | Production PostgreSQL connection URI |
| `SQLITE_FALLBACK_URL` | `sqlite:///./land_acquisition.db` | Local fallback database if Postgres unavailable |
| `SECRET_KEY` | `$(openssl rand -hex 32)` | 256-bit cryptographic signing secret for JWT tokens |
| `ALGORITHM` | `HS256` | JWT signing algorithm |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | `1440` | Session lifetime (24 hours) |
| `CORS_ORIGINS` | `https://your-domain.gov.in,https://app.your-domain.gov.in` | Explicit allowed frontend origins |

---

## 🐳 3. Containerized Deployment (Docker Compose)

The repository provides production-ready Docker configurations:
- `Dockerfile.backend` (Multi-stage Python 3.13 image)
- `Dockerfile.frontend` (Multi-stage Node.js build + Nginx alpine)
- `docker-compose.yml` (Orchestrates PostgreSQL, FastAPI Backend, and Angular Frontend)

### Deploy with Docker Compose:

```bash
# 1. Clone repository
git clone https://github.com/<AUTHORIZED_OWNER>/<REPO_NAME>.git
cd SIH26017

# 2. Configure production secrets in .env
cp .env.example .env
nano .env

# 3. Build and launch services in detached mode
docker compose up -d --build

# 4. Verify service health
docker compose ps
curl http://localhost:8000/api/health
```

---

## 💻 4. Bare-Metal / Virtual Private Server (VPS) Deployment

### Step A: Build Frontend

```bash
cd frontend
npm ci
npm run build
# Production files generated in: frontend/dist/frontend
```

### Step B: Setup Python Backend as Systemd Service

```ini
# /etc/systemd/system/sih26017-backend.service
[Unit]
Description=SIH26017 Land Acquisition Delay Prediction API
After=network.target postgresql.service

[Service]
User=www-data
Group=www-data
WorkingDirectory=/var/www/sih26017/backend
EnvironmentFile=/var/www/sih26017/.env
ExecStart=/var/www/sih26017/backend/.venv/bin/gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
```

Enable and start the service:
```bash
sudo systemctl daemon-reload
sudo systemctl enable sih26017-backend
sudo systemctl start sih26017-backend
```

### Step C: Nginx Reverse Proxy Configuration

```nginx
# /etc/nginx/sites-available/sih26017
server {
    listen 80;
    server_name sih26017.yourdomain.gov.in;

    # Redirect all HTTP to HTTPS
    return 301 https://$host$request_uri;
}

server {
    listen 443 ssl http2;
    server_name sih26017.yourdomain.gov.in;

    ssl_certificate /etc/letsencrypt/live/sih26017.yourdomain.gov.in/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/sih26017.yourdomain.gov.in/privkey.pem;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;

    # Angular SPA Frontend
    location / {
        root /var/www/sih26017/frontend/dist/frontend;
        index index.html;
        try_files $uri $uri/ /index.html;
    }

    # FastAPI Backend Reverse Proxy
    location /api/ {
        proxy_pass http://127.0.0.1:8000/api/;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_read_timeout 90;
    }

    # Swagger / OpenAPI documentation (Optional in production)
    location /docs {
        proxy_pass http://127.0.0.1:8000/docs;
    }
}
```

---

## 🔒 5. Security Checklist Before Launch

- [x] Environment files (`.env`) are excluded from version control via `.gitignore`.
- [x] Production JWT `SECRET_KEY` is generated randomly with high entropy (`openssl rand -hex 32`).
- [x] Database credentials are restricted to private network / localhost only.
- [x] Production CORS headers are restricted to authorized domains.
- [x] Global exception handler returns generic errors without stack traces.
- [x] HTTPS enforced with HTTP Strict Transport Security (HSTS).
