# Тестовое задание: имитация webhook от банка

## Описание
POST /api/v1/webhook/bank/
Webhook принимает JSON следующего формата:
'''
{
  "operation_id": "ccf0a86d-041b-4991-bcf7-e2352f7b8a4a",
  "amount": 145000,
  "payer_inn": "1234567890",
  "document_number": "PAY-328",
  "document_date": "2024-04-27T21:00:00Z"
}
'''
Поведение
Если операция уже была (operation_id) — ничего не делает, возвращает 200 OK Требуется защита от дублей, то есть если приходит тот же самый вебхук, мы не должны заново пополнять баланс
Если новая:
создаёт Payment
начисляет сумму на баланс организации с payer_inn
логирует изменение баланса (в отдельную таблицу или просто print / log)
🧾 GET /api/v1/organizations/<inn>/balance/
Возвращает текущий баланс организации по ИНН:

{
  "inn": "1234567890",
  "balance": 145000
}

## Необходимые инструменты

- Docker и Docker Compose (версия 3.8+)

---

## Шаг 1. Создание файла `.env` по подобию .env_example

> При необходимости скорректируйте переменные под ваши настройки.

---

## Шаг 2. Конфигурация `docker-compose.yml`

Используется версия `3.8`. Сервисы:

- **postgresql-service** — PostgreSQL 17 с tmpfs-хранилищем данных (каждая перезагрузка — чистая БД).
- **redis-stack-server** — Redis Stack в качестве брокера задач.
- **minio-s3-srv** — MinIO для S3-совместимого хранения статики.
- **backend-django-main-app-service** — Django-приложение: миграции + `runserver`.
- **celery-worker** — Celery Worker для выполнения задач.
- **celery-beat** — Celery Beat для планировщика задач.
- **flower** — Веб-интерфейс для мониторинга Celery.

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

---

## Дополнительные возможности

- Автоматическая обновление баланса через через Celery.
- документацию апи можно найти по api/v1/swagger/
- webhook/bank/imitation/ через этот эндпойнт модно имитировать запрос от банка, который будет обрабатыватсья вебхуком.

---

**Успешной работы с проектом!**

