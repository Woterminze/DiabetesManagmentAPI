import sqlite3

DATABASE = 'glucose.db'

def get_connection():
    return sqlite3.connect(DATABASE)

def init_database():
    connect = get_connection()
    connect = sqlite3.connect('glucose.db')
    cursor = connect.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS glucose_records (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        glucose_level FLOAT NOT NULL,
        glucose_measure STRING,
        measurement_time DATETIME NOT NULL,
        notes TEXT
        )
    ''')
    connect.commit()
    connect.close()

def insert_records(user_id, glucose_level, glucose_measure, measurement_time, notes):
    connect = get_connection()
    cursor = connect.cursor()
    query = '''
        INSERT INTO glucose_records (user_id, glucose_level, glucose_measure, measurement_time, notes) VALUES (?, ?, ?, ?, ?)
    '''
    cursor.execute(query, (user_id, glucose_level, glucose_measure, measurement_time, notes))
    connect.commit()
    connect.close()

def read_records():
    connect = get_connection()
    cursor = connect.cursor()
    cursor.execute('SELECT * FROM glucose_records')
    records = cursor.fetchall()
    connect.close()
    return records








