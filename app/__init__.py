from flask import Flask, request, jsonify
import sqlite3
import os
from datetime import date

DB_PATH = os.environ.get("DB_PATH", "aceest_fitness.db")


def get_db():
    return sqlite3.connect(DB_PATH)


def init_db():
    conn = get_db()
    cur = conn.cursor()

    # Users
    cur.execute("""
    CREATE TABLE IF NOT EXISTS users (
        username TEXT PRIMARY KEY,
        password TEXT,
        role TEXT
    )
    """)

    # Clients
    cur.execute("""
    CREATE TABLE IF NOT EXISTS clients (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT UNIQUE,
        age INTEGER,
        height REAL,
        weight REAL,
        program TEXT,
        calories INTEGER,
        target_weight REAL,
        target_adherence INTEGER,
        membership_status TEXT,
        membership_end TEXT
    )
    """)

    # Progress
    cur.execute("""
    CREATE TABLE IF NOT EXISTS progress (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        client_name TEXT,
        week TEXT,
        adherence INTEGER
    )
    """)

    # Workouts
    cur.execute("""
    CREATE TABLE IF NOT EXISTS workouts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        client_name TEXT,
        date TEXT,
        workout_type TEXT,
        duration_min INTEGER,
        notes TEXT
    )
    """)

    # Metrics
    cur.execute("""
    CREATE TABLE IF NOT EXISTS metrics (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        client_name TEXT,
        date TEXT,
        weight REAL,
        waist REAL,
        bodyfat REAL
    )
    """)

    # Default admin
    cur.execute("SELECT * FROM users WHERE username='admin'")
    if not cur.fetchone():
        cur.execute("INSERT INTO users VALUES ('admin','admin','Admin')")

    conn.commit()
    conn.close()


def create_app():
    app = Flask(__name__)

    init_db()

    @app.route("/")
    def home():
        return {"message": "ACEest Fitness API running"}

    # ---------------- LOGIN ----------------
    @app.route("/login", methods=["POST"])
    def login():
        data = request.json
        username = data.get("username")
        password = data.get("password")

        conn = get_db()
        cur = conn.cursor()

        cur.execute(
            "SELECT role FROM users WHERE username=? AND password=?",
            (username, password)
        )

        row = cur.fetchone()
        conn.close()

        if row:
            return {"status": "success", "role": row[0]}
        return {"status": "failed"}, 401

    # ---------------- CLIENTS ----------------
    @app.route("/clients", methods=["GET"])
    def list_clients():
        conn = get_db()
        cur = conn.cursor()

        cur.execute("SELECT name FROM clients ORDER BY name")
        clients = [r[0] for r in cur.fetchall()]

        conn.close()
        return jsonify(clients)

    @app.route("/clients", methods=["POST"])
    def add_client():
        data = request.json
        name = data.get("name")

        conn = get_db()
        cur = conn.cursor()

        cur.execute(
            "INSERT OR IGNORE INTO clients (name, membership_status) VALUES (?,?)",
            (name, "Active")
        )

        conn.commit()
        conn.close()

        return {"status": "client added"}

    # ---------------- WORKOUTS ----------------
    @app.route("/workouts/<client>", methods=["GET"])
    def get_workouts(client):
        conn = get_db()
        cur = conn.cursor()

        cur.execute("""
        SELECT date, workout_type, duration_min, notes
        FROM workouts
        WHERE client_name=?
        ORDER BY date DESC
        """, (client,))

        rows = cur.fetchall()
        conn.close()

        workouts = [
            {
                "date": r[0],
                "type": r[1],
                "duration": r[2],
                "notes": r[3]
            }
            for r in rows
        ]

        return jsonify(workouts)

    @app.route("/workouts", methods=["POST"])
    def add_workout():
        data = request.json

        conn = get_db()
        cur = conn.cursor()

        cur.execute("""
        INSERT INTO workouts
        (client_name, date, workout_type, duration_min, notes)
        VALUES (?,?,?,?,?)
        """, (
            data["client"],
            data.get("date", date.today().isoformat()),
            data["type"],
            data["duration"],
            data.get("notes", "")
        ))

        conn.commit()
        conn.close()

        return {"status": "workout saved"}

    # ---------------- MEMBERSHIP ----------------
    @app.route("/membership/<client>")
    def check_membership(client):

        conn = get_db()
        cur = conn.cursor()

        cur.execute("""
        SELECT membership_status, membership_end
        FROM clients
        WHERE name=?
        """, (client,))

        row = cur.fetchone()
        conn.close()

        if not row:
            return {"error": "client not found"}, 404

        return {
            "membership_status": row[0],
            "membership_end": row[1]
        }

    return app