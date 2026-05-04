import tkinter as tk
from tkinter import ttk, messagebox

from database import get_connection
from security import encrypt, decrypt
from gui.theme import apply_theme


class ShipmentFrame(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg="#0F172A")

        self.parent = parent
        self.selected_id = None

        self.build_header()
        self.build_form()
        self.build_search()
        self.build_table()
        self.load_shipments()

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
            text="Shipment Management",
            bg="#0F172A",
            fg="white",
            font=("Arial", 22, "bold")
        ).pack(pady=(18, 5))

    def build_form(self):
        form = tk.Frame(self, bg="#0F172A")
        form.pack(pady=10)

        labels = [
            "Order Number", "Sender Name", "Receiver Name", "Receiver Address",
            "Item Description", "Assigned Driver", "Route Details",
            "Transport Cost", "Surcharge", "Payment Status"
        ]

        self.entries = {}

        for index, label_text in enumerate(labels):
            tk.Label(
                form,
                text=label_text,
                bg="#0F172A",
                fg="white",
                font=("Arial", 10, "bold")
            ).grid(row=index // 2, column=(index % 2) * 2, padx=5, pady=5, sticky="w")

            entry = tk.Entry(form, width=30, bg="white", fg="black", font=("Arial", 11))
            entry.grid(row=index // 2, column=(index % 2) * 2 + 1, padx=5, pady=5)
            self.entries[label_text] = entry

        button_frame = tk.Frame(self, bg="#0F172A")
        button_frame.pack(pady=5)

        self.action_button(button_frame, "Add", self.add_shipment, 0)
        self.action_button(button_frame, "Update", self.update_shipment, 1)
        self.action_button(button_frame, "Delete", self.delete_shipment, 2)
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
            text="Search Order/Receiver:",
            bg="#0F172A",
            fg="white",
            font=("Arial", 10, "bold")
        ).grid(row=0, column=0, padx=5)

        self.search_entry = tk.Entry(search_frame, width=35, bg="white", fg="black")
        self.search_entry.grid(row=0, column=1, padx=5)

        tk.Button(search_frame, text="Search", command=self.search_shipments).grid(row=0, column=2, padx=5)
        tk.Button(search_frame, text="Show All", command=self.load_shipments).grid(row=0, column=3, padx=5)

    def build_table(self):
        columns = (
            "ID", "Order", "Sender", "Receiver", "Address",
            "Item", "Status", "Driver", "Route", "Cost", "Surcharge", "Payment"
        )

        self.tree = ttk.Treeview(self, columns=columns, show="headings")

        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=90)

        self.tree.pack(fill="both", expand=True, padx=20, pady=10)
        self.tree.bind("<<TreeviewSelect>>", self.select_record)

    def add_shipment(self):
        try:
            data = self.get_form_data()
            if data is None:
                return

            conn = get_connection()
            cursor = conn.cursor()

            cursor.execute("""
                INSERT INTO shipments (
                    order_number, sender_name, receiver_name, receiver_address,
                    item_description, assigned_driver, route_details,
                    transport_cost, surcharge, payment_status
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, data)

            conn.commit()
            conn.close()

            messagebox.showinfo("Success", "Shipment added successfully.")
            self.clear_form()
            self.load_shipments()

        except Exception as e:
            messagebox.showerror("Error", f"Could not add shipment: {e}")

    def update_shipment(self):
        if not self.selected_id:
            messagebox.showerror("Selection Error", "Please select a shipment to update.")
            return

        data = self.get_form_data()
        if data is None:
            return

        try:
            conn = get_connection()
            cursor = conn.cursor()

            cursor.execute("""
                UPDATE shipments
                SET order_number = ?, sender_name = ?, receiver_name = ?, receiver_address = ?,
                    item_description = ?, assigned_driver = ?, route_details = ?,
                    transport_cost = ?, surcharge = ?, payment_status = ?
                WHERE shipment_id = ?
            """, (*data, self.selected_id))

            conn.commit()
            conn.close()

            messagebox.showinfo("Success", "Shipment updated successfully.")
            self.clear_form()
            self.load_shipments()

        except Exception as e:
            messagebox.showerror("Error", f"Could not update shipment: {e}")

    def delete_shipment(self):
        if not self.selected_id:
            messagebox.showerror("Selection Error", "Please select a shipment to delete.")
            return

        confirm = messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this shipment?")
        if not confirm:
            return

        try:
            conn = get_connection()
            cursor = conn.cursor()

            cursor.execute("DELETE FROM shipments WHERE shipment_id = ?", (self.selected_id,))

            conn.commit()
            conn.close()

            messagebox.showinfo("Success", "Shipment deleted successfully.")
            self.clear_form()
            self.load_shipments()

        except Exception as e:
            messagebox.showerror("Error", f"Could not delete shipment: {e}")

    def search_shipments(self):
        keyword = self.search_entry.get().strip()

        for row in self.tree.get_children():
            self.tree.delete(row)

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT shipment_id, order_number, sender_name, receiver_name,
                   receiver_address, item_description, delivery_status,
                   assigned_driver, route_details, transport_cost, surcharge, payment_status
            FROM shipments
            WHERE order_number LIKE ? OR receiver_name LIKE ?
            ORDER BY shipment_id DESC
        """, (f"%{keyword}%", f"%{keyword}%"))

        rows = cursor.fetchall()
        conn.close()

        self.insert_rows(rows)

    def load_shipments(self):
        for row in self.tree.get_children():
            self.tree.delete(row)

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT shipment_id, order_number, sender_name, receiver_name,
                   receiver_address, item_description, delivery_status,
                   assigned_driver, route_details, transport_cost, surcharge, payment_status
            FROM shipments
            ORDER BY shipment_id DESC
        """)

        rows = cursor.fetchall()
        conn.close()

        self.insert_rows(rows)

    def insert_rows(self, rows):
        for row in rows:
            row = list(row)

            try:
                row[4] = decrypt(row[4])
            except Exception:
                row[4] = "Encrypted"

            self.tree.insert("", "end", values=row)

    def select_record(self, event):
        selected = self.tree.focus()
        if not selected:
            return

        values = self.tree.item(selected, "values")
        if not values:
            return

        self.selected_id = values[0]

        fields = [
            "Order Number", "Sender Name", "Receiver Name", "Receiver Address",
            "Item Description", "Assigned Driver", "Route Details",
            "Transport Cost", "Surcharge", "Payment Status"
        ]

        data = [
            values[1], values[2], values[3], values[4],
            values[5], values[7], values[8],
            values[9], values[10], values[11]
        ]

        self.clear_entries_only()

        for field, value in zip(fields, data):
            self.entries[field].insert(0, value)

    def get_form_data(self):
        order_number = self.entries["Order Number"].get().strip()
        sender_name = self.entries["Sender Name"].get().strip()
        receiver_name = self.entries["Receiver Name"].get().strip()
        receiver_address_text = self.entries["Receiver Address"].get().strip()
        item_description = self.entries["Item Description"].get().strip()
        assigned_driver = self.entries["Assigned Driver"].get().strip()
        route_details = self.entries["Route Details"].get().strip()
        payment_status = self.entries["Payment Status"].get().strip() or "Unpaid"

        if not order_number or not sender_name or not receiver_name or not receiver_address_text or not item_description:
            messagebox.showerror(
                "Validation Error",
                "Order Number, Sender Name, Receiver Name, Receiver Address and Item Description are required."
            )
            return None

        try:
            transport_cost = float(self.entries["Transport Cost"].get().strip() or 0)
            surcharge = float(self.entries["Surcharge"].get().strip() or 0)
        except ValueError:
            messagebox.showerror("Validation Error", "Transport Cost and Surcharge must be numbers.")
            return None

        return (
            order_number,
            sender_name,
            receiver_name,
            encrypt(receiver_address_text),
            item_description,
            assigned_driver,
            route_details,
            transport_cost,
            surcharge,
            payment_status
        )

    def clear_entries_only(self):
        for entry in self.entries.values():
            entry.delete(0, tk.END)

    def clear_form(self):
        self.selected_id = None
        self.clear_entries_only()