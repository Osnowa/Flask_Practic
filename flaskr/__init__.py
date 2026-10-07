import os

from flask import Flask

# Фабрика создания приложений (преимущества: можно создать неограниченное кол-во приложений (для тестов и т.д.))
def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True) # Создание экз класса Flask

    app.config.from_mapping( # задаем параметры конфигурации
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'), # куда сохраняем файл данных SQLite
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        # Переопределяет конфигурацию по умолчанию значениями, взятыми из config.py файла в папке экземпляра, если он существует. 
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    os.makedirs(app.instance_path, exist_ok=True)

    # a simple page that says hello
    @app.route('/hello')
    def hello():
        return 'Hello, World!'

    # регистрация функций
    from . import db
    db.init_app(app)

    return app