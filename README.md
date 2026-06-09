# GoCart

**Shop Smarter. Shop Faster.**

Enterprise-grade full-stack e-commerce platform built with Django REST Framework and React 19.

![Python](https://img.shields.io/badge/Python-3.12+-blue)
![Django](https://img.shields.io/badge/Django-5+-green)
![React](https://img.shields.io/badge/React-19-61dafb)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-blue)
![Docker](https://img.shields.io/badge/Docker-Ready-2496ED)

---

## Features

### Backend
- JWT Authentication (SimpleJWT) with refresh rotation & blacklisting
- RBAC: Customer & Admin roles with custom DRF permissions
- Products: CRUD, search, filter, sort, pagination, featured, best sellers
- Nested categories with recursive tree API
- Cart: add/remove/update, save for later, tax & discount calculation
- Wishlist, Reviews & Ratings (verified purchase validation)
- Addresses (shipping/billing), Coupons (percentage & fixed)
- Orders: place, track, cancel, invoice generation
- Razorpay payments with webhook & refund support
- Celery + Redis: email notifications, background tasks
- Redis caching for products & categories
- Admin analytics dashboard APIs
- OpenAPI/Swagger documentation
- Sentry, Prometheus monitoring
- Structured JSON logging

### Frontend
- React 19 + Vite + Redux Toolkit + Redux Persist
- Tailwind CSS with dark mode
- Amazon/Flipkart-inspired responsive UI
- Protected & admin routes
- Razorpay checkout integration
- Skeleton loaders, error boundaries, toast notifications
- Code splitting & lazy loading

---

## Tech Stack

| Layer | Technologies |
|-------|-------------|
| Backend | Python 3.12, Django 5, DRF, PostgreSQL, Redis, Celery |
| Frontend | React 19, Vite, Redux Toolkit, Tailwind CSS, Recharts |
| Auth | SimpleJWT, RBAC |
| Payments | Razorpay |
| DevOps | Docker, Nginx, GitHub Actions |
| Monitoring | Sentry, Prometheus, Grafana |

---

## Quick Start

### Prerequisites
- Python 3.12+
- Node.js 20+
- PostgreSQL 16
- Redis 7

### Backend

```bash
cd backend
python -m venv venv
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate

pip install -r requirements.txt
cp .env.example .env
# Edit .env with your database credentials

python manage.py migrate
python manage.py seed_data
python manage.py runserver
```

**Default Admin:** `admin@gocart.com` / `Admin@123`

### Frontend

```bash
cd frontend
npm install
cp .env.example .env
npm run dev
```

Open http://localhost:5173

### Docker (Recommended)

```bash
cp backend/.env.example backend/.env
docker compose up -d --build
docker compose exec backend python manage.py migrate
docker compose exec backend python manage.py seed_data
```

- App: http://localhost
- API Docs: http://localhost/api/docs/
- Admin: http://localhost/admin/

---

## API Endpoints

| Module | Base URL |
|--------|----------|
| Auth | `/api/v1/accounts/` |
| Products | `/api/v1/products/` |
| Cart | `/api/v1/cart/` |
| Orders | `/api/v1/orders/` |
| Payments | `/api/v1/payments/` |
| Notifications | `/api/v1/notifications/` |
| Analytics | `/api/v1/analytics/` |

Full documentation: http://localhost:8000/api/docs/

---

## Project Structure

```
gocart/
├── backend/
│   ├── config/              # Django settings, URLs, Celery
│   ├── apps/
│   │   ├── accounts/        # Auth, users, addresses
│   │   ├── products/        # Categories, products, reviews, wishlist
│   │   ├── cart/            # Shopping cart
│   │   ├── orders/          # Orders, coupons
│   │   ├── payments/        # Razorpay integration
│   │   ├── notifications/   # Email & in-app notifications
│   │   ├── analytics/       # Admin dashboard APIs
│   │   └── common/          # Shared utilities, permissions, cache
│   └── tests/               # Pytest test suite
├── frontend/
│   └── src/
│       ├── components/      # UI components
│       ├── pages/           # Route pages
│       ├── store/           # Redux slices
│       └── services/        # API client
├── docs/                    # System design, database, deployment
├── nginx/                   # Nginx reverse proxy config
└── docker-compose.yml
```

---

## Testing

### Backend

```bash
cd backend
pytest
```

### Frontend

```bash
cd frontend
npm run test
```

---

## Deployment

See [docs/DEPLOYMENT.md](docs/DEPLOYMENT.md) for guides on:
- Docker Compose
- Render
- Railway
- AWS EC2
- Vercel (frontend)

---

## Environment Variables

### Backend (`backend/.env`)

| Variable | Description |
|----------|-------------|
| `SECRET_KEY` | Django secret key |
| `DB_*` | PostgreSQL credentials |
| `REDIS_URL` | Redis connection URL |
| `RAZORPAY_KEY_ID` | Razorpay API key |
| `RAZORPAY_KEY_SECRET` | Razorpay secret |
| `FRONTEND_URL` | Frontend URL for email links |
| `SENTRY_DSN` | Sentry error tracking |

### Frontend (`frontend/.env`)

| Variable | Description |
|----------|-------------|
| `VITE_API_URL` | Backend API base URL |
| `VITE_RAZORPAY_KEY_ID` | Razorpay public key |

---

## License

MIT License — Built for portfolio demonstration.

---

**GoCart** — *Shop Smarter. Shop Faster.*
