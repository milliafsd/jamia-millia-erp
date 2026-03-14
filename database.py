import sqlite3

DB_NAME = "jamia.db"

def connect():
    return sqlite3.connect(DB_NAME, check_same_thread=False)

# 1. ٹیبلز بنانا (پہلے والا کوڈ)
def init_db():
    conn = connect()
    c = conn.cursor()
    c.execute("""
    CREATE TABLE IF NOT EXISTS teachers(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        name TEXT NOT NULL,
        password TEXT NOT NULL
    )""")
    c.execute("""
    CREATE TABLE IF NOT EXISTS students(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        father TEXT,
        darja TEXT,
        teacher_id INTEGER,
        FOREIGN KEY (teacher_id) REFERENCES teachers(id)
    )""")
    conn.commit()
    conn.close()

# 2. استاد کا اندراج (Add Teacher)
def add_teacher(username, name, password):
    conn = connect()
    c = conn.cursor()
    try:
        c.execute("INSERT INTO teachers (username, name, password) VALUES (?, ?, ?)", 
                  (username, name, password))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False # اگر یوزر نیم پہلے سے موجود ہو
    finally:
        conn.close()

# 3. طالب علم کا اندراج (Add Student)
def add_student(name, father, darja, teacher_id):
    conn = connect()
    c = conn.cursor()
    c.execute("INSERT INTO students (name, father, darja, teacher_id) VALUES (?, ?, ?, ?)", 
              (name, father, darja, teacher_id))
    conn.commit()
    conn.close()

# 4. تمام اساتذہ کی لسٹ دیکھنا
def view_teachers():
    conn = connect()
    c = conn.cursor()
    c.execute("SELECT id, name, username FROM teachers")
    data = c.fetchall()
    conn.close()
    return data

# 5. تمام طلباء کی لسٹ دیکھنا
def view_students():
    conn = connect()
    c = conn.cursor()
    # یہاں ہم 'Join' استعمال کر رہے ہیں تاکہ استاد کا نام بھی نظر آئے
    c.execute("""
        SELECT students.id, students.name, students.father, students.darja, teachers.name 
        FROM students 
        LEFT JOIN teachers ON students.teacher_id = teachers.id
    """)
    data = c.fetchall()
    conn.close()
    return data

# 6. کسی طالب علم کو حذف کرنا
def delete_student(student_id):
    conn = connect()
    c = conn.cursor()
    c.execute("DELETE FROM students WHERE id=?", (student_id,))
    conn.commit()
    conn.close()
# database.py میں یہ حصہ شامل کریں

def init_db():
    conn = connect()
    c = conn.cursor()
    # ... پرانے ٹیبلز کے ساتھ یہ نیا ٹیبل بھی شامل کریں ...
    c.execute("""
    CREATE TABLE IF NOT EXISTS hifz_record(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        student_id INTEGER,
        date TEXT,
        sabaq TEXT,          -- نیا سبق (مثلاً پارہ 1، رکوع 2)
        sabqi TEXT,         -- سبقی (پچھلے چند اسباق)
        manzil TEXT,        -- منزل (پچھلا پڑھا ہوا حصہ)
        mistakes INTEGER,    -- غلطی
        hesitation INTEGER,  -- اٹکن
        status TEXT,         -- حاضر / ناغہ
        FOREIGN KEY (student_id) REFERENCES students(id)
    )""")
    conn.commit()
    conn.close()

# حفظ کا ریکارڈ محفوظ کرنے کا فنکشن
def add_hifz_entry(student_id, date, sabaq, sabqi, manzil, mistakes, hesitation, status):
    conn = connect()
    c = conn.cursor()
    c.execute("""INSERT INTO hifz_record 
                 (student_id, date, sabaq, sabqi, manzil, mistakes, hesitation, status) 
                 VALUES (?, ?, ?, ?, ?, ?, ?, ?)""", 
              (student_id, date, sabaq, sabqi, manzil, mistakes, hesitation, status))
    conn.commit()
    conn.close()
