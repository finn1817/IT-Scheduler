import sqlite3
from datetime import datetime, timedelta

class DatabaseConnection:
    def __init__(self, db_file='data/schedule.db'):
        self.db_file = db_file
        
    def __enter__(self):
        self.conn = sqlite3.connect(self.db_file)
        self.conn.row_factory = sqlite3.Row
        return self.conn.cursor()
    
    def __exit__(self, type, value, traceback):
        self.conn.commit()
        self.conn.close()

class DatabaseOperations:
    @staticmethod
    def add_workplace(name, hours_open, hours_close):
        with DatabaseConnection() as cursor:
            cursor.execute('''INSERT INTO workplaces (name, hours_open, hours_close)
                            VALUES (?, ?, ?)''', (name, hours_open, hours_close))
            return cursor.lastrowid
    
    @staticmethod
    def get_workplaces():
        with DatabaseConnection() as cursor:
            cursor.execute('SELECT * FROM workplaces')
            return cursor.fetchall()
    
    @staticmethod
    def delete_workplace(workplace_id):
        with DatabaseConnection() as cursor:
            cursor.execute('DELETE FROM workplaces WHERE id = ?', (workplace_id,))
            
    @staticmethod
    def add_worker(workplace_id, first_name, last_name):
        with DatabaseConnection() as cursor:
            cursor.execute('''INSERT INTO workers (workplace_id, first_name, last_name)
                            VALUES (?, ?, ?)''', (workplace_id, first_name, last_name))
            return cursor.lastrowid
    
    @staticmethod
    def get_workers(workplace_id):
        with DatabaseConnection() as cursor:
            cursor.execute('SELECT * FROM workers WHERE workplace_id = ?', (workplace_id,))
            return cursor.fetchall()
    
    @staticmethod
    def update_availability(worker_id, day, start_time, end_time):
        with DatabaseConnection() as cursor:
            cursor.execute('''INSERT OR REPLACE INTO availability 
                            (worker_id, day, start_time, end_time)
                            VALUES (?, ?, ?, ?)''', (worker_id, day, start_time, end_time))
    
    @staticmethod
    def get_availability(worker_id):
        with DatabaseConnection() as cursor:
            cursor.execute('SELECT * FROM availability WHERE worker_id = ?', (worker_id,))
            return cursor.fetchall()
    
    @staticmethod
    def add_schedule(workplace_id, worker_id, date, start_time, end_time):
        with DatabaseConnection() as cursor:
            cursor.execute('''INSERT INTO schedules 
                            (workplace_id, worker_id, date, start_time, end_time)
                            VALUES (?, ?, ?, ?, ?)''', 
                            (workplace_id, worker_id, date, start_time, end_time))
    
    @staticmethod
    def get_schedule(workplace_id, date):
        with DatabaseConnection() as cursor:
            cursor.execute('''SELECT s.*, w.first_name, w.last_name 
                            FROM schedules s
                            JOIN workers w ON s.worker_id = w.id
                            WHERE s.workplace_id = ? AND s.date = ?''', 
                            (workplace_id, date))
            return cursor.fetchall()
