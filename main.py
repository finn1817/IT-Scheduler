import tkinter as tk
from tkinter import ttk, messagebox
from backend import ScheduleManager
from datetime import datetime, timedelta
import calendar

class ScheduleApp:
    def __init__(self, root):
        self.root = root
        self.root.title("IT Schedule Manager")
        self.schedule_manager = ScheduleManager()
        
        # making the main frames
        self.workplace_frame = ttk.LabelFrame(root, text="Workplaces", padding="5")
        self.workplace_frame.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")
        
        self.worker_frame = ttk.LabelFrame(root, text="Workers", padding="5")
        self.worker_frame.grid(row=0, column=1, padx=5, pady=5, sticky="nsew")
        
        self.schedule_frame = ttk.LabelFrame(root, text="Schedule", padding="5")
        self.schedule_frame.grid(row=0, column=2, padx=5, pady=5, sticky="nsew")

        # workplace section
        self.setup_workplace_section()
        
        # worker section
        self.setup_worker_section()
        
        # schedule section
        self.setup_schedule_section()
        
        # configuring grid weights
        root.grid_columnconfigure(0, weight=1)
        root.grid_columnconfigure(1, weight=1)
        root.grid_columnconfigure(2, weight=1)
        root.grid_rowconfigure(0, weight=1)

        # first / start update
        self.update_workplace_list()

    def setup_workplace_section(self):
        # workplace list
        self.workplace_list = tk.Listbox(self.workplace_frame, height=10)
        self.workplace_list.grid(row=0, column=0, columnspan=2, sticky="nsew")
        self.workplace_list.bind('<<ListboxSelect>>', self.on_workplace_select)
        
        # the "add workplace" button
        ttk.Button(self.workplace_frame, text="Add Workplace", 
                  command=self.add_workplace_dialog).grid(row=1, column=0, pady=5)
        
        # the "delete workplace" button
        ttk.Button(self.workplace_frame, text="Delete Workplace",
                  command=self.delete_workplace).grid(row=1, column=1, pady=5)

    def setup_worker_section(self):
        # worker list
        self.worker_list = tk.Listbox(self.worker_frame, height=10)
        self.worker_list.grid(row=0, column=0, columnspan=2, sticky="nsew")
        
        # add worker button
        ttk.Button(self.worker_frame, text="Add Worker",
                  command=self.add_worker_dialog).grid(row=1, column=0, pady=5)
        
        # delete worker button
        ttk.Button(self.worker_frame, text="Delete Worker",
                  command=self.delete_worker).grid(row=1, column=1, pady=5)
        
        # set availability button
        ttk.Button(self.worker_frame, text="Set Availability",
                  command=self.set_availability_dialog).grid(row=2, column=0, columnspan=2, pady=5)

    def setup_schedule_section(self):
        # date selection
        ttk.Label(self.schedule_frame, text="Date:").grid(row=0, column=0, pady=5)
        self.date_entry = ttk.Entry(self.schedule_frame)
        self.date_entry.grid(row=0, column=1, pady=5)
        self.date_entry.insert(0, datetime.now().strftime('%Y-%m-%d'))
        
        # time selection
        ttk.Label(self.schedule_frame, text="Start Time:").grid(row=1, column=0, pady=5)
        self.start_time_entry = ttk.Entry(self.schedule_frame)
        self.start_time_entry.grid(row=1, column=1, pady=5)
        
        ttk.Label(self.schedule_frame, text="End Time:").grid(row=2, column=0, pady=5)
        self.end_time_entry = ttk.Entry(self.schedule_frame)
        self.end_time_entry.grid(row=2, column=1, pady=5)
        
        # schedule buttons
        ttk.Button(self.schedule_frame, text="View Available Workers",
                  command=self.view_available_workers).grid(row=3, column=0, columnspan=2, pady=5)
        
        ttk.Button(self.schedule_frame, text="Add Schedule",
                  command=self.add_schedule).grid(row=4, column=0, columnspan=2, pady=5)
        
        # schedule display
        self.schedule_text = tk.Text(self.schedule_frame, height=10, width=40)
        self.schedule_text.grid(row=5, column=0, columnspan=2, pady=5)

    def add_workplace_dialog(self):
        dialog = tk.Toplevel(self.root)
        dialog.title("Add Workplace")
        
        ttk.Label(dialog, text="Name:").grid(row=0, column=0, pady=5)
        name_entry = ttk.Entry(dialog)
        name_entry.grid(row=0, column=1, pady=5)
        
        ttk.Label(dialog, text="Opening Time (HH:MM):").grid(row=1, column=0, pady=5)
        open_time_entry = ttk.Entry(dialog)
        open_time_entry.grid(row=1, column=1, pady=5)
        
        ttk.Label(dialog, text="Closing Time (HH:MM):").grid(row=2, column=0, pady=5)
        close_time_entry = ttk.Entry(dialog)
        close_time_entry.grid(row=2, column=1, pady=5)
        
        def save():
            name = name_entry.get()
            open_time = open_time_entry.get()
            close_time = close_time_entry.get()
            
            if self.schedule_manager.add_workplace(name, open_time, close_time):
                self.update_workplace_list()
                dialog.destroy()
            else:
                messagebox.showerror("Error", "Invalid input")
        
        ttk.Button(dialog, text="Save", command=save).grid(row=3, column=0, columnspan=2, pady=5)

    def add_worker_dialog(self):
        selection = self.workplace_list.curselection()
        if not selection:
            messagebox.showerror("Error", "Please select a workplace first")
            return
            
        workplace_id = self.schedule_manager.db.get_workplaces()[selection[0]]['id']
        
        dialog = tk.Toplevel(self.root)
        dialog.title("Add Worker")
        
        ttk.Label(dialog, text="First Name:").grid(row=0, column=0, pady=5)
        first_name_entry = ttk.Entry(dialog)
        first_name_entry.grid(row=0, column=1, pady=5)
        
        ttk.Label(dialog, text="Last Name:").grid(row=1, column=0, pady=5)
        last_name_entry = ttk.Entry(dialog)
        last_name_entry.grid(row=1, column=1, pady=5)
        
        def save():
            first_name = first_name_entry.get()
            last_name = last_name_entry.get()
            
            if self.schedule_manager.add_worker(workplace_id, first_name, last_name):
                self.update_worker_list()
                dialog.destroy()
            else:
                messagebox.showerror("Error", "Invalid input")
        
        ttk.Button(dialog, text="Save", command=save).grid(row=2, column=0, columnspan=2, pady=5)

    def set_availability_dialog(self):
        selection = self.worker_list.curselection()
        if not selection:
            messagebox.showerror("Error", "Please select a worker first")
            return
        
        workplace_selection = self.workplace_list.curselection()
        if not workplace_selection:
            return
            
        workers = self.schedule_manager.db.get_workers(
            self.schedule_manager.db.get_workplaces()[workplace_selection[0]]['id']
        )
        worker_id = workers[selection[0]]['id']
        
        dialog = tk.Toplevel(self.root)
        dialog.title("Set Availability")
        
        days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        day_var = tk.StringVar(dialog)
        day_var.set(days[0])
        
        ttk.Label(dialog, text="Day:").grid(row=0, column=0, pady=5)
        day_menu = ttk.OptionMenu(dialog, day_var, *days)
        day_menu.grid(row=0, column=1, pady=5)
        
        ttk.Label(dialog, text="Start Time (HH:MM):").grid(row=1, column=0, pady=5)
        start_time_entry = ttk.Entry(dialog)
        start_time_entry.grid(row=1, column=1, pady=5)
        
        ttk.Label(dialog, text="End Time (HH:MM):").grid(row=2, column=0, pady=5)
        end_time_entry = ttk.Entry(dialog)
        end_time_entry.grid(row=2, column=1, pady=5)
        
        def save():
            day = day_var.get()
            start_time = start_time_entry.get()
            end_time = end_time_entry.get()
            
            if self.schedule_manager.set_availability(worker_id, day, start_time, end_time):
                dialog.destroy()
            else:
                messagebox.showerror("Error", "Invalid input")
        
        ttk.Button(dialog, text="Save", command=save).grid(row=3, column=0, columnspan=2, pady=5)

    def update_workplace_list(self):
        self.workplace_list.delete(0, tk.END)
        workplaces = self.schedule_manager.db.get_workplaces()
        for workplace in workplaces:
            self.workplace_list.insert(tk.END, f"{workplace['name']} ({workplace['hours_open']}-{workplace['hours_close']})")

    def update_worker_list(self):
        self.worker_list.delete(0, tk.END)
        selection = self.workplace_list.curselection()
        if selection:
            workplace = self.schedule_manager.db.get_workplaces()[selection[0]]
            workers = self.schedule_manager.db.get_workers(workplace['id'])
            for worker in workers:
                self.worker_list.insert(tk.END, f"{worker['first_name']} {worker['last_name']}")

    def on_workplace_select(self, event):
        self.update_worker_list()

    def delete_workplace(self):
        selection = self.workplace_list.curselection()
        if selection:
            if messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this workplace?"):
                workplace = self.schedule_manager.db.get_workplaces()[selection[0]]
                if self.schedule_manager.db.delete_workplace(workplace['id']):
                    self.update_workplace_list()
                    self.update_worker_list()

    def delete_worker(self):
        worker_selection = self.worker_list.curselection()
        workplace_selection = self.workplace_list.curselection()
        if worker_selection and workplace_selection:
            if messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this worker?"):
                workplace = self.schedule_manager.db.get_workplaces()[workplace_selection[0]]
                workers = self.schedule_manager.db.get_workers(workplace['id'])
                worker = workers[worker_selection[0]]
                if self.schedule_manager.db.delete_worker(worker['id']):
                    self.update_worker_list()

    def view_available_workers(self):
        selection = self.workplace_list.curselection()
        if not selection:
            messagebox.showerror("Error", "Please select a workplace")
            return
            
        workplace = self.schedule_manager.db.get_workplaces()[selection[0]]
        date = self.date_entry.get()
        start_time = self.start_time_entry.get()
        end_time = self.end_time_entry.get()
        
        try:
            available_workers = self.schedule_manager.get_available_workers(
                workplace['id'], date, start_time, end_time
            )
            
            self.schedule_text.delete(1.0, tk.END)
            self.schedule_text.insert(tk.END, "Available Workers:\n\n")
            
            for worker in available_workers:
                self.schedule_text.insert(
                    tk.END, f"{worker['first_name']} {worker['last_name']}\n"
                )
        except ValueError:
            messagebox.showerror("Error", "Invalid date or time format")

    def add_schedule(self):
        workplace_selection = self.workplace_list.curselection()
        worker_selection = self.worker_list.curselection()
        
        if not workplace_selection or not worker_selection:
            messagebox.showerror("Error", "Please select a workplace and worker")
            return
            
        workplace = self.schedule_manager.db.get_workplaces()[workplace_selection[0]]
        workers = self.schedule_manager.db.get_workers(workplace['id'])
        worker = workers[worker_selection[0]]
        
        date = self.date_entry.get()
        start_time = self.start_time_entry.get()
        end_time = self.end_time_entry.get()
        
        if self.schedule_manager.add_schedule(workplace['id'], worker['id'], date, start_time, end_time):
            messagebox.showinfo("Success", "Schedule added successfully")
        else:
            messagebox.showerror("Error", "Failed to add schedule")

def main():
    root = tk.Tk()
    app = ScheduleApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
