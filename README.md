# Django Next.js Template

A powerful, production-ready full-stack application template combining a **Django Rest Framework (DRF)** backend with a **Next.js** frontend. This project is architected for scalability, featuring authentication, multi-tenancy, payments, and CMS integration out of the box.

## 🚀 Features

### Backend (Django)
- **Authentication**: JWT-based auth with `SimpleJWT` and Social Authentication.
- **API**: Fully documented REST API with `drf-spectacular` (Swagger/Redoc).
- **Payments**: Stripe integration via `dj-stripe`.
- **Multi-tenancy**: Built-in support for standard multi-tenant architecture.
- **CMS**: Contentful integration.
- **AI**: OpenAI integration ready.
- **Task Queue**: Celery with Redis.
- **Security**: Robust access policies with `drf-access-policy`.
- **Developer Experience**:
    - `django-debug-toolbar` for performance profiling.
    - `drf-standardized-errors` for consistent error handling.
    - `django-cors-headers` pre-configured for Next.js.

### Frontend (Next.js)
- **Framework**: Next.js 14+ (App Router).
- **Language**: TypeScript for type safety.
- **Styling**: Tailwind CSS.
- **API Client**: Optimized for fetching data from the Django backend.

## 📂 Project Structure

```bash
.
├── backend/    # Django Project (API, DB, Celery)
├── frontend/   # Next.js Application (UI)
└── docs/       # Comprehensive System Design & Guides
```

## 🛠️ Getting Started

### Prerequisites
- Python 3.10+
- Node.js 18+
- `pipenv` (recommended for Python dependency management)

### 1. Backend Setup

```bash
cd backend

# Install dependencies
pipenv install --dev

# Activate virtual environment
pipenv shell

# Configure Environment Variables
cp .env.example .env
# Edit .env with your database and API keys

# Run Migrations
python manage.py migrate

# Create Superuser
python manage.py createsuperuser

# Start Server
python manage.py runserver
```
*The API will be available at `http://localhost:8000`*

### 2. Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Start Development Server
npm run dev
```
*The UI will be available at `http://localhost:3000`*

## 📚 Documentation

Detailed documentation is available in the `docs/` directory:

- **[System Design](docs/system_design/)**: Comprehensive architectural plans (Requirements, Architecture, Detailed Design).
- **[Django Rest Framework](docs/django_rest_framework/)**: Guides for installed packages:
    - [Access Policy](docs/django_rest_framework/6.%20drf_access_policy.ipynb)
    - [Spectacular (Swagger)](docs/django_rest_framework/7.%20drf_spectacular.ipynb)
    - [CORS Headers](docs/django_rest_framework/8.%20cors_headers.ipynb)
    - [Nested Routers](docs/django_rest_framework/9.%20drf_nested_routers.ipynb)
    - [Camel Case](docs/django_rest_framework/10.%20drf_camel_case.ipynb)
    - [Standardized Errors](docs/django_rest_framework/11.%20drf_standardized_errors.ipynb)
    - [Debug Toolbar](docs/django_rest_framework/12.%20django_debug_toolbar.ipynb)

## 🔗 API Documentation

Once the backend is running, access the interactive API docs:
- **Swagger UI**: [http://localhost:8000/doc/](http://localhost:8000/doc/)
- **Redoc**: [http://localhost:8000/redoc/](http://localhost:8000/redoc/)
