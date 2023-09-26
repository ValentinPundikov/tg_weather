import sqlite3

def createDB():
    conn = sqlite3.connect("DataBase.db")
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS data (id INTEGER, lat TEXT, lon INTEGER)''',())
    conn.close()


def check_user(user_id):
    conn = sqlite3.connect("DataBase.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM data WHERE id=?", (user_id,))
    existing_value = cursor.fetchone()
    if existing_value is None:
        add_user(user_id)
    else:
        pass


def add_user(user_id):
    conn = sqlite3.connect("DataBase.db")
    cursor = conn.cursor()
    cursor.execute('INSERT INTO data (id) VALUES (?)',(user_id,))
    conn.commit()
def add_lat_lon(user_id,lat,lon):
    conn = sqlite3.connect("DataBase.db")
    cursor = conn.cursor()
    cursor.execute('UPDATE data SET lat=? WHERE id = ?',(lat,user_id,))
    cursor.execute('UPDATE data SET lon=? WHERE id = ?', (lon, user_id,))
    conn.commit()

def get_lat(user_id):
    conn = sqlite3.connect("DataBase.db")
    cursor = conn.cursor()
    cursor.execute('''SELECT lat FROM data WHERE id = ?''',(user_id,))
    lat = cursor.fetchone()
    return lat

def get_lon(user_id):
    conn = sqlite3.connect("DataBase.db")
    cursor = conn.cursor()
    cursor.execute('''SELECT lon FROM data WHERE id = ?''',(user_id,))
    lon = cursor.fetchone()
    return lon