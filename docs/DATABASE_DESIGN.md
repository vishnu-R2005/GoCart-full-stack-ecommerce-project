# GoCart — Database Design

## ER Diagram

```mermaid
erDiagram
    User ||--o{ Address : has
    User ||--o{ CartItem : owns
    User ||--o{ WishlistItem : owns
    User ||--o{ Order : places
    User ||--o{ Review : writes
    User ||--o{ Notification : receives

    Category ||--o{ Category : parent
    Category ||--o{ Product : contains

    Product ||--o{ ProductImage : has
    Product ||--o{ Review : receives
    Product ||--o{ CartItem : in
    Product ||--o{ WishlistItem : in
    Product ||--o{ OrderItem : ordered

    Order ||--o{ OrderItem : contains
    Order ||--o| Payment : has
    Order ||--o| Coupon : uses
    Order }o--|| Address : ships_to
    Order }o--|| Address : bills_to

    Coupon ||--o{ Order : applied

    User {
        uuid id PK
        string email UK
        string role
        boolean is_verified
    }

    Category {
        int id PK
        string name
        string slug UK
        int parent_id FK
    }

    Product {
        int id PK
        string name
        string slug UK
        decimal price
        decimal discount_price
        int stock
        string sku UK
        int category_id FK
        float avg_rating
        int reviews_count
    }

    Order {
        uuid id PK
        string order_number UK
        string status
        decimal total
        uuid user_id FK
    }

    Payment {
        uuid id PK
        string razorpay_order_id
        string razorpay_payment_id
        string status
        decimal amount
    }
```

## Relationships

| Parent | Child | Type | On Delete |
|--------|-------|------|-----------|
| User | Address | 1:N | CASCADE |
| User | CartItem | 1:N | CASCADE |
| User | Order | 1:N | PROTECT |
| Category | Category | self-ref | CASCADE |
| Category | Product | 1:N | PROTECT |
| Product | ProductImage | 1:N | CASCADE |
| Product | Review | 1:N | CASCADE |
| Order | OrderItem | 1:N | CASCADE |
| Order | Payment | 1:1 | CASCADE |

## Indexing Strategy

```sql
-- Products: search & filter
CREATE INDEX idx_product_category ON products(category_id);
CREATE INDEX idx_product_active_featured ON products(is_active, is_featured);
CREATE INDEX idx_product_slug ON products(slug);
CREATE INDEX idx_product_sku ON products(sku);
CREATE INDEX idx_product_price ON products(price);

-- Orders: user history & admin analytics
CREATE INDEX idx_order_user_status ON orders(user_id, status);
CREATE INDEX idx_order_created ON orders(created_at DESC);
CREATE INDEX idx_order_number ON orders(order_number);

-- Reviews: product aggregation
CREATE INDEX idx_review_product ON reviews(product_id);
CREATE UNIQUE INDEX idx_review_user_product ON reviews(user_id, product_id);

-- Cart: fast lookup
CREATE UNIQUE INDEX idx_cart_user_product ON cart_items(user_id, product_id);

-- Categories: tree traversal
CREATE INDEX idx_category_parent ON categories(parent_id);
CREATE INDEX idx_category_slug ON categories(slug);
```

## Query Optimization

1. **Product listing**: `select_related('category')` + `prefetch_related('images')`
2. **Order details**: `prefetch_related('items__product')`
3. **Admin dashboard**: Aggregate queries with `annotate()` + `values()` — avoid N+1
4. **Featured products**: Redis cache, invalidated on save
5. **Review ratings**: Denormalized `avg_rating` / `reviews_count` on Product, updated via signals
