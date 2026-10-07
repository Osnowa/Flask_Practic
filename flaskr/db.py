import sqlite3
from datetime import datetime

import click
from flask import current_app, g

# g - спец обьект, уникальный для каждого запроса
def get_db():
    if "db" not in g: # проверка, уже открывали в этом контексте ? 
        g.db = sqlite3.connect( # нет, создаем соединение с бд! 
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row # верни строки, которые ведут себя как словари 

    return g.db


def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()

def init_db():
    db = get_db() # Соединение с БД

    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))

@click.command('init_db')
def init_db_command():
    init_db()
    click.echo('Инициализация DB')

sqlite3.register_converter(
    "timestamp", lambda v: datetime.fromisoformat(v.decode())
)

# Принимает приложения и выполняет регистрацию
def init_app(app):
    "Регистрация команд"
    app.teardown_appcontext(close_db) # Указываем, вызвать эту функцию при выполнении очистки после возврата ответа 
    app.cli.add_command(init_db_command) # добавление новой команды

