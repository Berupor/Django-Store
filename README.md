# Marketplace Django Project

This is a Django based project that allows you to set up an online store with a payment system. It includes basic
functionalities such as adding products, managing orders, and processing payments.

## Features

- Shopping cart for storing selected items
- Order placement and management
- Payment integration with Stripe
- Order history and status tracking for users
- Admin panel for managing store, products, orders
- Secure implementation with protection against common web vulnerabilities (such as CSRF)

## Project initialization

1. Clone the repository to your local machine
2. Create a .env file and fill it with values ​​from `.env`
3. Run compose `docker-compose up -d --build`

### In the container:

4. Run migrations

```console
python manage.py migrate
```

5. Create a superuser

```console
python manage.py createsuperuser
```

6. Login to Strip

```console
strip login
```

7. Configure Strip

```console
make listen
```

## Usage

- Add items in `http://localhost:8000/admin/` panel
- Go to `http://localhost:8000/api/v1/items/` and start using marketplace

