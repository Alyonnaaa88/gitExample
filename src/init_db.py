import sqlite3
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
DATABASE = PROJECT_ROOT / "db" / "fitness_club.db"

def create_tables():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    #Клиент
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Клиент (
        клиент_id INTEGER PRIMARY KEY,
        ФИО TEXT NOT NULL,
        дата_рождения DATE,
        пол TEXT CHECK(пол IN ('М', 'Ж')),
        номер_телефона TEXT NOT NULL
        )
    ''')

    #Тренер
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Тренер (
        тренер_id INTEGER PRIMARY KEY,
        ФИО TEXT NOT NULL,
        специализация TEXT NOT NULL,
        стаж_работы INTEGER,
        контактный_телефон TEXT NOT NULL
        )
    ''')

    #Администратор
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Администратор (
        админ_id INTEGER PRIMARY KEY,
        ФИО TEXT NOT NULL
        )
    ''')

    #Запись, статус занятия: 0-не проведено, 1-проведено
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Запись (
        запись_id INTEGER PRIMARY KEY,
        клиент_id INTEGER,
        занятие_id INTEGER,
        админ_id INTEGER,
        статус_занятия INTEGER CHECK(статус_занятия IN (0, 1)), 
        оценка_от_тренера INTEGER,
        оценка_от_клиента INTEGER,
        FOREIGN KEY (клиент_id) REFERENCES Клиент(клиент_id),
        FOREIGN KEY (занятие_id) REFERENCES Занятие(занятие_id),
        FOREIGN KEY (админ_id) REFERENCES Администратор(админ_id)
        )
    ''')

    #Занятие
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Занятие (
        занятие_id INTEGER PRIMARY KEY,
        название TEXT NOT NULL,
        тренер_id INTEGER,
        дата DATE,
        время_проведения TEXT NOT NULL,
        цена NUMERIC,
        FOREIGN KEY (тренер_id) REFERENCES Тренер(тренер_id)
        )
    ''')

    #Абонемент
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Абонемент (
        абонемент_id INTEGER PRIMARY KEY,
        стоимость NUMERIC,
        клиент_id INTEGER,
        FOREIGN KEY (клиент_id) REFERENCES Клиент(клиент_id)
        )
    ''')


def insert_test_data():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    #Клиенты
    cursor.executemany('INSERT INTO Клиент (клиент_id, ФИО, дата_рождения, пол, номер_телефона) VALUES (?, ?, ?, ?, ?)', [
        (1, 'Никифоров Кирилл Андреевич', '2000-05-15', 'М', '+79261607175'),
        (2, 'Ковалёва София Артемьева', '2002-12-03', 'Ж', '+79906693025')
    ])

    #Тренеры
    cursor.executemany('INSERT INTO Тренер (тренер_id, ФИО, специализация, стаж_работы, контактный_телефон) VALUES (?, ?, ?, ?, ?)', [
        (1, 'Белоусов Илья Степанович', 'силовой фитнес', '7', '+79443425683'),
        (2, 'Ковалёва София Артемьева', 'йога', '13', '+79611963250')
    ])

    #Администратор
    cursor.execute('INSERT INTO Администратор (админ_id, ФИО) VALUES (?, ?)',(1, "Тихонов Демид Русланович")
    )

    #Абонемент
    cursor.execute('INSERT INTO Абонемент (абонемент_id, стоимость, клиент_id) VALUES (?, ?, ?)',(1, 3000.0, 1))

    #Занятия
    cursor.executemany('INSERT INTO Занятие (занятие_id, название, тренер_id, дата, время_проведения, цена) VALUES (?, ?, ?, ?, ?, ?)',
    [(1, 'Утренняя йога', 2, '2025-11-01', '10:00', 650.0),
     (2, 'Силовая тренировка', 1, '2025-11-02','18:00', 700.0)
     ])

    #Запись
    cursor.execute('INSERT INTO Запись (запись_id, клиент_id, занятие_id, админ_id, статус_занятия, оценка_от_тренера, оценка_от_клиента) VALUES (?, ?, ?, ?, ?, ?, ?)',
    (1, 1, 2, 1, 0, None, None))

    conn.commit()
    conn.close()
    print('Тестовые данные добавлены')

if __name__ == "__main__":
    create_tables()
    insert_test_data()
