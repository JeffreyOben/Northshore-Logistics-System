import tkinter as tk
from tkinter import ttk, messagebox

from database import get_connection
from gui.theme import apply_theme


class UserRegistryFrame(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg="#0F172A")
        self.parent = parent
        self.selected_user_id = None

        self.build_header()
        self.build_table()
        self.load_users()

        apply_theme(self)

    def build_header(self):
        nav = tk.Frame(self, bg="#1E293B", height=55)
        nav.pack(fill="x")

        tk.Label(nav, text="User Registry", bg="#1E293B", fg="white",
                 font=("Arial", 16, "bold")).pack(side="left", padx=20, pady=12)

        tk.Button(nav, text="Dashboard", bg="#38BDF8", fg="#0F172A",
                  command=self.parent.show_dashboard).pack(side="right", padx=20)

    def build_table(self):
        self.tree = ttk.Treeview(self, columns=("ID", "Username", "Role", "Full Name"), show="headings")

        for col in ("ID", "Username", "Role", "Full Name"):
            self.tree.heading(col, text=col)
            self.tree.column(col, width=200)

        self.tree.pack(fill="both", expand=True, padx=20, pady=20)

        controls = tk.Frame(self, bg="#0F172A")
        controls.pack(pady=10)

        tk.Button(controls, text="Promote to Manager", command=self.promote_user).grid(row=0, column=0, padx=5)
        tk.Button(controls, text="Set as Staff", command=self.set_staff).grid(row=0, column=1, padx=5)
        tk.Button(controls, text="Refresh", command=self.load_users).grid(row=0, column=2, padx=5)

        self.tree.bind("<<TreeviewSelect>>", self.select_user)

    def select_user(self, event):
        selected = self.tree.focus()
        if selected:
            values = self.tree.item(selected, "values")
            self.selected_user_id = values[0]

    def load_users(self):
        for row in self.tree.get_children():
            self.tree.delete(row)

        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT user_id, username, role, full_name FROM users ORDER BY user_id DESC")
        rows = cursor.fetchall()
        conn.close()

        for row in rows:
            self.tree.insert("", "end", values=row)

    def update_role(self, role):
        if not self.selected_user_id:
            messagebox.showerror("Error", "Please select a user first.")
            return

        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE users SET role = ? WHERE user_id = ?", (role, self.selected_user_id))
        conn.commit()
        conn.close()

        messagebox.showinfo("Success", f"User role changed to {role}.")
        self.load_users()

    def promote_user(self):
        self.update_role("manager")

    def set_staff(self):
        self.update_role("staff")