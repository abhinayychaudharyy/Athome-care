
import tkinter as tk
from tkinter import messagebox
import json
import os

class ServiceApp:
    def __init__(self, root):
        self.root = root
        self.root.title("AtHomeCare")
        self.root.geometry("450x500")

      
        self.services = {
            "Electrician": [
                ("Fan Repair", 500),
                ("Light Installation", 1000),
                ("Wiring Repair", 500),
                ("Switch Replacement", 300),
                ("Camera Installation", 800),
                ("AC Installation", 200)
            ],
            "Carpenter": [
                ("Furniture Assembly", 700),
                ("Door Repair", 600),
                ("Wardrobe", 400),
                ("Cabinet Repair", 100),
                ("Window Repair", 500),
                ("Furniture Making", 1000)
            ],
            "Plumber": [
                ("Pipe Installation", 300),
                ("Drain Cleaning", 150),
                ("Fixture Installation and Repair", 200),
                ("Water Heater Services", 500),
                ("Leak Detection and Repair", 400)
            ],
            "Gardener": [
                ("Planting and Landscaping", 800),
                ("Lawn Care", 600),
                ("Garden Cleaning", 1000)
            ]
        }

        self.workers = self.load_workers()
        self.users = {}
        self.load_users()
        self.logged_in_user = None
        self.selected_city = None  
        self.selected_category = None

        self.login_screen()

    def load_users(self):
        if os.path.exists("users.json"):
            with open("users.json", "r") as file:
                self.users = json.load(file)

    def save_users(self):
        with open("users.json", "w") as file:
            json.dump(self.users, file)

    def load_workers(self):
        if os.path.exists("workers.json"):
            with open("workers.json", "r") as file:
                return json.load(file)
        

    def save_workers(self):
        with open("workers.json", "w") as file:
            json.dump(self.workers, file)

    def login_screen(self):
        self.clear_screen()
        try:
            self.photo = tk.PhotoImage(file="athomecare.png") 
            img_label = tk.Label(self.root, image=self.photo)
            img_label.pack(padx=10)  
        except Exception as e:
            print(f"Error loading image: {e}")
        

        tk.Label(self.root, text="Username", fg="red").pack()
        self.entry_username = tk.Entry(self.root)
        self.entry_username.pack()

        tk.Label(self.root, text="Password", fg="red").pack()
        self.entry_password = tk.Entry(self.root, show="*")
        self.entry_password.pack()

        tk.Button(self.root, text="Register", command=self.register_user).pack(pady=5)
        tk.Button(self.root, text="Login", command=self.login_user).pack(pady=5)

    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def register_user(self):
        username = self.entry_username.get().strip()
        password = self.entry_password.get().strip()

        if username and password:
            if username in self.users:
                messagebox.showerror("Error", "Username already exists")
            else:
                self.users[username] = password
                self.save_users()
                messagebox.showinfo("Registration", "User Registered Successfully")
        else:
            messagebox.showerror("Error", "Both fields are required")

    def login_user(self):
        username = self.entry_username.get().strip()
        password = self.entry_password.get().strip()

        if username and password:
            if username in self.users and self.users[username] == password:
                self.logged_in_user = username
                messagebox.showinfo("Login", "Login Successful")
                self.after_login_screen()
            else:
                messagebox.showerror("Login", "Invalid Login id")
        else:
            messagebox.showerror("Error", "Both login and password are required")

    def after_login_screen(self):
        self.clear_screen()
        tk.Label(self.root, text=f"Welcome, {self.logged_in_user}!", font=("Arial", 14)).pack(pady=10)

        tk.Button(self.root, text="Book a Service", command=self.select_city_screen).pack(pady=10)
        tk.Button(self.root, text="Add a Worker", command=self.add_worker_screen).pack(pady=10)

    def select_city_screen(self):
        self.clear_screen()
        tk.Label(self.root, text="Select a City", font=("Arial", 14)).pack(pady=10)

        Indian_cities = set(city for category_workers in self.workers.values() for _, _, city in category_workers)
        if not Indian_cities:
            messagebox.showerror("Error", "No cities available with workers.")
            return

        self.city_var = tk.StringVar()
        self.city_var.set("Select City") 
        city_options = list(Indian_cities)
        
        city_dropdown = tk.OptionMenu(self.root, self.city_var, *city_options)
        city_dropdown.pack(pady=10)

        tk.Button(self.root, text="Next", command=self.show_categories_screen).pack(pady=10)
        tk.Button(self.root, text="Back", command=self.after_login_screen).pack(pady=5)

    def show_categories_screen(self):
        selected_city = self.city_var.get()
        if selected_city == "Select City":
            messagebox.showerror("Error", "Please select a city.")
            return

        self.selected_city = selected_city  
        self.clear_screen()

        tk.Label(self.root, text="Select a Service Category", font=("Arial", 14)).pack(pady=10)

        self.category_var = tk.StringVar()

        for category in self.services.keys():
            tk.Radiobutton(self.root, text=category, variable=self.category_var, value=category).pack(anchor='w')

        tk.Button(self.root, text="Next: Choose Worker", command=self.show_workers_screen).pack(pady=20)
        tk.Button(self.root, text="Back", command=self.select_city_screen).pack(pady=5)

    def show_workers_screen(self):
        selected_category = self.category_var.get()
        if not selected_category:
            messagebox.showerror("Error", "Please select a service category.")
            return

        self.selected_category = selected_category
        self.clear_screen()

        tk.Label(self.root, text=f"Available {selected_category} in {self.selected_city}", font=("Arial", 14)).pack(pady=10)

        city_filtered_workers = [
            (name, rate) for name, rate, city in self.workers[selected_category] if city == self.selected_city
        ]
        if not city_filtered_workers:
            messagebox.showinfo("No Workers", f"No workers available in {self.selected_city} for {selected_category}")
            self.show_categories_screen()
            return

        city_filtered_workers.sort(key=lambda x: x[1])
        self.worker_var = tk.StringVar()
        for name, rate in city_filtered_workers:
            tk.Radiobutton(self.root, text=f"{name} - ₹{rate}/hr", variable=self.worker_var, value=name).pack(anchor='w')

        tk.Button(self.root, text="Next: Choose Services", command=self.show_services_screen).pack(pady=20)
        tk.Button(self.root, text="Back", command=self.show_categories_screen).pack(pady=5)

    def show_services_screen(self):
        selected_worker = self.worker_var.get()
        if not selected_worker:
            messagebox.showerror("Error", "Please select a worker.")
            return

        self.clear_screen()
        tk.Label(self.root, text="Select Services", font=("Arial", 14)).pack(pady=10)

        self.selected_services = {}
        for service, price in self.services[self.selected_category]:
            var = tk.BooleanVar()
            chk = tk.Checkbutton(self.root, text=f"{service} - ₹{price}", variable=var)
            chk.pack(anchor='w')
            self.selected_services[service] = (var, price)

        tk.Button(self.root, text="Book Service", command=self.confirm_booking).pack(pady=20)
        tk.Button(self.root, text="Back", command=self.show_workers_screen).pack(pady=5)

    def confirm_booking(self):
        selected_worker = self.worker_var.get()
        if not selected_worker:
            messagebox.showerror("Error", "Please select a worker.")
            return

        selected_services = [
            (service, price) for service, (var, price) in self.selected_services.items() if var.get()
        ]

        if not selected_services:
            messagebox.showerror("Error", "Please select at least one service.")
            return

        worker_rate = next(rate for name, rate, city in self.workers[self.selected_category]
                           if name == selected_worker and city == self.selected_city)

        total_cost = sum(price for _, price in selected_services) + worker_rate

        service_details = "\n".join([f"{service}: ₹{price}" for service, price in selected_services])

        message = (
            f"Booking Summary:\n\n"
            f"Worker: {selected_worker}\n"
            f"Hourly Rate: ₹{worker_rate}\n\n"
            f"Services:\n{service_details}\n\n"
            f"Total Cost: ₹{total_cost}"
        )
        messagebox.showinfo("Booking Confirmation", message)

    def add_worker_screen(self):
        self.clear_screen()
        tk.Label(self.root, text="Add a Worker", font=("Arial", 14)).pack(pady=10)

        tk.Label(self.root, text="Worker Name:").pack()
        self.entry_worker_name = tk.Entry(self.root)
        self.entry_worker_name.pack()

        tk.Label(self.root, text="Hourly Rate (₹):").pack()
        self.entry_worker_rate = tk.Entry(self.root)
        self.entry_worker_rate.pack()

        tk.Label(self.root, text="City:").pack()
        self.entry_worker_city = tk.Entry(self.root)
        self.entry_worker_city.pack()

        self.worker_category_var = tk.StringVar()
        self.worker_category_var.set("Select Category")

        category_dropdown = tk.OptionMenu(self.root, self.worker_category_var, *self.services.keys())
        category_dropdown.pack(pady=10)

        tk.Button(self.root, text="Add Worker", command=self.add_worker).pack(pady=10)
        tk.Button(self.root, text="Back", command=self.after_login_screen).pack(pady=5)

    def add_worker(self):
        worker_name = self.entry_worker_name.get().strip()
        worker_rate = self.entry_worker_rate.get().strip()
        worker_city = self.entry_worker_city.get().strip()
        worker_category = self.worker_category_var.get()

        if worker_name and worker_rate.isdigit() and worker_city and worker_category in self.services:
            worker_rate = int(worker_rate)
            self.workers[worker_category].append((worker_name, worker_rate, worker_city))
            self.save_workers()
            messagebox.showinfo("Success", "Worker added successfully!")
        else:
            messagebox.showerror("Error", "Please fill all fields with valid information.")

if __name__ == "__main__":
    root = tk.Tk()
    app = ServiceApp(root)
    root.mainloop()
