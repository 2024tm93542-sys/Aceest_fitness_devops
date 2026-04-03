from flask import Flask
import sqlite3
import os

DB_PATH = os.environ.get('DB_PATH', 'app.db')

def create_app():
    app = Flask(__name__)

    @app.route('/')
    def index():
        return {'message': 'Hello, World!'}

    @app.route('/init_db')
    def init_db():
        conn = sqlite3.connect(DB_PATH)
        cur = conn.cursor()
        cur.execute('''CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, name TEXT)''')
        conn.commit()
        conn.close()
        return {'status': 'initialized'}

    return app
