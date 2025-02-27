import tkinter as tk
from tkinter import ttk, messagebox
from backend import ScheduleManager
from availability import AvailabilityManager
from datetime import datetime, timedelta

class ScheduleApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Schedule Manager")
        self.schedule_manager = ScheduleManager()
        self.availability_manager = AvailabilityManager()
        
        # create main frame
        self.main_frame = ttk.Frame(root, padding="10")
        self.main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # create workplace section
        ttk.Label(self.main_frame, text="Workplaces").grid(row=0, column=0, pady=5)
        self.workplace_list = tk.Listbox(self.main_frame, height=5)
        self.workplace_list.grid(row=1, column=0, columnspan=2, pady=5)
        
        # buttons
        ttk.Button(self.main_frame, text="Add Workplace", 
                   command=self.add_workplace_dialog).grid(row=2, column=0, pady=5)
        ttk.Button(self.main_frame, text="Delete Workplace", 
                   command=self.delete_workplace).grid(row=2, column=1, pady=5)
        
        # workers section
        ttk.Label(self.main_frame, text="Workers").grid(row=3, column=0, pady=5)
        self.worker_list = tk.Listbox(self.main_frame, height=5)
        self.worker_list.grid(row=4, column=0, columnspan=2, pady=5)
        
        ttk.Button(self.main_frame, text="Add Worker", 
                   command=self.add_worker_dialog).grid(row=5, column=0, pady=5)
        ttk.Button(self.main_frame, text="Set Availability", 
                   command=self.set_availability_dialog).grid(row=5, column=1, pady=5)
        
        # schedule section
        ttk.Button(self.main_frame, text="Create Schedule", 
                   command=self.create_schedule_dialog).grid(row=6, column=0, pady=5)
        ttk.Button(self.main_frame, text="View Schedule", 
                   command=self.view_schedule_dialog).grid(row=6, column=1, pady=5)
        
        self.refresh_workplaces()
    
    def refresh_workplaces(self):
        self.workplace_list.delete(0, tk.END)
        workplaces = self.schedule_manager.db.get_workplaces()
        for workplace in workplaces:
            self.workplace_list.insert(tk.END, workplace['name'])
    
    def add_workplace_dialog(self):
        dialog = tk.Toplevel(self.root)
        dialog.title("Add Workplace")
        
        ttk.Label(dialog, text="Name:").grid(row=0, column=0, pady=5)
        name_entry = ttk.Entry(dialog)
        name_entry.grid(row=0, column=1, pady=5)
        
        ttk.Label(dialog, text="Opening Time (HH:MM):").grid(row=1, column=0, pady=5)
        open_entry = ttk.Entry(dialog)
        open_entry.grid(row=1, column=1, pady=5)
        
        ttk.Label(dialog, text="Closing Time (HH:MM):").grid(row=2, column=0, pady=5)
        close_entry = ttk.Entry(dialog)
        close_entry.grid(row=2, column=1, pady=5)
        
        def save():
            name = name_entry.get()
            hours_open = open_entry.get()
            hours_close = close_entry.get()
            
            if self.schedule_manager.add_workplace(name, hours_open, hours_close):
                self.refresh_workplaces()
                dialog.destroy()
            else:
                messagebox.showerror("Error", "Invalid input")
        
        ttk.Button(dialog, text="Save", command=save).grid(row=3, column=0, columnspan=2, pady=5)
    
    def delete_workplace(self):
        selection = self.workplace_list.curselection()
        if selection:
            workplace = self.schedule_manager.db.get_workplaces()[selection[0]]
            self.schedule_manager.db.delete_workplace(workplace['id'])
            self.refresh_workplaces()
    
    # Add in any other dialog methods here (add_worker_dialog, set_availability_dialog, etc.)
    
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    root = tk.Tk()
    app = ScheduleApp(root)
    app.run()
