# Сервис для оплаты заказов
Бэкенд - Django.  
БД - Postgres или SQLite  
Платежная система - [Stripe](https://stripe.com/docs).

## Перед запуском
1) Скачайте проект:
```commandline
git clone https://github.com/949027/things-store
```
2) Создайте файл `.env` в корне проекта со следующими настройками.

Необходимо:
- `STRIPE_SECRET_KEY` - получить [здесь](https://dashboard.stripe.com/test/dashboard), предварительно зарегистрироваться.
- `STRIPE_PUBLISHABLE_KEY` - получить [здесь](https://dashboard.stripe.com/test/dashboard), предварительно зарегистрироваться.
- `SECRET_KEY` — [секретный ключ](https://docs.djangoproject.com/en/4.1/ref/settings/#std-setting-SECRET_KEY) проекта. Он отвечает за шифрование на сайте.

Необязательно:
- `DEBUG` - [дебаг-режим](https://docs.djangoproject.com/en/4.1/ref/settings/#debug). По умолчанию - True.
- `ALLOWED_HOSTS` - [список допустимых хостов](https://docs.djangoproject.com/en/4.1/ref/settings/#allowed-hosts). По умолчанию - 127.0.0.1, localhost.
- `DB_URL` - конфигурация БД, указывается в [виде URL](https://github.com/jazzband/dj-database-url). Например `postgres://test_user:qwerty123@localhost:5432/test_db`.  Если значение не указано, то при запуске на локальной машине используется SQLite.

## Запуск на локальной машине 
1) [Python3](https://www.python.org/downloads/) должен быть уже установлен.
2) Рекомендуется использовать [virtualenv/venv](https://docs.python.org/3/library/venv.html) для изоляции проекта.
3) Затем используйте pip (или pip3, есть конфликт с Python2) для установки зависимостей:
```python
pip install -r requirements.txt
```
4) Настройте Postgres ([пример](https://www.digitalocean.com/community/tutorials/how-to-install-postgresql-on-ubuntu-20-04-quickstart-ru)) или не указывайте переменную окружения `DB_URL`, тогда будет использоваться SQLite. 
5) Проведите миграции БД:
```python
python manage.py migrate
```
6) Создайте суперпользователя:
```python
python manage.py createsuperuser
```
7) Запустите разработческий сервер ([не годится для production](https://docs.djangoproject.com/en/4.1/ref/django-admin/#runserver)):
```python
python manage.py runserver
```

## Запуск в Docker
1) Установите [Docker](https://docs.docker.com/engine/install/) и [Docker Compose](https://docs.docker.com/compose/install/).
2) Соберите и запустите контейнеры:
```commandline
docker-compose up
```

3) В другом терминале создайте суперпользователя:
```commandline
docker exec -it web python manage.py createsuperuser
```

## Как использовать
### Админ-панель
Админ-панель доступна по адресу http://127.0.0.1:8000/admin. В ней можно добавлять товары, скидки, налоги и собирать заказы.
### API
API имеет два метода:
1) GET /buy/{order_id} - получить `id` сессии [checkout](https://stripe.com/docs/payments/checkout) для выбранного заказа, например:
```commandline
curl -X GET http://localhost:8000/buy/1
```
2) GET /order/{order_id} - получить html-страницу с информацией о заказе и кнопкой на оплату, например:
```commandline
curl -X GET http://localhost:8000/order/1
```

## Цели проекта
Код написан в качестве тестового задания.