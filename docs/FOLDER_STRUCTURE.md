# GoCart Folder Structure

```
Salon_management/                    # Project root (GoCart)
├── backend/
│   ├── config/                      # Django project config
│   │   ├── settings.py
│   │   ├── settings_test.py
│   │   ├── urls.py
│   │   ├── celery.py
│   │   └── wsgi.py
│   ├── apps/
│   │   ├── common/                  # Shared utilities
│   │   │   ├── cache.py
│   │   │   ├── exceptions.py
│   │   │   ├── logging.py
│   │   │   ├── middleware.py
│   │   │   ├── pagination.py
│   │   │   ├── permissions.py
│   │   │   ├── utils.py
│   │   │   ├── validators.py
│   │   │   └── management/commands/seed_data.py
│   │   ├── accounts/                # Auth, users, addresses
│   │   │   ├── models.py
│   │   │   ├── serializers.py
│   │   │   ├── services.py
│   │   │   ├── repositories.py
│   │   │   ├── views.py
│   │   │   ├── urls.py
│   │   │   ├── backends.py
│   │   │   └── signals.py
│   │   ├── products/                # Categories, products, reviews, wishlist
│   │   │   ├── models.py
│   │   │   ├── serializers.py
│   │   │   ├── services.py
│   │   │   ├── repositories.py
│   │   │   ├── filters.py
│   │   │   ├── views.py
│   │   │   └── signals.py
│   │   ├── cart/
│   │   ├── orders/                  # Orders, coupons
│   │   ├── payments/                # Razorpay
│   │   ├── notifications/           # Celery email tasks
│   │   └── analytics/               # Admin dashboard APIs
│   ├── templates/
│   │   ├── emails/
│   │   └── orders/invoice.html
│   ├── tests/                       # Pytest + Factory Boy
│   ├── requirements.txt
│   ├── Dockerfile
│   └── manage.py
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── auth/ProtectedRoute.jsx
│   │   │   ├── common/ErrorBoundary.jsx, Skeleton.jsx
│   │   │   ├── layout/Navbar.jsx, Footer.jsx, Layout.jsx
│   │   │   └── products/ProductCard.jsx
│   │   ├── pages/                   # All route pages
│   │   ├── store/slices/            # Redux Toolkit slices
│   │   ├── services/api.js          # Axios API client
│   │   └── test/
│   ├── Dockerfile
│   └── package.json
├── docs/
│   ├── SYSTEM_DESIGN.md
│   ├── DATABASE_DESIGN.md
│   ├── FOLDER_STRUCTURE.md
│   └── DEPLOYMENT.md
├── nginx/nginx.conf
├── monitoring/prometheus.yml
├── docker-compose.yml
├── .github/workflows/ci.yml
└── README.md
```
