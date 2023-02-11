## Project initialization

1. Create a .env file and fill it with values ​​from `.env`
2. Run the project `docker-compose up -d --build`

### In the container:

3. Run migrations
4. Create a superuser
5. Login to Strip

```console
strip login
```

6. Configure Strip

```console
make listen
```

7. Add items in `http://localhost:8000/admin/` admin panel
8. Go to `http://localhost:8000/api/v1/items/` and use web site

---
