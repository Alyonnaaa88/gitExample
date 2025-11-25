import sqlite3
from pathlib import Path
from models import Клиент, Тренер, Занятие, Запись, Администратор, Абонемент

DATABASE = Path(__file__).parent.parent / "db" / "fitness_club.db"

def get_connection():
    return sqlite3.connect(DATABASE)

# Получить клиента по ID
def get_client_by_id(client_id):
    with get_connection() as conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM Клиент WHERE клиент_id = ?", (client_id,))
        row = cur.fetchone()
        if row:
            return Клиент(*row)
        return None

# Получить все записи конкретного клиента (с информацией о занятии)
def get_bookings_by_client(client_id):
    with get_connection() as conn:
        cur = conn.cursor()
        cur.execute("""
            SELECT Запись.*, Занятие.название, Тренер.ФИО 
            FROM Запись
            JOIN Занятие ON Запись.занятие_id = Занятие.занятие_id
            JOIN Тренер ON Занятие.тренер_id = Тренер.тренер_id
            WHERE Запись.клиент_id = ?
        """, (client_id,))
        rows = cur.fetchall()
        return [Запись(row[0], row[1], row[2], row[3], row[4], row[5], row[6]) for row in rows]

# Получить всех клиентов
def get_all_clients():
    with get_connection() as conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM Клиент")
        rows = cur.fetchall()
        return [Клиент(*row) for row in rows]
