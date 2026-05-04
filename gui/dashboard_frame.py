import tkinter as tk
from tkinter import messagebox
from database import get_connection


class DashboardFrame(tk.Frame):
    def __init__(self, parent, user):
        super().__init__(parent, bg="#0F172A")

        self.parent = parent
        self.user = user
        self.username, self.role, self.full_name = user
        self.role = self.role.lower()

        self.build_ui()
        self.auto_refresh()

    # ================= UI =================
    def build_ui(self):
        self.build_sidebar()
        self.build_main_area()

    # ================= SIDEBAR =================
    def build_sidebar(self):
        sidebar = tk.Frame(self, bg="#020617", width=270)
        sidebar.pack(side="left", fill="y")
        sidebar.pack_propagate(False)

        if self.role == "driver":
            menu = [
                ("DASHBOARD", self.parent.show_dashboard, True),
                ("SHIPMENT HUB", self.parent.show_shipments, True),
            ]
        else:
            menu = [
                ("DASHBOARD", self.parent.show_dashboard, True),

                ("SHIPMENT HUB", self.parent.show_shipments, True),

                ("INVENTORY CONTROL", self.parent.show_inventory, self.role in ["admin", "manager", "staff"]),

                ("FLEET MANAGEMENT", self.parent.show_vehicles, self.role in ["admin", "manager"]),

                ("FACILITY CONTROL", self.parent.show_facility, self.role in ["admin", "manager", "staff"]),

                ("OPERATIONAL REPORTS", self.parent.show_reports, self.role in ["admin", "manager"]),

                ("USER REGISTRY", self.parent.show_user_registry, self.role in ["admin", "manager"]),

                ("SECURITY AUDIT", self.parent.show_security_audit, self.role in ["admin", "manager"]),
            ]

        for text, command, allowed in menu:
            if allowed:
                self.sidebar_btn(sidebar, text, command)
            else:
                self.sidebar_restricted(sidebar, text)

        tk.Frame(sidebar, bg="#020617").pack(expand=True, fill="both")
        self.logout_btn(sidebar)

    def sidebar_btn(self, parent, text, command):
        btn = tk.Label(
            parent,
            text=text,
            bg="#020617",
            fg="#E2E8F0",
            font=("Arial", 14, "bold"),
            anchor="w",
            padx=25,
            pady=18,
            cursor="hand2"
        )
        btn.pack(fill="x")
        btn.bind("<Button-1>", lambda e: command())
        btn.bind("<Enter>", lambda e: btn.config(bg="#0F172A", fg="white"))
        btn.bind("<Leave>", lambda e: btn.config(bg="#020617", fg="#E2E8F0"))

    def sidebar_restricted(self, parent, text):
        btn = tk.Label(
            parent,
            text=f"{text} 🔒",
            bg="#020617",
            fg="#64748B",
            font=("Arial", 14, "bold"),
            anchor="w",
            padx=25,
            pady=18,
            cursor="hand2"
        )
        btn.pack(fill="x")
        btn.bind("<Button-1>", lambda e: self.access_denied(text))
        btn.bind("<Enter>", lambda e: btn.config(bg="#0F172A", fg="#94A3B8"))
        btn.bind("<Leave>", lambda e: btn.config(bg="#020617", fg="#64748B"))

    def logout_btn(self, parent):
        btn = tk.Label(
            parent,
            text="LOGOUT",
            bg="#DC2626",
            fg="white",
            font=("Arial", 13, "bold"),
            padx=20,
            pady=12,
            cursor="hand2"
        )
        btn.pack(fill="x", padx=20, pady=25)
        btn.bind("<Button-1>", lambda e: self.parent.show_login())
        btn.bind("<Enter>", lambda e: btn.config(bg="#991B1B"))
        btn.bind("<Leave>", lambda e: btn.config(bg="#DC2626"))

    # ================= MAIN =================
    def build_main_area(self):
        main = tk.Frame(self, bg="#0F172A")
        main.pack(side="right", fill="both", expand=True)

        tk.Label(
            main,
            text="DASHBOARD OVERVIEW",
            bg="#0F172A",
            fg="white",
            font=("Arial", 26, "bold")
        ).pack(anchor="w", padx=30, pady=(25, 15))

        metrics = tk.Frame(main, bg="#0F172A")
        metrics.pack(fill="x", padx=30)

        total, pending, low_stock, fleet = self.get_metrics()

        self.metric_card(metrics, "TOTAL SHIPMENTS", total, "#3B82F6", 0)
        self.metric_card(metrics, "PENDING DELIVERIES", pending, "#FACC15", 1)
        self.metric_card(metrics, "LOW STOCK ALERTS", low_stock, "#EF4444", 2)
        self.metric_card(metrics, "AVAILABLE FLEET", fleet, "#22C55E", 3)

        tk.Label(
            main,
            text="ANALYTICS OVERVIEW",
            bg="#0F172A",
            fg="#94A3B8",
            font=("Arial", 13, "bold")
        ).pack(anchor="w", padx=30, pady=(35, 10))

        self.build_analytics(main)

        tk.Label(
            main,
            text="SYSTEM ACTIVITY STREAM",
            bg="#0F172A",
            fg="#94A3B8",
            font=("Arial", 13, "bold")
        ).pack(anchor="w", padx=30, pady=(30, 10))

        self.build_activity(main)

    # ================= METRICS =================
    def metric_card(self, parent, title, value, color, col):
        card = tk.Frame(parent, bg="#111827", width=240, height=140)
        card.grid(row=0, column=col, padx=10)
        card.grid_propagate(False)

        tk.Frame(card, bg=color, height=5).pack(fill="x")

        tk.Label(
            card,
            text=title,
            bg="#111827",
            fg="#94A3B8",
            font=("Arial", 10, "bold")
        ).pack(pady=(25, 8))

        tk.Label(
            card,
            text=str(value),
            bg="#111827",
            fg="white",
            font=("Arial", 28, "bold")
        ).pack()

    # ================= ANALYTICS =================
    def build_analytics(self, parent):
        charts = tk.Frame(parent, bg="#0F172A")
        charts.pack(fill="x", padx=30)

        self.bar_chart(
            charts,
            "Shipment Status",
            self.get_shipment_status_data(),
            0,
            ["#3B82F6", "#FACC15", "#22C55E", "#EF4444"]
        )

        self.bar_chart(
            charts,
            "Inventory Alerts",
            self.get_inventory_alert_data(),
            1,
            ["#22C55E", "#EF4444"]
        )

    def bar_chart(self, parent, title, data, column, colors):
        card = tk.Frame(parent, bg="#111827", width=500, height=240)
        card.grid(row=0, column=column, padx=10)
        card.grid_propagate(False)

        tk.Label(
            card,
            text=title,
            bg="#111827",
            fg="white",
            font=("Arial", 13, "bold")
        ).pack(anchor="w", padx=15, pady=(10, 0))

        canvas = tk.Canvas(card, width=460, height=160, bg="#111827", highlightthickness=0)
        canvas.pack()

        if not data:
            canvas.create_text(230, 80, text="No data available", fill="#94A3B8")
            return

        max_val = max(v for _, v in data) or 1

        for i, (label, value) in enumerate(data):
            x = 50 + i * 100
            h = (value / max_val) * 100

            canvas.create_rectangle(
                x, 120 - h, x + 50, 120,
                fill=colors[i % len(colors)],
                outline=""
            )

            canvas.create_text(x + 25, 135, text=str(label)[:10], fill="white")
            canvas.create_text(x + 25, 110 - h, text=str(value), fill="white")

    # ================= ACTIVITY =================
    def build_activity(self, parent):
        frame = tk.Frame(parent, bg="#111827")
        frame.pack(fill="both", expand=True, padx=30, pady=10)

        logs = self.get_logs()

        if not logs:
            tk.Label(frame, text="No activity available", bg="#111827", fg="white").pack()
            return

        for ts, user, action in logs:
            tk.Label(
                frame,
                text=f"{ts} | {user} | {action}",
                bg="#111827",
                fg="white"
            ).pack(anchor="w", padx=10)

    # ================= DATA =================
    def get_metrics(self):
        conn = get_connection()
        cursor = conn.cursor()

        def count(q):
            try:
                cursor.execute(q)
                return cursor.fetchone()[0] or 0
            except:
                return 0

        total = count("SELECT COUNT(*) FROM shipments")
        pending = count("SELECT COUNT(*) FROM shipments WHERE delivery_status='Pending'")
        low = count("SELECT COUNT(*) FROM inventory WHERE quantity <= reorder_level")
        fleet = count("SELECT COUNT(*) FROM vehicles WHERE availability='Available'")

        conn.close()
        return total, pending, low, fleet

    def get_shipment_status_data(self):
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT delivery_status, COUNT(*) FROM shipments GROUP BY delivery_status")
            data = cursor.fetchall()
            conn.close()
            return data
        except:
            return []

    def get_inventory_alert_data(self):
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM inventory WHERE quantity > reorder_level")
            ok = cursor.fetchone()[0]
            cursor.execute("SELECT COUNT(*) FROM inventory WHERE quantity <= reorder_level")
            low = cursor.fetchone()[0]
            conn.close()
            return [("Healthy", ok), ("Low", low)]
        except:
            return []

    def get_logs(self):
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT timestamp, username, action FROM activity_logs ORDER BY log_id DESC LIMIT 10")
            data = cursor.fetchall()
            conn.close()
            return data
        except:
            return []

    # ================= REFRESH =================
    def auto_refresh(self):
        self.after(10000, self.refresh_dashboard)

    def refresh_dashboard(self):
        for widget in self.winfo_children():
            widget.destroy()

        self.build_ui()
        self.auto_refresh()

    def access_denied(self, module):
        messagebox.showwarning("Access Restricted", f"No access to {module}")