# GoCart — System Design

**GoCart** | *Shop Smarter. Shop Faster*

## Architecture Overview

```
┌─────────────┐     ┌─────────────┐     ┌──────────────────────────────────┐
│   React 19  │────▶│    Nginx    │────▶│  Django REST API (Gunicorn)      │
│   + Vite    │     │  Reverse    │     │  ┌────────┐ ┌────────┐        │
│   + Redux   │     │   Proxy     │     │  │Accounts│ │Products│ ...    │
└─────────────┘     └─────────────┘     │  └────────┘ └────────┘        │
                                        └──────────┬───────────────────────┘
                                                   │
                    ┌──────────────────────────────┼──────────────────────┐
                    │                              │                      │
              ┌─────▼─────┐                 ┌──────▼──────┐        ┌──────▼──────┐
              │ PostgreSQL │                 │    Redis    │        │   Celery    │
              │  Primary   │                 │   Cache +   │        │   Workers   │
              │    DB      │                 │   Broker    │        │             │
              └───────────┘                 └─────────────┘        └─────────────┘
```

## Layered Architecture

| Layer | Responsibility |
|-------|----------------|
| **Presentation** | React SPA, Redux state, API services |
| **API Gateway** | Nginx, CORS, rate limiting, static/media |
| **Application** | DRF ViewSets, serializers, permissions |
| **Service** | Business logic, payment, notifications |
| **Repository** | Data access abstraction |
| **Domain** | Django models, validators, signals |
| **Infrastructure** | PostgreSQL, Redis, Celery, Sentry |

## Request Flow

1. Client sends JWT in `Authorization: Bearer <token>`
2. Nginx routes `/api/*` to Gunicorn, `/` to React static
3. DRF authenticates via SimpleJWT, checks RBAC permissions
4. ViewSet delegates to Service layer
5. Service uses Repository for DB, Redis cache, Celery for async
6. Response serialized via DRF serializers

## Security

- JWT with refresh rotation + blacklist
- RBAC: `customer`, `admin` roles
- Rate limiting via DRF throttling
- OWASP headers via Django SecurityMiddleware
- Input validation at serializer + model level
- Razorpay signature verification for payments

## Caching Strategy

| Key Pattern | TTL | Invalidation |
|-------------|-----|--------------|
| `products:list:{hash}` | 5 min | Product save/delete signal |
| `products:featured` | 10 min | Product featured toggle |
| `categories:tree` | 15 min | Category CRUD |

## Monitoring

- **Sentry**: Exception tracking
- **Prometheus**: `/metrics` endpoint via django-prometheus
- **Grafana**: Dashboards for request latency, order volume
