import sqlite3

def connect_db():
    conn = sqlite3.connect("attendance.db")
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS students(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            roll_no TEXT NOT NULL UNIQUE
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS attendance(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER,
            date TEXT,
            status TEXT,
            FOREIGN KEY(student_id) REFERENCES students(id)
        )
    ''')
    conn.commit()
    conn.close()

def add_student(name, roll_no):
    conn = sqlite3.connect("attendance.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO students (name, roll_no) VALUES (?,?)", (name, roll_no))
    conn.commit()
    conn.close()

def update_student(student_id, name, roll_no):
    conn = sqlite3.connect("attendance.db")
    cursor = conn.cursor()
    cursor.execute("UPDATE students SET name=?, roll_no=? WHERE id=?", (name, roll_no, student_id))
    conn.commit()
    conn.close()

def delete_student(student_id):
    conn = sqlite3.connect("attendance.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM students WHERE id=?", (student_id,))
    cursor.execute("DELETE FROM attendance WHERE student_id=?", (student_id,))
    conn.commit()
    conn.close()

def get_students(search=""):
    conn = sqlite3.connect("attendance.db")
    cursor = conn.cursor()
    if search:
        cursor.execute("SELECT * FROM students WHERE name LIKE ? OR roll_no LIKE ?", ('%'+search+'%', '%'+search+'%'))
    else:
        cursor.execute("SELECT * FROM students")
    data = cursor.fetchall()
    conn.close()
    return data

def mark_attendance(student_id, date, status):
    conn = sqlite3.connect("attendance.db")
    cursor = conn.cursor()
    # Check if already marked
    cursor.execute("SELECT * FROM attendance WHERE student_id=? AND date=?", (student_id, date))
    if cursor.fetchone():
        cursor.execute("UPDATE attendance SET status=? WHERE student_id=? AND date=?", (status, student_id, date))
    else:
        cursor.execute("INSERT INTO attendance (student_id, date, status) VALUES (?,?,?)", (student_id, date, status))
    conn.commit()
    conn.close()

def get_attendance(search=""):
    conn = sqlite3.connect("attendance.db")
    cursor = conn.cursor()
    query = '''
        SELECT students.roll_no, students.name, attendance.date, attendance.status
        FROM attendance
        JOIN students ON attendance.student_id = students.id
    '''
    if search:
        query += " WHERE students.name LIKE ? OR students.roll_no LIKE ?"
        cursor.execute(query, ('%'+search+'%', '%'+search+'%'))
    else:
        cursor.execute(query)
    data = cursor.fetchall()
    conn.close()
    return data
