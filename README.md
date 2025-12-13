# 📚 Liberium - A Library Management System with API

A production-ready Django REST Framework API for managing a library system with user authentication, book management, and loan tracking.

## ✨ Features

- **JWT Authentication** - Secure token-based authentication using `djangorestframework-simplejwt`
- **User Roles** - Anonymous (read-only), Registered users (borrow/return), Admin (full CRUD)
- **Book Management** - Full CRUD operations for books with filtering, search, and pagination
- **Loan System** - Borrow and return books with automatic availability tracking
- **API Documentation** - Interactive Swagger/OpenAPI documentation
- **Comprehensive Testing** - 85%+ test coverage with pytest
- **Docker Support** - Ready-to-use Docker configuration
- **CI/CD** - GitHub Actions workflow for automated testing
- **Code Quality** - Pre-commit hooks with black, isort, and flake8

## 🏗️ Project Architecture

```
book-library-liberium/
├── config/                 # Django project configuration
│   ├── settings/
│   │   ├── base.py        # Base settings
│   │   ├── local.py       # Local development settings
│   │   └── production.py  # Production settings
│   ├── urls.py            # Main URL configuration
│   └── wsgi.py            # WSGI configuration
├── users/                 # User authentication app
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   └── urls.py
├── books/                 # Books management app
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   ├── filters.py
│   ├── permissions.py
│   └── urls.py
├── loans/                 # Loan management app
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   ├── services.py        # Business logic layer
│   └── urls.py
├── tests/                 # Test suite
│   ├── unit/              # Unit tests
│   └── integration/       # Integration tests
├── scripts/               # Utility scripts
│   └── seed_data.py       # Database seeding script
├── docker/                # Docker configuration
├── Dockerfile
├── docker-compose.yml
├── Makefile
├── requirements.txt
└── README.md
```

## 🚀 Quick Start

### Prerequisites

- Python 3.12+
- PostgreSQL 15+ (or SQLite for local development)
- Docker and Docker Compose (optional)

### Database Setup

To set up your PostgreSQL database, run the following commands:

1. **Open the PostgreSQL shell:**
   ```bash
   sudo -u postgres psql
   ```

2. **Create the database and user, then grant privileges:**
   ```sql
   CREATE DATABASE book_library_liberium;
   CREATE USER liberium_user WITH PASSWORD '1111';
   GRANT ALL PRIVILEGES ON DATABASE book_library_liberium TO liberium_user;

   GRANT USAGE ON SCHEMA public TO liberium_user;
   GRANT CREATE ON SCHEMA public TO liberium_user;
   GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO liberium_user;
   GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO liberium_user;
   ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON TABLES TO liberium_user;
   ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON SEQUENCES TO liberium_user;
   ```

3. **Exit the PostgreSQL shell:**
   ```sql
   \q
   ```

> **Note:** Remember to update your `.env` file with the database credentials you just created.

### Local Development Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd book-library-liberium
   ```

2. **Create and activate virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   make install
   # or
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your settings
   ```

5. **Run migrations**
   ```bash
   make migrate
   # or
   python manage.py migrate
   ```

6. **Create superuser** (optional)
   ```bash
   make superuser
   # or
   python manage.py createsuperuser
   ```

7. **Seed sample data** (optional)
   ```bash
   python scripts/seed_data.py
   ```

8. **Run development server**
   ```bash
   make run
   # or
   python manage.py runserver
   ```

9. **Access the API**
   - API Base: http://localhost:8000/
   - Swagger UI: http://localhost:8000/swagger/
   - Admin Panel: http://localhost:8000/admin/

## 🐋 Docker Setup

### Using Docker Compose

1. **Start services**
   ```bash
   make docker-up
   # or
   docker-compose up -d
   ```

2. **Run migrations**
   ```bash
   make docker-migrate
   # or
   docker-compose exec web python manage.py migrate
   ```

3. **Create superuser**
   ```bash
   make docker-superuser
   # or
   docker-compose exec web python manage.py createsuperuser
   ```

4. **View logs**
   ```bash
   make docker-logs
   # or
   docker-compose logs -f
   ```

5. **Stop services**
   ```bash
   make docker-down
   # or
   docker-compose down
   ```

### Docker Services

- **web** - Django application (port 8000)
- **db** - PostgreSQL database (port 5432)

## 📖 API Endpoints

### Authentication

- `POST /auth/register/` - Register a new user
- `POST /auth/login/` - Login and get JWT tokens
- `POST /auth/token/refresh/` - Refresh access token
- `GET /auth/me/` - Get current user info (authenticated)

### Users

- `GET /users/` - List all users (admin only)
- `GET /users/<id>/` - Get user details (admin only or self with authentication)
- `GET /users/<id>/loan_history/` - Get loan history for a user (admin only or self with authentication)

### Books

- `GET /books/` - List all books (with filtering, search, pagination)
- `GET /books/<id>/` - Get book details
- `POST /books/` - Create a book (admin only)
- `PUT /books/<id>/` - Update a book (admin only)
- `DELETE /books/<id>/` - Delete a book (admin only)
- `POST /books/<id>/borrow/` - Borrow a book (authenticated)
- `POST /books/<id>/return/` - Return a book (authenticated)

### Loans

- `GET /loans/` - List user's loans (self with authentication)
- `GET /loans/<id>/` - Get loan details (self with authentication)

### Documentation

- `GET /swagger/` - Swagger UI
- `GET /swagger.json` - OpenAPI schema
- `GET /redoc/` - ReDoc documentation

## 🔍 Filtering and Search

### Books Endpoint Filters

- `title` - Filter by title (case-insensitive contains)
- `author` - Filter by author (case-insensitive contains)
- `isbn` - Filter by exact ISBN
- `is_available` - Filter by availability (true/false)
- `search` - Search across title, author, and ISBN
- `ordering` - Order by title, author, created_at, page_count

### Example Requests

```bash
# Search for books
GET /books/?search=python

# Filter available books
GET /books/?is_available=true

# Filter by author
GET /books/?author=Fitzgerald

# Order by title
GET /books/?ordering=title
```

## 🔒 Permissions

### User Roles

1. **Anonymous Users**
   - Can browse and search books (read-only)
   - Cannot borrow books
   - Cannot create/update/delete books

2. **Registered Users**
   - All anonymous permissions
   - Can borrow books
   - Can return books
   - Can view their own loans

3. **Admin Users**
   - All registered user permissions
   - Can create/update/delete books
   - Full access to admin panel

### Permission Classes

- `IsAdminOrReadOnly` - Read-only for everyone, write for admins
- `IsAuthenticated` - Requires authentication
- `IsAuthenticatedOrReadOnly` - Read for everyone, write for authenticated users

## 🧪 Testing

### Run Tests

```bash
# Run all tests
make test

# Run with coverage
make test-coverage

# Run in verbose mode
make test-verbose

# Run in Docker
make docker-test
```

### Test Coverage

The project aims for 85%+ test coverage. Coverage reports are generated in:
- Terminal output
- `htmlcov/` directory (HTML report)
- `coverage.xml` (for CI/CD)

### Test Structure

- `tests/unit/` - Unit tests for models, serializers, services
- `tests/integration/` - Integration tests for API endpoints

## 🛠️ Development Tools

### Code Formatting

```bash
# Format code
make format

# Check formatting
make lint
```

### Pre-commit Hooks

Install pre-commit hooks:

```bash
pre-commit install
```

Hooks run automatically on commit:
- Black (code formatting)
- isort (import sorting)
- flake8 (linting)
- Various file checks

### Makefile Commands

```bash
make help              # Show all available commands
make install           # Install dependencies
make run               # Run development server
make test              # Run tests
make format            # Format code
make lint              # Run linting
make migrate           # Run migrations
make superuser         # Create superuser
make clean             # Clean cache files
make docker-up         # Start Docker containers
make docker-down       # Stop Docker containers
```

## 📦 Environment Variables

Create a `.env` file based on `.env.example`:

```env
# Django Settings
SECRET_KEY=django-insecure-change-me-in-production
ALLOWED_HOSTS=localhost,127.0.0.1
DB_NAME=book_library_liberium
DB_USER=liberium_user
DB_PASSWORD=1111
DB_HOST=localhost
DB_PORT=5432

# Database Settings
POSTGRES_DB=book_library_liberium
POSTGRES_USER=liberium_user
POSTGRES_PASSWORD=1111

# Production Settings
SECURE_SSL_REDIRECT=False
```

## 🚢 Deployment

### Production Checklist

1. Set `ALLOWED_HOSTS` with your domain
2. Configure PostgreSQL database
3. Set secure `SECRET_KEY`
4. Configure static files (WhiteNoise)
5. Set up SSL/HTTPS
6. Configure logging
7. Set up monitoring and error tracking

### Using Docker in Production

```bash
# Build image
docker-compose build

# Run with production settings
docker-compose -f docker-compose.yml up -d
```

### Environment Variables for Production

```env
# Django Settings
SECRET_KEY=<strong-secret-key>
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
DB_NAME=book_library_liberium
DB_USER=liberium_user
DB_PASSWORD=<secure-password>
DB_HOST=<host-name>
DB_PORT=5432

# Database Settings
POSTGRES_DB=book_library_liberium
POSTGRES_USER=liberium_user
POSTGRES_PASSWORD=<secure-password>

# Production Settings
SECURE_SSL_REDIRECT=True
```

## 📚 API Usage Examples

### Register a User

```bash
curl -X POST http://localhost:8000/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "john_doe",
    "email": "john@example.com",
    "password": "securepass123",
    "password2": "securepass123"
  }'
```

### Login

```bash
curl -X POST http://localhost:8000/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "john_doe",
    "password": "securepass123"
  }'
```

### Borrow a Book

```bash
curl -X POST http://localhost:8000/books/1/borrow/ \
  -H "Authorization: Bearer <access_token>"
```

### Return a Book

```bash
curl -X POST http://localhost:8000/books/1/return/ \
  -H "Authorization: Bearer <access_token>"
```

## 📝 License

This project is licensed under the MIT License.

## 🙏 Acknowledgments

- Django REST Framework
- djangorestframework-simplejwt
- drf-yasg for API documentation
- All contributors and open-source libraries used

## 🔗 Links

- [Swagger Documentation](http://localhost:8000/swagger/)
- [ReDoc Documentation](http://localhost:8000/redoc/)
- [Admin Panel](http://localhost:8000/admin/)

