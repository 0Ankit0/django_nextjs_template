# Entity Relationship Diagram (ERD)

```mermaid
erDiagram
    iam_user {
        hashid id PK
        varchar username
        varchar email
        varchar password
        bool is_active
        bool is_superuser
    }

    multitenancy_tenant {
        hashid id PK
        varchar name
        varchar slug
        varchar billing_email
        varchar type
    }

    multitenancy_tenantmembership {
        hashid id PK
        fk user_id
        fk tenant_id
        varchar role
        bool is_accepted
    }

    djstripe_customer {
        varchar id PK "stripe_id"
        fk subscriber_id "Tenant"
        decimal balance
    }

    djstripe_subscription {
        varchar id PK
        fk customer_id
        varchar status
        timestamp current_period_end
    }

    djstripe_product {
        varchar id PK
        varchar name
    }

    djstripe_price {
        varchar id PK
        fk product_id
        decimal unit_amount
        varchar currency
    }

    iam_user ||--o{ multitenancy_tenantmembership : has
    multitenancy_tenant ||--o{ multitenancy_tenantmembership : has
    multitenancy_tenant ||--o| djstripe_customer : "is subscriber"
    djstripe_customer ||--o{ djstripe_subscription : has
    djstripe_subscription }|--|| djstripe_price : "based on"
    djstripe_price }|--|| djstripe_product : "variant of"
```
