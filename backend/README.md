# dsauce_app Backend (Django + DRF + PostgreSQL + Channels)

## Overview
Production-ready backend replacing Appwrite with modular Django apps:
- `apps/authentication`
- `apps/users`
- `apps/friendships`
- `apps/posts`
- `apps/messaging`
- `apps/notifications`
- `apps/courses`
- `apps/uploads`

## Installation Guide
```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements/development.txt
cp .env.example .env
```

## Run with Docker
```bash
cd backend
docker compose up --build
```

## Run locally (without Docker)
```bash
cd backend
export USE_SQLITE=True  # optional local fallback
python manage.py migrate
python manage.py runserver
```

## Environment Variables
Use `.env.example`.
Important keys:
- `DJANGO_SECRET_KEY`
- `DJANGO_DEBUG`
- `POSTGRES_DB`, `POSTGRES_USER`, `POSTGRES_PASSWORD`, `POSTGRES_HOST`, `POSTGRES_PORT`
- `REDIS_HOST`, `REDIS_PORT`
- `CORS_ALLOWED_ORIGINS`
- `JWT_ACCESS_MINUTES`, `JWT_REFRESH_DAYS`

## Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

## Create Superuser
```bash
python manage.py createsuperuser
```

## Seed Sample Test Data
```bash
python manage.py seed_sample_data
```
Sample users created:
- `admin@dsauce.app / AdminPass123!`
- `merchant@dsauce.app / MerchantPass123!`
- `customer@dsauce.app / CustomerPass123!`

## Seed Initial Admin
Set `ADMIN_SEED_EMAIL`, `ADMIN_SEED_USERNAME`, and `ADMIN_SEED_PASSWORD` in `.env`, then run:
```bash
python manage.py seed_admin
```

## API Documentation (Core Endpoints)
Base URL: `/api`

### Authentication
- `POST /api/auth/register/`
- `POST /api/auth/login/`
- `POST /api/auth/logout/`
- `POST /api/auth/refresh/`
- `POST /api/auth/password-reset/request/`
- `POST /api/auth/password-reset/confirm/`
- `POST /api/auth/email/verify/`
- `GET /api/auth/me/`

### Users
- `GET /api/users/` (search/order/filter)
- `GET /api/users/me/`
- `PATCH /api/users/update_profile/`
- `POST /api/users/upload_profile_image/`
- `GET /api/users/suggestions/`

### Friendships
- `POST /api/friendships/send/`
- `POST /api/friendships/{id}/accept/`
- `POST /api/friendships/{id}/reject/`
- `DELETE /api/friendships/remove/{friend_id}/`
- `GET /api/friendships/friends/`
- `GET /api/friendships/mutual/{user_id}/`

### Posts
- `GET|POST /api/posts/`
- `PATCH|DELETE /api/posts/{id}/`
- `POST /api/posts/{id}/like/`
- `GET /api/posts/feed/`
- `GET|POST /api/comments/`

### Messaging
- `GET|POST /api/conversations/`
- `GET|POST /api/messages/`
- `POST /api/messages/mark_read/`

### Notifications
- `GET /api/notifications/`
- `POST /api/notifications/{id}/mark_read/`
- `POST /api/notifications/mark_all_read/`

### Courses
- `GET|POST /api/courses/`
- `GET|POST /api/materials/`
- `GET|POST /api/assignments/`
- `GET|POST /api/enrollments/`
- `GET|POST /api/submissions/`

### Uploads
- `POST /api/uploads/upload/`

## Example Requests/Responses

### Register Request
```json
{
  "username": "john",
  "email": "john@example.com",
  "password": "StrongPass123!",
  "role": "customer"
}
```
Response `201 Created`
```json
{
  "id": 5,
  "username": "john",
  "email": "john@example.com",
  "profile_picture": null,
  "bio": "",
  "role": "customer",
  "is_verified": false,
  "created_at": "2026-05-10T10:00:00Z",
  "updated_at": "2026-05-10T10:00:00Z"
}
```

### Login Request
```json
{
  "email": "john@example.com",
  "password": "StrongPass123!"
}
```
Response `200 OK`
```json
{
  "refresh": "<jwt-refresh>",
  "access": "<jwt-access>"
}
```

### Create Post Request
```json
{
  "content": "My first post"
}
```
Response `201 Created`
```json
{
  "id": 10,
  "user": 5,
  "user_username": "john",
  "content": "My first post",
  "media": null,
  "likes_count": 0,
  "comments_count": 0,
  "created_at": "2026-05-10T10:10:00Z",
  "updated_at": "2026-05-10T10:10:00Z"
}
```

### WebSocket Endpoints
- Chat: `ws://localhost:8000/ws/chat/{conversation_id}/?token=<jwt-access>`
- Presence: `ws://localhost:8000/ws/presence/?token=<jwt-access>`
- Notifications: `ws://localhost:8000/ws/notifications/?token=<jwt-access>`

Client messages for chat websocket:
```json
{"action": "typing", "is_typing": true}
```
```json
{"action": "message", "content": "Hello"}
```
