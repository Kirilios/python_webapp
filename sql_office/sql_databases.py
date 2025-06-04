'''Ссылка на схему БД: https://drawdb.vercel.app/editor?shareId=9e9f40e4afe942771fa2f31dfd6497c7'''

import sqlite3

class Database:
    def __init__(self, db_name='employees_tables.db'):
        """Инициализируем класс"""
        self.db_name = db_name
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()

    def initialize_tables(self):
        """Создаём тут таблицы через cursor.execute, если они ещё не существуют"""
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS departments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE
        )
        ''')

        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS employees (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            full_name TEXT NOT NULL,
            birth_date DATE NOT NULL,
            position TEXT NOT NULL,
            phone TEXT,
            email TEXT,
            department_id INTEGER,
            manager_id INTEGER,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (department_id) REFERENCES departments(id), 
            FOREIGN KEY (manager_id) REFERENCES employees(id) 
        )
        ''')

        self.conn.commit()

    def insert_department(self, name):
        """Добавляет новый департамент. Возвращает True, если добавлен, False если уже есть"""
        try:
            self.cursor.execute('''
                INSERT INTO departments (name) VALUES (?)
            ''', (name,))
            self.conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False

    def insert_employee(self, full_name, birth_date, position,
                        phone, email, department_id, manager_id):
        """Добавление одного сотрудника"""
        self.cursor.execute('''
            INSERT INTO employees (
                full_name, birth_date, position, phone, email,
                department_id, manager_id
            ) VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (
            full_name, birth_date, position, phone, email,
            department_id if department_id else None,
            manager_id if manager_id else None
        ))
        self.conn.commit()

    def get_all_departments(self):
        self.cursor.execute("SELECT id, name FROM departments")
        return self.cursor.fetchall()

    def get_employees_by_department(self, department_id):
        self.cursor.execute('''
            SELECT id, full_name, position FROM employees WHERE department_id = ?
        ''', (department_id,))
        return self.cursor.fetchall()

    def get_subordinates_by_manager(self, manager_id):
        self.cursor.execute('''
            SELECT id, full_name, position FROM employees WHERE manager_id = ?
        ''', (manager_id,))
        return self.cursor.fetchall()

    def close(self):
        """Закрывает соединение"""
        self.conn.close()