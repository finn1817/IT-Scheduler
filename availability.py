from connections import DatabaseOperations
from datetime import datetime, timedelta

class AvailabilityManager:
    def __init__(self):
        self.db = DatabaseOperations()
    
    def set_availability(self, worker_id, day, start_time, end_time):
        """Set availability for a worker on a specific day"""
        try:
            # Validate time format
            datetime.strptime(start_time, '%H:%M')
            datetime.strptime(end_time, '%H:%M')
            
            if start_time >= end_time:
                raise ValueError("Start time must be before end time")
            
            self.db.update_availability(worker_id, day, start_time, end_time)
            return True
        except ValueError as e:
            print(f"Error setting availability: {str(e)}")
            return False
    
    def get_worker_availability(self, worker_id):
        """Get all availability entries for a worker"""
        return self.db.get_availability(worker_id)
    
    def is_worker_available(self, worker_id, date, start_time, end_time):
        """Check if a worker is available for a specific time slot"""
        day_of_week = datetime.strptime(date, '%Y-%m-%d').strftime('%A')
        availability = self.get_worker_availability(worker_id)
        
        for avail in availability:
            if avail['day'] == day_of_week:
                if avail['start_time'] <= start_time and avail['end_time'] >= end_time:
                    return True
        return False
    
    def get_available_workers(self, workplace_id, date, start_time, end_time):
        """Get all available workers for a specific time slot"""
        workers = self.db.get_workers(workplace_id)
        available_workers = []
        
        for worker in workers:
            if self.is_worker_available(worker['id'], date, start_time, end_time):
                available_workers.append(worker)
        
        return available_workers
