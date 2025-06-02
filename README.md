# Тестовое задание: Имитация webhook от банка

## Описание задачи

Сервис на Django принимает webhook-и от банка, корректно начисляет баланс организации по ИНН, защищён от дублей транзакций.

### Эндпоинты:

- **POST `/api/v1/webhook/bank/`**  
  Принимает JSON формата:
  ```json
  {
    "operation_id": "ccf0a86d-041b-4991-bcf7-e2352f7b8a4a",
    "amount": 145000,
    "payer_inn": "1234567890",
    "document_number": "PAY-328",
    "document_date": "2024-04-27T21:00:00Z"
  }
  ```
Поведение
Если операция уже была (operation_id) — ничего не делает, возвращает 200 OK Требуется защита от дублей, то есть если приходит тот же самый вебхук, мы не должны заново пополнять баланс
Если новая:
создаёт Payment
начисляет сумму на баланс организации с payer_inn
логирует изменение баланса (в отдельную таблицу или просто print / log)

- **GET `/api/v1/organizations/<inn>/balance/`**
Возвращает текущий баланс организации по ИНН:
  ```json
  {
    "inn": "1234567890",
    "balance": 145000
  }
  ```
## Необходимые инструменты

- Docker и Docker Compose (версия 3.8+)

---

## Шаг 1. Создание файла `.env` по подобию .env_example

> При необходимости скорректируйте переменные под ваши настройки.

---

## Шаг 2. Конфигурация `docker-compose.yml`


Используются два отдельных Redis:

redis-cache — для кэша Django

redis-celery — для брокера задач Celery

Сервисы:

postgresql-service — PostgreSQL 17

redis-cache — Redis для Django-кэша (порт 6380)

redis-celery — Redis для Celery (порт 6379)

minio-s3-srv — S3-совместимое хранилище

backend-django-main-app-service — Django-приложение

celery-worker — Celery worker

celery-beat — Celery beat

flower — мониторинг Celery

---

## Шаг 3. Запуск проекта

В корне репозитория выполните:

```bash
docker-compose up -d --build
```

Это создаст и запустит контейнеры для всех сервисов.

```bash
docker-compose ps
```

---

## Шаг 4. Настройка MinIO

1. Откройте консоль MinIO по адресу: http://localhost:9001
2. Введите credentials из `.env`.
3. Создайте бакет с именем `s3bucket` и сделайте его публичным.

---

## Шаг 5. Первичная настройка Django

1. Соберите статические файлы:

    ```bash
    docker-compose exec backend-django-main-app-service python manage.py collectstatic
    ```

2. Создайте суперпользователя:

    ```bash
    docker-compose exec backend-django-main-app-service python manage.py createsuperuser
    ```

---

## Шаг 6. Доступ к административным панелям

- **Admin**: http://localhost:8000/admin/

Используйте учётные данные суперпользователя.
Далее необходимо создать организацию, заполнив соответсвующие поля

---

## Дополнительные возможности

- Автоматическое обновление баланса через через Celery.
- документацию апи можно найти по api/v1/swagger/
- http://127.0.0.1:8000/swagger/webhook/bank/imitation/ через этот эндпойнт модно имитировать запрос от банка, который будет обрабатыватсья вебхуком.
- Логирование изменения баланса можно просмотреть в контейнере celery-worker
---

**Успешной работы с проектом!**

