# fastapi - celery - rabbitmq - redis - alembic -> Docker

## build and run containers

```bash
docker-compose up -d --build
```

This will expose fastapi application on 5000 and celery flower on 5566

swagger docs - `http://localhost:5000/docs`

redoc - `http://localhost:5000/redoc`

celery flower - `http://localhost:5566`
