alembic current# Int2 Map Backend V2

## Hướng dẫn chạy project
#### `docker-compose up -d`
#### `docker exec -it [ID Container] bash`
#### `python migrate.py`
## Hướng dẫn sử dụng Alembic tạo database
## `khoi tao alembic: "alembic init alembic"`
## `ket noi db alembic mo file alembic.ini chinh sua url sqlalchemy.url: "alembic init alembic"`
### `Create a Migration Script: alembic revision -m "create account table"`
### `Autogrenerate db "alembic revision --autogenerate -m "first revision"""`
### `add collum by alembic: "alembic upgrade head"`