import sqlite3
from datetime import datetime

class DatabaseConnection:
    def __init__(self, db_file='data/schedule.db'):
        self.db_file = db_file

    def __enter__(self):
        self.conn = sqlite3.connect(self.db_file)
        self.conn.row_factory = sqlite3.Row
        return self.conn.cursor()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.conn.commit()
        self.conn.close()

class DatabaseManager:
    def __init__(self, db_file='data/schedule.db'):
        self.db_file = db_file

    def add_workplace(self, name, hours_open, hours_close):
        try:
            with DatabaseConnection(self.db_file) as cursor:
                cursor.execute('''
                    INSERT INTO workplaces (name, hours_open, hours_close)
                    VALUES (?, ?, ?)
                ''', (name, hours_open, hours_close))
            return True
        except Exception as e:
            print(f"Error adding workplace: {e}")
            return False

    def add_worker(self, workplace_id, first_name, last_name):
        try:
            with DatabaseConnection(self.db_file) as cursor:
                cursor.execute('''
                    INSERT INTO workers (workplace_id, first_name, last_name)
                    VALUES (?, ?, ?)
                ''', (workplace_id, first_name, last_name))
            return True
        except Exception as e:
            print(f"Error adding worker: {e}")
            return False

    def get_workplaces(self):
        with DatabaseConnection(self.db_file) as cursor:
            cursor.execute('SELECT * FROM workplaces')
            return [dict(row) for row in cursor.fetchall()]

    def get_workers(self, workplace_id=None):
        with DatabaseConnection(self.db_file) as cursor:
            if workplace_id is not None:
                cursor.execute('SELECT * FROM workers WHERE workplace_id = ?', (workplace_id,))
            else:
                cursor.execute('SELECT * FROM workers')
            return [dict(row) for row in cursor.fetchall()]

    def add_schedule(self, workplace_id, worker_id, date, start_time, end_time):
        try:
            with DatabaseConnection(self.db_file) as cursor:
                cursor.execute('''
                    INSERT INTO schedules (workplace_id, worker_id, date, start_time, end_time)
                    VALUES (?, ?, ?, ?, ?)
                ''', (workplace_id, worker_id, date, start_time, end_time))
            return True
        except Exception as e:
            print(f"Error adding schedule: {e}")
            return False

    def get_schedules(self, workplace_id=None, worker_id=None, date=None):
        with DatabaseConnection(self.db_file) as cursor:
            query = 'SELECT * FROM schedules WHERE 1=1'
            params = []
            
            if workplace_id:
                query += ' AND workplace_id = ?'
                params.append(workplace_id)
            if worker_id:
                query += ' AND worker_id = ?'
                params.append(worker_id)
            if date:
                query += ' AND date = ?'
                params.append(date)
                
            cursor.execute(query, params)
            return [dict(row) for row in cursor.fetchall()]

    def delete_workplace(self, workplace_id):
        try:
            with DatabaseConnection(self.db_file) as cursor:
                cursor.execute('DELETE FROM workplaces WHERE id = ?', (workplace_id,))
            return True
        except Exception as e:
            print(f"Error deleting workplace: {e}")
            return False

    def delete_worker(self, worker_id):
        try:
            with DatabaseConnection(self.db_file) as cursor:
                cursor.execute('DELETE FROM workers WHERE id = ?', (worker_id,))
            return True
        except Exception as e:
            print(f"Error deleting worker: {e}")
            return False
