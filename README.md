# Coderr – Developer Platform Backend

**Coderr** is a backend system for a developer platform that connects
clients and developers. The backend is built using *Django* and
*Django REST Framework*.

The project provides the server-side logic for managing users, developer
profiles, offers, and orders. It ensures that all data handling,
authentication, and permissions work reliably together with a frontend
application.

Coderr focuses on providing a structured API that allows clients to browse
developer services while enabling developers to manage their profiles and
offers.

The project provides the backend API for an existing frontend application.

---

## 🚀 Features

- User registration and authentication
- Developer profile management
- Service and offer creation
- Order management between clients and developers
- Permission-based access control
- RESTful API endpoints for frontend integration

---

## 🛠 Tech Stack

- Python 3
- Django
- Django REST Framework
- Token Authentication
- SQLite (development)

---

## 📦 Installation

### 1. Clone the repository

```bash
git clone https://github.com/alexschoefer/Coderr.git
cd Coderr
```

### 2. Create and activate a virtual environment

```bash
python -m venv venv

# macOS / Linux
source venv/bin/activate

# Windows
venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Apply migrations

```bash
python manage.py migrate
```

### 5. Run the development server

```bash
python manage.py runserver
```

---

## 🔐 Authentication

Coderr uses **token-based authentication** to secure API access.
After successful registration or login, the API returns an authentication token.

Include the token in the request headers:

```http
Authorization: Token your_token_here
```

---

## 🛠 Superuser & Admin Access

For administrative tasks, Coderr provides access to the Django admin interface.
A superuser account is required to manage users, developer profiles, offers,
and other database objects.

### 1. Create a Superuser

```bash
python manage.py createsuperuser
```

Follow the prompts to create an admin username, email, and password.

### 2. Start the Development Server

```bash
python manage.py runserver
```

### 3. Access the Admin Panel

Open the following URL in your browser:

```txt
http://127.0.0.1:8000/admin/
```

Log in using the superuser credentials you created earlier.

### 4. Admin Capabilities

- Manage registered users
- Edit developer profiles
- View and modify offers
- Inspect database entries
- Debug application data

---

## 📚 API Overview

### Authentication

| Method | Endpoint | Description |
|---|---|---|
| POST | `/api/register/` | Register a new user |
| POST | `/api/login/` | Login and receive authentication token |

---

### Business and Customer Profiles

| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/profiles/business` | List available business profiles |
| GET | `/api/profiles/customer` | List available customer profiles |
| GET | `/api/profiles/<id>/` | Retrieve business profile or customer profile |
| PATCH | `/api/profiles/<id>/` | Update business profile or customer profile |

---

### Offers

| Method | Endpoint | Description |
|---|---|---|
| POST | `/api/offers/` | Create a new service offer |
| GET | `/api/offers/` | List available offers |
| GET | `/api/offers/<id>/` | Retrieve offer details |
| PATCH | `/api/offers/<id>/` | Update an offer |
| DELETE | `/api/offers/<id>/` | Delete an offer |

---

### Orders

| Method | Endpoint | Description |
|---|---|---|
| POST | `/api/orders/` | Create a new order |
| GET | `/api/orders/` | List available orders |
| GET | `/api/order-count/<id>/` | Returns the number of active orders for a specific business user |
| GET | `/api/completed-order-count/<id>/` | Returns the number of completed orders for a specific business user |
| PATCH | `/api/orders/<id>/` | Update an order |
| DELETE | `/api/offers/<id>/` | Delete an offer |

---

### Review

| Method | Endpoint | Description |
|---|---|---|
| POST | `/api/reviews/` | Create a new review |
| GET | `/api/reviews/` | List available reviews |
| PATCH | `/api/reviews/<id>/` | Update a review |
| DELETE | `/api/review/<id>/` | Delete a review |

---

### Base-Info

| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/base-info/` | Provides general background information about the platform |

---

## 🔐 Permission Concept

- Only authenticated users can access protected endpoints
- Business users can only manage their own profiles and offers
- Customers can browse developers and available offers
- Only offer owners can update or delete their offers
- Orders can only be accessed by the involved users

---

## 📄 License

This project is licensed under the MIT License — © 2026 Alex Schöfer.