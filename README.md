# KanMind Backend

A RESTful API backend for KanMind – a Kanban-style project management application built with Django and Django REST Framework.

## Tech Stack

- Python 3.x
- Django 6.x
- Django REST Framework
- SQLite (development)

## Project Structure

```
kanmind_backend/
├── core/               # Project settings, root URLs, wsgi
├── user_auth_app/      # Registration, login, user profiles
│   └── api/            # serializers, views, urls, permissions
├── boards_app/         # Board management
│   └── api/
├── tasks_app/          # Task & comment management
│   └── api/
└── requirements.txt
```

## Getting Started

### 1. Clone the repository

```bash
git clone <your-repo-url>
cd kanmind_backend
```

### 2. Create and activate a virtual environment

```bash
python -m venv env

# Windows
env\Scripts\activate

# macOS / Linux
source env/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Apply migrations

```bash
python manage.py migrate
```

### 5. Create a superuser (optional, for Django Admin)

```bash
python manage.py createsuperuser
```

### 6. Create the guest user

```bash
python manage.py create_guest_user
```

### 7. Start the development server

```bash
python manage.py runserver
```

The API is now available at `http://127.0.0.1:8000/api/`.

## API Overview

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/registration/` | Register a new user |
| POST | `/api/login/` | Login and receive auth token |
| GET | `/api/boards/` | List all boards for current user |
| POST | `/api/boards/` | Create a new board |
| GET | `/api/boards/{id}/` | Retrieve board detail with tasks |
| PATCH | `/api/boards/{id}/` | Update board title or members |
| DELETE | `/api/boards/{id}/` | Delete a board |
| GET | `/api/email-check/` | Check if an email is registered |
| GET | `/api/tasks/assigned-to-me/` | Tasks assigned to current user |
| GET | `/api/tasks/reviewing/` | Tasks where current user is reviewer |
| POST | `/api/tasks/` | Create a task |
| PATCH | `/api/tasks/{id}/` | Update a task |
| DELETE | `/api/tasks/{id}/` | Delete a task |
| GET | `/api/tasks/{id}/comments/` | List comments on a task |
| POST | `/api/tasks/{id}/comments/` | Add a comment |
| DELETE | `/api/tasks/{id}/comments/{id}/` | Delete a comment |

## Authentication

All endpoints (except registration and login) require a token in the request header:

```
Authorization: Token <your-token>
```

## Notes

- The database file (`db.sqlite3`) is excluded from version control.
- CORS is enabled for all origins in development (`CORS_ALLOW_ALL_ORIGINS = True`). Restrict this in production.
- Never use `DEBUG = True` or the default `SECRET_KEY` in production.
