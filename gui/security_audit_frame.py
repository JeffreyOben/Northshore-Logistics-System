import tkinter as tk
from tkinter import ttk

from database import get_connection
from gui.theme import apply_theme


class SecurityAuditFrame(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg="#0F172A")
        self.parent = parent

        self.build_header()
        self.build_table()
        self.load_logs()

        apply_theme(self)

    def build_header(self):
        nav = tk.Frame(self, bg="#1E293B", height=55)
        nav.pack(fill="x")

        tk.Label(nav, text="Security Audit", bg="#1E293B", fg="white",
                 font=("Arial", 16, "bold")).pack(side="left", padx=20, pady=12)

        tk.Button(nav, text="Dashboard", bg="#38BDF8", fg="#0F172A",
                  command=self.parent.show_dashboard).pack(side="right", padx=20)

    def build_table(self):
        self.tree = ttk.Treeview(self, columns=("ID", "Username", "Action", "Timestamp"), show="headings")

        for col in ("ID", "Username", "Action", "Timestamp"):
            self.tree.heading(col, text=col)
            self.tree.column(col, width=220)

        self.tree.pack(fill="both", expand=True, padx=20, pady=20)

        tk.Button(self, text="Refresh Logs", command=self.load_logs).pack(pady=10)

    def load_logs(self):
        for row in self.tree.get_children():
            self.tree.delete(row)

        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT log_id, username, action, timestamp
            FROM activity_logs
            ORDER BY log_id DESC
        """)
        rows = cursor.fetchall()
        conn.close()

        for row in rows:
            self.tree.insert("", "end", values=row)