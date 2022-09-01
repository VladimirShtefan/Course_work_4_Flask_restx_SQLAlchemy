# Описание
Python v3.10
### Проект Flask + SQLAlchemy + Flask-RESTX
### Подготовка и запуск
1. Создать, активировать venv:  
**python -m vevn vevn**  
**source venv/bin/activate**
2. Установить зависимости:  
**pip install -r requirements.txt**
3. Создать при необходимости базу данных по пути прописанному в app/constants.py DATA_BASE_PATH.  
Можно воспользоваться готовой базой, для этого необходимо выполнить python3 create_tables.py для создания таблиц 
и python3 load_fixtures.py для заполнения данными.
4. Запуск проекта в режиме разработки:  
**export FLASK_ENV=development,  
export FLASK_APP=run.py,  
flask run --host='0.0.0.0' --port=5000.**

### Для запуска тестов используйте:
**pytest --cov-report term-missing --cov=app tests/** 

