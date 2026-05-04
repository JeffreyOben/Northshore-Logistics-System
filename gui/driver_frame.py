import tkinter as tk
from tkinter import ttk, messagebox

from database import get_connection
from security import encrypt, decrypt
from gui.theme import apply_theme


class DriverFrame(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg="#0F172A")

        self.parent = parent
        self.selected_id = None

        self.build_header()
        self.build_form()
        self.build_search()
        self.build_table()
        self.load_drivers()

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
            text="Driver Management",
            bg="#0F172A",
            fg="white",
            font=("Arial", 22, "bold")
        ).pack(pady=(18, 5))

    def build_form(self):
        form = tk.Frame(self, bg="#0F172A")
        form.pack(pady=10)

        labels = ["Full Name", "License Number", "Phone", "Shift Assignment", "Route History"]
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

        self.action_button(button_frame, "Add", self.add_driver, 0)
        self.action_button(button_frame, "Update", self.update_driver, 1)
        self.action_button(button_frame, "Delete", self.delete_driver, 2)
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
            text="Search Name/Shift:",
            bg="#0F172A",
            fg="white",
            font=("Arial", 10, "bold")
        ).grid(row=0, column=0, padx=5)

        self.search_entry = tk.Entry(search_frame, width=35, bg="white", fg="black")
        self.search_entry.grid(row=0, column=1, padx=5)

        tk.Button(search_frame, text="Search", command=self.search_drivers).grid(row=0, column=2, padx=5)
        tk.Button(search_frame, text="Show All", command=self.load_drivers).grid(row=0, column=3, padx=5)

    def build_table(self):
        columns = ("ID", "Name", "License", "Phone", "Shift", "Route History")
        self.tree = ttk.Treeview(self, columns=columns, show="headings")

        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=155)

        self.tree.pack(fill="both", expand=True, padx=20, pady=10)
        self.tree.bind("<<TreeviewSelect>>", self.select_record)

    def add_driver(self):
        data = self.get_form_data()
        if data is None:
            return

        try:
            conn = get_connection()
            cursor = conn.cursor()

            cursor.execute("""
                INSERT INTO drivers (full_name, license_number, phone, shift_assignment, route_history)
                VALUES (?, ?, ?, ?, ?)
            """, data)

            conn.commit()
            conn.close()

            messagebox.showinfo("Success", "Driver added successfully.")
            self.clear_form()
            self.load_drivers()

        except Exception as e:
            messagebox.showerror("Error", f"Could not add driver: {e}")

    def update_driver(self):
        if not self.selected_id:
            messagebox.showerror("Selection Error", "Please select a driver to update.")
            return

        data = self.get_form_data()
        if data is None:
            return

        try:
            conn = get_connection()
            cursor = conn.cursor()

            cursor.execute("""
                UPDATE drivers
                SET full_name = ?, license_number = ?, phone = ?, shift_assignment = ?, route_history = ?
                WHERE driver_id = ?
            """, (*data, self.selected_id))

            conn.commit()
            conn.close()

            messagebox.showinfo("Success", "Driver updated successfully.")
            self.clear_form()
            self.load_drivers()

        except Exception as e:
            messagebox.showerror("Error", f"Could not update driver: {e}")

    def delete_driver(self):
        if not self.selected_id:
            messagebox.showerror("Selection Error", "Please select a driver to delete.")
            return

        confirm = messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this driver?")
        if not confirm:
            return

        try:
            conn = get_connection()
            cursor = conn.cursor()

            cursor.execute("DELETE FROM drivers WHERE driver_id = ?", (self.selected_id,))

            conn.commit()
            conn.close()

            messagebox.showinfo("Success", "Driver deleted successfully.")
            self.clear_form()
            self.load_drivers()

        except Exception as e:
            messagebox.showerror("Error", f"Could not delete driver: {e}")

    def search_drivers(self):
        keyword = self.search_entry.get().strip()

        for row in self.tree.get_children():
            self.tree.delete(row)

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT driver_id, full_name, license_number, phone, shift_assignment, route_history
            FROM drivers
            WHERE full_name LIKE ? OR shift_assignment LIKE ?
            ORDER BY driver_id DESC
        """, (f"%{keyword}%", f"%{keyword}%"))

        rows = cursor.fetchall()
        conn.close()

        self.insert_rows(rows)

    def load_drivers(self):
        for row in self.tree.get_children():
            self.tree.delete(row)

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT driver_id, full_name, license_number, phone, shift_assignment, route_history
            FROM drivers
            ORDER BY driver_id DESC
        """)

        rows = cursor.fetchall()
        conn.close()

        self.insert_rows(rows)

    def insert_rows(self, rows):
        for row in rows:
            row = list(row)

            try:
                row[2] = decrypt(row[2])
                row[3] = decrypt(row[3]) if row[3] else ""
            except Exception:
                pass

            self.tree.insert("", "end", values=row)

    def select_record(self, event):
        selected = self.tree.focus()
        if not selected:
            return

        values = self.tree.item(selected, "values")
        if not values:
            return

        self.selected_id = values[0]

        fields = ["Full Name", "License Number", "Phone", "Shift Assignment", "Route History"]
        data = [values[1], values[2], values[3], values[4], values[5]]

        self.clear_entries_only()

        for field, value in zip(fields, data):
            self.entries[field].insert(0, value)

    def get_form_data(self):
        full_name = self.entries["Full Name"].get().strip()
        license_number = self.entries["License Number"].get().strip()
        phone = self.entries["Phone"].get().strip()
        shift_assignment = self.entries["Shift Assignment"].get().strip()
        route_history = self.entries["Route History"].get().strip()

        if not full_name or not license_number:
            messagebox.showerror("Validation Error", "Full Name and License Number are required.")
            return None

        return (
            full_name,
            encrypt(license_number),
            encrypt(phone) if phone else "",
            shift_assignment,
            route_history
        )

    def clear_entries_only(self):
        for entry in self.entries.values():
            entry.delete(0, tk.END)

    def clear_form(self):
        self.selected_id = None
        self.clear_entries_only()