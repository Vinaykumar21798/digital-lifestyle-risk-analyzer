import sqlite3
import pandas as pd
from datetime import date, timedelta
import random

DB_NAME = "health_data.db"


def create_table():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS health_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT NOT NULL,
            sleep_hours REAL,
            water_liters REAL,
            exercise_minutes INTEGER,
            mood_score INTEGER CHECK(mood_score BETWEEN 1 AND 5),
            steps INTEGER,
            screen_time REAL
        )
    """)

    conn.commit()
    conn.close()


def insert_data(date_value, sleep, water, exercise, mood, steps, screen):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO health_logs
        (date, sleep_hours, water_liters, exercise_minutes, mood_score, steps, screen_time)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (date_value, sleep, water, exercise, mood, steps, screen))

    conn.commit()
    conn.close()


def generate_dummy_data(days=14):
    for i in range(days):
        dummy_date = date.today() - timedelta(days=i)

        sleep = round(random.uniform(5.5, 8.5), 1)
        water = round(random.uniform(1.5, 3.5), 1)
        exercise = random.randint(0, 60)
        mood = random.randint(2, 5)
        steps = random.randint(3000, 12000)
        screen = round(random.uniform(3, 8), 1)

        insert_data(str(dummy_date), sleep, water, exercise, mood, steps, screen)


def fetch_data():
    conn = sqlite3.connect(DB_NAME)

    df = pd.read_sql_query(
        "SELECT * FROM health_logs ORDER BY date ASC",
        conn
    )

    conn.close()
    return df