1. Скачать проект.

git clone https://github.com/Arhipkin7/view_employees

python3 -m venv env

source env/bin/activate

cd view_employees

2. Установка зависимостей

pip3 install requirements.txt

3. Создать базу данных

3.1 Создать роль

CREATE USER test_user WITH password 'test_password';

3.2 Создать базу

CREATE DATABASE test_db;

3.3 Связать БД с ролью

GRANT ALL ON DATABASE  test_db TO test_user

4. Запустить скрипт инициализации

python3 manage.py runscript initialize_db

5. Создать суперпользователя

python3 manage.py createsuperuser

6. Запустить проект 

python3 manage.py runserver

7. Запустить тесты

python3 manage.py test
