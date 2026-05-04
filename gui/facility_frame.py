import tkinter as tk
from tkinter import ttk, messagebox

from database import get_connection
from gui.theme import apply_theme


class FacilityFrame(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg="#0F172A")
        self.parent = parent

        self.build_header()
        self.build_form()
        self.build_table()
        self.load_warehouses()

        apply_theme(self)

    def build_header(self):
        nav = tk.Frame(self, bg="#1E293B", height=55)
        nav.pack(fill="x")

        tk.Label(nav, text="Facility Control", bg="#1E293B", fg="white",
                 font=("Arial", 16, "bold")).pack(side="left", padx=20, pady=12)

        tk.Button(nav, text="Dashboard", bg="#38BDF8", fg="#0F172A",
                  command=self.parent.show_dashboard).pack(side="right", padx=20)

    def build_form(self):
        form = tk.Frame(self, bg="#0F172A")
        form.pack(pady=20)

        tk.Label(form, text="Warehouse Name", bg="#0F172A", fg="white").grid(row=0, column=0, padx=5, pady=5)
        self.name_entry = tk.Entry(form, width=35)
        self.name_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(form, text="Location", bg="#0F172A", fg="white").grid(row=1, column=0, padx=5, pady=5)
        self.location_entry = tk.Entry(form, width=35)
        self.location_entry.grid(row=1, column=1, padx=5, pady=5)

        tk.Button(form, text="Add Facility", command=self.add_warehouse).grid(row=2, column=0, pady=10)
        tk.Button(form, text="Refresh", command=self.load_warehouses).grid(row=2, column=1, pady=10)

    def build_table(self):
        self.tree = ttk.Treeview(self, columns=("ID", "Name", "Location"), show="headings")
        for col in ("ID", "Name", "Location"):
            self.tree.heading(col, text=col)
            self.tree.column(col, width=220)
        self.tree.pack(fill="both", expand=True, padx=20, pady=10)

    def add_warehouse(self):
        name = self.name_entry.get().strip()
        location = self.location_entry.get().strip()

        if not name or not location:
            messagebox.showerror("Error", "Warehouse name and location are required.")
            return

        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO warehouses (name, location) VALUES (?, ?)", (name, location))
        conn.commit()
        conn.close()

        messagebox.showinfo("Success", "Facility added successfully.")
        self.name_entry.delete(0, tk.END)
        self.location_entry.delete(0, tk.END)
        self.load_warehouses()

    def load_warehouses(self):
        for row in self.tree.get_children():
            self.tree.delete(row)

        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT warehouse_id, name, location FROM warehouses ORDER BY warehouse_id DESC")
        rows = cursor.fetchall()
        conn.close()

        for row in rows:
            self.tree.insert("", "end", values=row)