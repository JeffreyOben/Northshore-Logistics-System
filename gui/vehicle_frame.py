import tkinter as tk
from tkinter import ttk, messagebox

from database import get_connection
from gui.theme import apply_theme


class VehicleFrame(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg="#0F172A")

        self.parent = parent
        self.selected_id = None

        self.build_header()
        self.build_form()
        self.build_search()
        self.build_table()
        self.load_vehicles()

        apply_theme(self)

    def build_header(self):
        nav = tk.Frame(self, bg="#1E293B", height=55)
        nav.pack(fill="x")

        tk.Label(
            nav,
            text="Northshore Logistics System",
            bg="#1E293B",
            fg="white",
            font=("Arial", 15, "bold")
        ).pack(side="left", padx=20, pady=12)

        tk.Button(
            nav,
            text="Dashboard",
            bg="#38BDF8",
            fg="#0F172A",
            font=("Arial", 11, "bold"),
            command=self.parent.show_dashboard
        ).pack(side="right", padx=20, pady=10)

        tk.Label(
            self,
            text="Vehicle Management",
            bg="#0F172A",
            fg="white",
            font=("Arial", 22, "bold")
        ).pack(pady=(18, 5))

    def build_form(self):
        form = tk.Frame(self, bg="#0F172A")
        form.pack(pady=10)

        labels = ["Registration Number", "Capacity", "Maintenance Date", "Availability"]
        self.entries = {}

        for i, label_text in enumerate(labels):
            tk.Label(
                form,
                text=label_text,
                bg="#0F172A",
                fg="white",
                font=("Arial", 10, "bold")
            ).grid(row=i, column=0, padx=5, pady=5, sticky="w")

            entry = tk.Entry(form, width=35, bg="white", fg="black", font=("Arial", 11))
            entry.grid(row=i, column=1, padx=5, pady=5)
            self.entries[label_text] = entry

        button_frame = tk.Frame(self, bg="#0F172A")
        button_frame.pack(pady=5)

        self.action_button(button_frame, "Add", self.add_vehicle, 0)
        self.action_button(button_frame, "Update", self.update_vehicle, 1)
        self.action_button(button_frame, "Delete", self.delete_vehicle, 2)
        self.action_button(button_frame, "Clear", self.clear_form, 3)

    def action_button(self, parent, text, command, column):
        bg = "#DC2626" if text == "Delete" else "#38BDF8"
        fg = "white" if text == "Delete" else "#0F172A"

        tk.Button(
            parent,
            text=text,
            width=15,
            bg=bg,
            fg=fg,
            font=("Arial", 11, "bold"),
            command=command
        ).grid(row=0, column=column, padx=5)

    def build_search(self):
        search_frame = tk.Frame(self, bg="#0F172A")
        search_frame.pack(pady=5)

        tk.Label(
            search_frame,
            text="Search Registration/Availability:",
            bg="#0F172A",
            fg="white",
            font=("Arial", 10, "bold")
        ).grid(row=0, column=0, padx=5)

        self.search_entry = tk.Entry(search_frame, width=35, bg="white", fg="black")
        self.search_entry.grid(row=0, column=1, padx=5)

        tk.Button(search_frame, text="Search", command=self.search_vehicles).grid(row=0, column=2, padx=5)
        tk.Button(search_frame, text="Show All", command=self.load_vehicles).grid(row=0, column=3, padx=5)

    def build_table(self):
        columns = ("ID", "Registration", "Capacity", "Maintenance", "Availability")
        self.tree = ttk.Treeview(self, columns=columns, show="headings")

        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=170)

        self.tree.pack(fill="both", expand=True, padx=20, pady=10)
        self.tree.bind("<<TreeviewSelect>>", self.select_record)

    def add_vehicle(self):
        data = self.get_form_data()
        if data is None:
            return

        try:
            conn = get_connection()
            cursor = conn.cursor()

            cursor.execute("""
                INSERT INTO vehicles (registration_number, capacity, maintenance_date, availability)
                VALUES (?, ?, ?, ?)
            """, data)

            conn.commit()
            conn.close()

            messagebox.showinfo("Success", "Vehicle added successfully.")
            self.clear_form()
            self.load_vehicles()

        except Exception as e:
            messagebox.showerror("Error", f"Could not add vehicle: {e}")

    def update_vehicle(self):
        if not self.selected_id:
            messagebox.showerror("Selection Error", "Please select a vehicle to update.")
            return

        data = self.get_form_data()
        if data is None:
            return

        try:
            conn = get_connection()
            cursor = conn.cursor()

            cursor.execute("""
                UPDATE vehicles
                SET registration_number = ?, capacity = ?, maintenance_date = ?, availability = ?
                WHERE vehicle_id = ?
            """, (*data, self.selected_id))

            conn.commit()
            conn.close()

            messagebox.showinfo("Success", "Vehicle updated successfully.")
            self.clear_form()
            self.load_vehicles()

        except Exception as e:
            messagebox.showerror("Error", f"Could not update vehicle: {e}")

    def delete_vehicle(self):
        if not self.selected_id:
            messagebox.showerror("Selection Error", "Please select a vehicle to delete.")
            return

        confirm = messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this vehicle?")
        if not confirm:
            return

        try:
            conn = get_connection()
            cursor = conn.cursor()

            cursor.execute("DELETE FROM vehicles WHERE vehicle_id = ?", (self.selected_id,))

            conn.commit()
            conn.close()

            messagebox.showinfo("Success", "Vehicle deleted successfully.")
            self.clear_form()
            self.load_vehicles()

        except Exception as e:
            messagebox.showerror("Error", f"Could not delete vehicle: {e}")

    def search_vehicles(self):
        keyword = self.search_entry.get().strip()

        for row in self.tree.get_children():
            self.tree.delete(row)

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT vehicle_id, registration_number, capacity, maintenance_date, availability
            FROM vehicles
            WHERE registration_number LIKE ? OR availability LIKE ?
            ORDER BY vehicle_id DESC
        """, (f"%{keyword}%", f"%{keyword}%"))

        rows = cursor.fetchall()
        conn.close()

        for row in rows:
            self.tree.insert("", "end", values=row)

    def load_vehicles(self):
        for row in self.tree.get_children():
            self.tree.delete(row)

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT vehicle_id, registration_number, capacity, maintenance_date, availability
            FROM vehicles
            ORDER BY vehicle_id DESC
        """)

        rows = cursor.fetchall()
        conn.close()

        for row in rows:
            self.tree.insert("", "end", values=row)

    def select_record(self, event):
        selected = self.tree.focus()
        if not selected:
            return

        values = self.tree.item(selected, "values")
        if not values:
            return

        self.selected_id = values[0]

        fields = ["Registration Number", "Capacity", "Maintenance Date", "Availability"]
        data = [values[1], values[2], values[3], values[4]]

        self.clear_entries_only()

        for field, value in zip(fields, data):
            self.entries[field].insert(0, value)

    def get_form_data(self):
        registration_number = self.entries["Registration Number"].get().strip()
        capacity = self.entries["Capacity"].get().strip()
        maintenance_date = self.entries["Maintenance Date"].get().strip()
        availability = self.entries["Availability"].get().strip() or "Available"

        if not registration_number or not capacity:
            messagebox.showerror("Validation Error", "Registration Number and Capacity are required.")
            return None

        return registration_number, capacity, maintenance_date, availability

    def clear_entries_only(self):
        for entry in self.entries.values():
            entry.delete(0, tk.END)

    def clear_form(self):
        self.selected_id = None
        self.clear_entries_only()