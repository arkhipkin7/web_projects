# Foobar

Parser CIAN

## Installation
```bash
$ mkdir test_project
$ git clone https://github.com/arkhipkin7/test_project
$ cd test_project
$ python3 -m venv env
$ source env/bin/activate
$ pip install requirements.txt
```
## Настройка бд
```sql
CREATE USER user_test WITH password 'pass_test';
CREATE DATABASE db_test;
GRANT ALL ON DATABASE db_test TO user_test
```
## Выполнить миграции
```bash
$ python3 manage.py migrate
```
## Создать пользователя
```
$ python3 manage.py createsuperuser 
```

## Выполнить скрип парсинга с параметрами (url - ссылка на страницу для парсинга, pages - кол-во страниц для сканирвоания)
```bash
$ python3 manage parse_cian.py 'url' pages
```

## Run server
```bash
$ python3 manage runserver
```

## Резульатат находится по адресу
```http
127.0.0.1:8000/products/{id_serch}/
```
