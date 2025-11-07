# Flask Messenger

Небольшой учебный проект мессенджера на Flask с HTML-интерфейсом и REST API, использующий PostgreSQL.

## Возможности

- Веб-интерфейс для создания пользователей, чатов и отправки сообщений
- REST API с тем же функционалом
- Слой сервисов и репозиториев, разделяющий ответственность по ООП-принципам
- Docker/Docker-compose для быстрого развёртывания вместе с PostgreSQL

## Структура проекта

- `app/` — исходный код приложения
  - `models/` — ORM-модели SQLAlchemy
  - `db/` — инициализация БД и репозитории
  - `services/` — доменные сервисы
  - `routes/` — Flask Blueprints для веба и API
  - `templates/`, `static/` — фронтенд
- `wsgi.py` — точка входа
- `Dockerfile`, `docker-compose.yml` — контейнеризация
- `requirements.txt` — зависимости

## Локальный запуск без Docker

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
export DATABASE_URL="postgresql+psycopg2://user:pass@localhost:5432/messenger"  # настройте подключение
flask --app wsgi run --reload
```

## Docker Compose

1. Скопируйте файл `.env` из примера и при необходимости измените значения:

   ```bash
   cp env.example .env
   ```

   Ключевые переменные:

   - `APP_NAME`, `SECRET_KEY`, `FLASK_ENV`
   - `DATABASE_URL`
   - `WEB_IMAGE` — тег Docker-образа (например, `yourname/messenger:1.0.0`)
   - `POSTGRES_USER`, `POSTGRES_PASSWORD`, `POSTGRES_DB`

### Локальная разработка (сборка из исходников)

По умолчанию `docker-compose.yml` настроен на локальную сборку. Просто запустите:

```bash
docker compose up --build
```

Если в `.env` указан `WEB_IMAGE`, **закомментируйте или удалите** эту строку для локальной разработки:

```bash
# WEB_IMAGE=mrgan12009/messenger:1.0.0  # Закомментируйте для локальной сборки
```

- Веб-интерфейс: http://localhost:5000/
- REST API: http://localhost:5000/api

### Продакшн/сервер (использование готового образа)

Для использования готового образа из Docker Hub:

1. Убедитесь, что `WEB_IMAGE` в `.env` указывает на опубликованный образ:
   ```bash
   WEB_IMAGE=mrgan12009/messenger:1.0.0
   ```

2. Добавьте `image` в `docker-compose.yml` в секцию `web`:
   ```yaml
   services:
     web:
       image: ${WEB_IMAGE}
       build:
         context: .
         dockerfile: Dockerfile
   ```

3. Запустите:
   ```bash
   docker compose pull
   docker compose up -d
   ```

### Остановка и очистка

```bash
docker compose down
docker compose down -v  # удалить данные PostgreSQL
```

## Основные эндпоинты API

| Метод | Путь | Описание |
| --- | --- | --- |
| `GET` | `/api/users` | список пользователей |
| `POST` | `/api/users` | создать пользователя |
| `GET` | `/api/chats` | список чатов |
| `POST` | `/api/chats` | создать чат |
| `GET` | `/api/chats/<id>` | детали чата + сообщения |
| `POST` | `/api/chats/<id>/messages` | отправить сообщение |

Пример создания чата:

```bash
curl -X POST http://localhost:5000/api/chats \
  -H "Content-Type: application/json" \
  -d '{"title": "General", "participant_ids": [1, 2]}'
```

## Сборка и публикация образа

```bash
docker login
docker build -t yourname/messenger:1.0.0 .
docker push yourname/messenger:1.0.0
```

После публикации обновите `WEB_IMAGE` и перезапустите Compose (см. раздел выше).

## Развёртывание на сервере

1. Установите Docker и Docker Compose.
2. Скопируйте на сервер файлы `docker-compose.yml`, `docker-compose.dev.yml` (опционально), `env.example`, `.env`.
3. В `.env` укажите `WEB_IMAGE` на опубликованный образ.
4. Выполните:

   ```bash
   docker compose pull
   docker compose up -d
   ```

5. Проверьте логи: `docker compose logs -f web`.

### Миграции/инициализация базы

При первом запуске SQLAlchemy создаст таблицы автоматически. Для реального проекта рекомендуется добавить Alembic.

## Тестовые данные

Вы можете создать пользователей и чаты через веб-формы или API. После этого чаты и сообщения появятся в интерфейсе.

