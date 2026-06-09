# GoCart Deployment Guide

**GoCart** | *Shop Smarter. Shop Faster.*

---

## 1. Docker Compose (Local / VPS)

### Prerequisites
- Docker & Docker Compose
- Copy `backend/.env.example` to `backend/.env` and configure

### Steps

```bash
# Clone and configure
cp backend/.env.example backend/.env
# Edit backend/.env with your secrets

# Start all services
docker compose up -d --build

# Run migrations and seed data
docker compose exec backend python manage.py migrate
docker compose exec backend python manage.py seed_data

# Access
# Frontend: http://localhost (via Nginx) or http://localhost:5173
# API: http://localhost/api/v1/
# Swagger: http://localhost/api/docs/
# Admin: http://localhost/admin/
```

### Services
| Service | Port | Description |
|---------|------|-------------|
| nginx | 80 | Reverse proxy |
| backend | 8000 | Django API |
| frontend | 5173 | React SPA |
| db | 5432 | PostgreSQL |
| redis | 6379 | Cache + Celery broker |
| celery | - | Background tasks |

---

## 2. Render

### Backend (Web Service)

1. Create **PostgreSQL** database on Render
2. Create **Redis** instance (or use Upstash Redis URL)
3. Create **Web Service** from GitHub repo:
   - **Root Directory**: `backend`
   - **Build Command**: `pip install -r requirements.txt && python manage.py collectstatic --noinput`
   - **Start Command**: `gunicorn config.wsgi:application --bind 0.0.0.0:$PORT`
4. Environment variables:

```
SECRET_KEY=<generate-strong-key>
DEBUG=False
ALLOWED_HOSTS=your-app.onrender.com
DB_NAME=<from-render-postgres>
DB_USER=<from-render-postgres>
DB_PASSWORD=<from-render-postgres>
DB_HOST=<from-render-postgres>
DB_PORT=5432
REDIS_URL=<redis-url>
CORS_ALLOWED_ORIGINS=https://your-frontend.onrender.com
FRONTEND_URL=https://your-frontend.onrender.com
RAZORPAY_KEY_ID=<your-key>
RAZORPAY_KEY_SECRET=<your-secret>
```

5. Create **Background Worker** for Celery:
   - Start Command: `celery -A config worker -l info`

### Frontend (Static Site)

1. Create **Static Site**:
   - **Root Directory**: `frontend`
   - **Build Command**: `npm install && npm run build`
   - **Publish Directory**: `dist`
2. Environment:
```
VITE_API_URL=https://your-backend.onrender.com/api/v1
VITE_RAZORPAY_KEY_ID=<your-key>
```

---

## 3. Railway

### Backend

1. New Project → Deploy from GitHub
2. Add **PostgreSQL** and **Redis** plugins
3. Set service root to `backend`
4. Railway auto-detects Dockerfile or use:

```bash
pip install -r requirements.txt
python manage.py migrate
gunicorn config.wsgi:application --bind 0.0.0.0:$PORT
```

5. Reference variables: `${{Postgres.*}}`, `${{Redis.REDIS_URL}}`

### Frontend

1. Add second service with root `frontend`
2. Use Dockerfile or Nixpacks with `npm run build`
3. Set `VITE_API_URL` to backend Railway URL

### Celery Worker

Add worker service:
- Start: `celery -A config worker -l info`
- Same env vars as backend

---

## 4. AWS EC2

### Instance Setup (Ubuntu 22.04)

```bash
# SSH into EC2
ssh -i your-key.pem ubuntu@<ec2-ip>

# Install Docker
sudo apt update && sudo apt install -y docker.io docker-compose-plugin git
sudo usermod -aG docker ubuntu

# Clone repo
git clone <your-repo-url> gocart && cd gocart
cp backend/.env.example backend/.env
nano backend/.env  # Set production values

# Launch
docker compose up -d --build
docker compose exec backend python manage.py migrate
docker compose exec backend python manage.py seed_data
```

### Security Group
| Type | Port | Source |
|------|------|--------|
| HTTP | 80 | 0.0.0.0/0 |
| HTTPS | 443 | 0.0.0.0/0 |
| SSH | 22 | Your IP |

### SSL with Certbot

```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d yourdomain.com
```

### S3 for Media (optional)

```
AWS_ACCESS_KEY_ID=
AWS_SECRET_ACCESS_KEY=
AWS_STORAGE_BUCKET_NAME=gocart-media
```

Use `django-storages` for production media uploads.

---

## 5. Vercel (Frontend Only)

Vercel hosts the React frontend. Backend must be deployed separately (Render/Railway/EC2).

### Steps

1. Import GitHub repo in Vercel
2. Set **Root Directory** to `frontend`
3. Framework Preset: **Vite**
4. Environment Variables:

```
VITE_API_URL=https://your-backend-url.com/api/v1
VITE_RAZORPAY_KEY_ID=rzp_live_xxx
```

5. `vercel.json` (optional):

```json
{
  "rewrites": [{ "source": "/(.*)", "destination": "/index.html" }]
}
```

6. Deploy → Vercel provides `https://gocart.vercel.app`

### CORS
Add Vercel URL to backend `CORS_ALLOWED_ORIGINS`:
```
CORS_ALLOWED_ORIGINS=https://gocart.vercel.app
```

---

## Monitoring Setup

### Sentry
```
SENTRY_DSN=https://xxx@sentry.io/xxx
SENTRY_ENVIRONMENT=production
```

### Prometheus + Grafana

Metrics available at `/metrics` (django-prometheus).

```yaml
# Add to docker-compose.yml
prometheus:
  image: prom/prometheus
  volumes:
    - ./monitoring/prometheus.yml:/etc/prometheus/prometheus.yml
  ports:
    - "9090:9090"

grafana:
  image: grafana/grafana
  ports:
    - "3000:3000"
```

`monitoring/prometheus.yml`:
```yaml
scrape_configs:
  - job_name: 'gocart'
    static_configs:
      - targets: ['backend:8000']
    metrics_path: '/metrics'
```

---

## Production Checklist

- [ ] `DEBUG=False`
- [ ] Strong `SECRET_KEY`
- [ ] HTTPS enabled
- [ ] CORS origins restricted
- [ ] Razorpay live keys configured
- [ ] Email SMTP configured
- [ ] Sentry DSN set
- [ ] Database backups enabled
- [ ] Celery worker running
- [ ] Static/media storage configured
