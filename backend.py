from connections import DatabaseManager
from availability import AvailabilityManager
from datetime import datetime, timedelta

class ScheduleManager:
    def __init__(self, db_file='data/schedule.db'):
        self.db = DatabaseManager(db_file)
        self.availability = AvailabilityManager(db_file)

    def add_workplace(self, name, hours_open, hours_close):
        # correct the timing formatting
        try:
            datetime.strptime(hours_open, '%H:%M')
            datetime.strptime(hours_close, '%H:%M')
        except ValueError:
            return False
        return self.db.add_workplace(name, hours_open, hours_close)

    def add_worker(self, workplace_id, first_name, last_name):
        if not first_name or not last_name:
            return False
        return self.db.add_worker(workplace_id, first_name, last_name)

    def set_availability(self, worker_id, day, start_time, end_time):
        try:
            datetime.strptime(start_time, '%H:%M')
            datetime.strptime(end_time, '%H:%M')
        except ValueError:
            return False
        return self.availability.set_availability(worker_id, day, start_time, end_time)

    def add_schedule(self, workplace_id, worker_id, date, start_time, end_time):
        try:
            datetime.strptime(date, '%Y-%m-%d')
            datetime.strptime(start_time, '%H:%M')
            datetime.strptime(end_time, '%H:%M')
        except ValueError:
            return False
        return self.db.add_schedule(workplace_id, worker_id, date, start_time, end_time)

    def get_available_workers(self, workplace_id, date, start_time, end_time):
        all_workers = self.db.get_workers(workplace_id)
        available_workers = []
        
        day_of_week = datetime.strptime(date, '%Y-%m-%d').strftime('%A')
        
        for worker in all_workers:
            availability = self.availability.get_availability(worker['id'], day_of_week)
            if availability:
                for slot in availability:
                    if slot['start_time'] <= start_time and slot['end_time'] >= end_time:
                        available_workers.append(worker)
                        break
                        
        return available_workers
