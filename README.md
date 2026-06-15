# DRF E-commerce API

A simple E-commerce REST API built with Django REST Framework.

This project provides product management, shopping cart functionality, order creation, authentication, filtering, searching, ordering, and pagination.

## Features

* Product CRUD operations
* Category management
* Shopping cart system
* Add products to cart
* Update and remove cart items
* Create orders from cart
* JWT Authentication
* Custom permissions
* Search functionality
* Filtering by category
* Ordering results
* Pagination support

## Technologies Used

* Python
* Django
* Django REST Framework
* SQLite
* Simple JWT

## Installation

Clone the repository:

```bash
git clone https://github.com/elya3243/drf-ecommerce-api.git
cd drf-ecommerce-api
```

Create a virtual environment:

```bash
python -m venv venv
```

Activate the virtual environment:

Linux/macOS:

```bash
source venv/bin/activate
```

Windows:

```bash
venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Apply migrations:

```bash
python manage.py migrate
```

Run the server:

```bash
python manage.py runserver
```

## Authentication

JWT authentication is used.

Get access and refresh tokens:

```http
POST /api/token/
```

Refresh access token:

```http
POST /api/token/refresh/
```

## API Endpoints

### Products

```http
GET    /products/
POST   /products/
GET    /products/<id>/
PUT    /products/<id>/
DELETE /products/<id>/
```

### Categories

```http
GET    /categories/
POST   /categories/
```

### Cart

```http
GET    /cart/
POST   /cart/add/
PATCH  /cart/item/<id>/
DELETE /cart/item/<id>/
```

### Orders

```http
POST   /orders/create/
GET    /orders/
GET    /orders/<id>/
```

## Future Improvements

* Payment gateway integration
* Product images
* Wishlist functionality
* Product reviews and ratings
* Docker support

## Author

Developed by Elyas Derakhshafar.
