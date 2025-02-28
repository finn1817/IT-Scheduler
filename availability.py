from connections import DatabaseConnection

class AvailabilityManager:
    def __init__(self, db_file='data/schedule.db'):
        self.db_file = db_file

    def set_availability(self, worker_id, day, start_time, end_time):
        try:
            with DatabaseConnection(self.db_file) as cursor:
                # deleting existing availability for this worker and day
                cursor.execute('''
                    DELETE FROM availability 
                    WHERE worker_id = ? AND day = ?
                ''', (worker_id, day))
                
                # adding in new availability
                cursor.execute('''
                    INSERT INTO availability (worker_id, day, start_time, end_time)
                    VALUES (?, ?, ?, ?)
                ''', (worker_id, day, start_time, end_time))
            return True
        except Exception as e:
            print(f"Error setting availability: {e}")
            return False

    def get_availability(self, worker_id=None, day=None):
        with DatabaseConnection(self.db_file) as cursor:
            query = 'SELECT * FROM availability WHERE 1=1'
            params = []
            
            if worker_id:
                query += ' AND worker_id = ?'
                params.append(worker_id)
            if day:
                query += ' AND day = ?'
                params.append(day)
                
            cursor.execute(query, params)
            return [dict(row) for row in cursor.fetchall()]

    def delete_availability(self, worker_id, day=None):
        try:
            with DatabaseConnection(self.db_file) as cursor:
                if day:
                    cursor.execute('''
                        DELETE FROM availability 
                        WHERE worker_id = ? AND day = ?
                    ''', (worker_id, day))
                else:
                    cursor.execute('''
                        DELETE FROM availability 
                        WHERE worker_id = ?
                    ''', (worker_id,))
            return True
        except Exception as e:
            print(f"Error deleting availability: {e}")
            return False
