from connections import DatabaseOperations
from availability import AvailabilityManager
from datetime import datetime, timedelta

class ScheduleManager:
    def __init__(self):
        self.db = DatabaseOperations()
        self.availability = AvailabilityManager()
    
    def add_workplace(self, name, hours_open, hours_close):
        """Add a new workplace"""
        try:
            # validate the time format
            datetime.strptime(hours_open, '%H:%M')
            datetime.strptime(hours_close, '%H:%M')
            
            if hours_open >= hours_close:
                raise ValueError("Opening time must be before closing time")
            
            return self.db.add_workplace(name, hours_open, hours_close)
        except ValueError as e:
            print(f"Error adding workplace: {str(e)}")
            return None
    
    def add_worker(self, workplace_id, first_name, last_name):
        """Add a new worker"""
        if not first_name or not last_name:
            print("Error: First name and last name are required")
            return None
        
        return self.db.add_worker(workplace_id, first_name, last_name)
    
    def create_schedule(self, workplace_id, date, shifts):
        """Create a schedule for a specific date"""
        try:
            date_obj = datetime.strptime(date, '%Y-%m-%d')
            
            for shift in shifts:
                worker_id = shift['worker_id']
                start_time = shift['start_time']
                end_time = shift['end_time']
                
                # check on worker availability
                if not self.availability.is_worker_available(worker_id, date, start_time, end_time):
                    raise ValueError(f"Worker {worker_id} is not available for this shift")
                
                # check for any schedule conflicts
                existing_schedule = self.db.get_schedule(workplace_id, date)
                for existing_shift in existing_schedule:
                    if (existing_shift['worker_id'] == worker_id and
                        not (end_time <= existing_shift['start_time'] or 
                             start_time >= existing_shift['end_time'])):
                        raise ValueError(f"Schedule conflict for worker {worker_id}")
                
                self.db.add_schedule(workplace_id, worker_id, date, start_time, end_time)
            
            return True
        except ValueError as e:
            print(f"Error creating schedule: {str(e)}")
            return False
    
    def get_schedule(self, workplace_id, date):
        """Get schedule for a specific date"""
        return self.db.get_schedule(workplace_id, date)
