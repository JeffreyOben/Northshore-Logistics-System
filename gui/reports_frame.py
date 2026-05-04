import csv
import tkinter as tk
from tkinter import filedialog, messagebox

from database import get_connection
from gui.theme import apply_theme


class ReportsFrame(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg="#0F172A")
        self.parent = parent

        self.current_report_title = "Northshore Logistics Report"
        self.current_report_rows = []

        self.build_header()
        self.build_buttons()
        self.build_report_box()

        apply_theme(self)

    # ================= HEADER =================
    def build_header(self):
        nav = tk.Frame(self, bg="#1E293B", height=55)
        nav.pack(fill="x")

        tk.Label(
            nav,
            text="Operational Reports",
            bg="#1E293B",
            fg="white",
            font=("Arial", 16, "bold")
        ).pack(side="left", padx=20, pady=12)

        tk.Button(
            nav,
            text="Dashboard",
            bg="#38BDF8",
            fg="#0F172A",
            font=("Arial", 11, "bold"),
            command=self.parent.show_dashboard
        ).pack(side="right", padx=20, pady=10)

    # ================= BUTTONS =================
    def build_buttons(self):
        frame = tk.Frame(self, bg="#0F172A")
        frame.pack(pady=15)

        self.btn(frame, "Shipment Report", self.shipment_report, 0, 0)
        self.btn(frame, "Inventory Report", self.inventory_report, 0, 1)
        self.btn(frame, "Vehicle Report", self.vehicle_report, 0, 2)
        self.btn(frame, "Driver Report", self.driver_report, 0, 3)

        self.btn(frame, "Full System Summary", self.full_system_report, 1, 0)
        self.btn(frame, "Export CSV", self.export_csv, 1, 1, "#10B981", "white")
        self.btn(frame, "Export PDF", self.export_pdf, 1, 2, "#8B5CF6", "white")
        self.btn(frame, "Clear Report", self.clear_report, 1, 3, "#DC2626", "white")

    def btn(self, parent, text, cmd, r, c, bg="#38BDF8", fg="#0F172A"):
        tk.Button(
            parent,
            text=text,
            width=20,
            bg=bg,
            fg=fg,
            font=("Arial", 11, "bold"),
            command=cmd
        ).grid(row=r, column=c, padx=6, pady=6)

    # ================= REPORT BOX =================
    def build_report_box(self):
        self.report_box = tk.Text(
            self,
            width=115,
            height=30,
            bg="white",
            fg="black",
            font=("Arial", 11),
            bd=2
        )
        self.report_box.pack(padx=20, pady=10)

    def clear_report(self):
        self.current_report_rows = []
        self.report_box.delete("1.0", tk.END)

    def write_header(self, title):
        self.clear_report()
        self.current_report_title = title
        self.report_box.insert(tk.END, title + "\n" + "="*70 + "\n\n")

    def add(self, text):
        self.report_box.insert(tk.END, text + "\n")

    def set_rows(self, headers, rows):
        self.current_report_rows = [headers] + rows

    # ================= REPORTS =================
    def shipment_report(self):
        self.write_header("SHIPMENT REPORT")

        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM shipments")
        rows = cur.fetchall()
        conn.close()

        self.set_rows(
            ["ID","Order","Sender","Receiver","Address","Item","Status","Driver","Route","Cost","Surcharge","Payment"],
            rows
        )

        for r in rows:
            self.add(str(r))

    def inventory_report(self):
        self.write_header("INVENTORY REPORT")

        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM inventory")
        rows = cur.fetchall()
        conn.close()

        self.set_rows(["ID","Item","Warehouse","Qty","Reorder","Location"], rows)

        for r in rows:
            self.add(str(r))

    def vehicle_report(self):
        self.write_header("VEHICLE REPORT")

        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM vehicles")
        rows = cur.fetchall()
        conn.close()

        self.set_rows(["ID","Reg","Capacity","Maintenance","Availability"], rows)

        for r in rows:
            self.add(str(r))

    def driver_report(self):
        self.write_header("DRIVER REPORT")

        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM drivers")
        rows = cur.fetchall()
        conn.close()

        self.set_rows(["ID","Name","License","Phone","Shift","Route"], rows)

        for r in rows:
            self.add(str(r))

    def full_system_report(self):
        self.write_header("SYSTEM SUMMARY")

        conn = get_connection()
        cur = conn.cursor()

        tables = ["shipments","inventory","vehicles","drivers","users","activity_logs"]
        rows = []

        for t in tables:
            try:
                cur.execute(f"SELECT COUNT(*) FROM {t}")
                count = cur.fetchone()[0]
                self.add(f"{t}: {count}")
                rows.append((t, count))
            except:
                self.add(f"{t}: error")
                rows.append((t, "error"))

        conn.close()
        self.set_rows(["Table","Count"], rows)

    # ================= EXPORT CSV =================
    def export_csv(self):
        if not self.current_report_rows:
            messagebox.showerror("Error","Generate report first")
            return

        file = filedialog.asksaveasfilename(defaultextension=".csv")
        if not file:
            return

        with open(file,"w",newline="",encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerows(self.current_report_rows)

        messagebox.showinfo("Done","CSV exported")

    # ================= EXPORT PDF =================
    def export_pdf(self):
        content = self.report_box.get("1.0", tk.END).strip()
        if not content:
            messagebox.showerror("Error","Generate report first")
            return

        file = filedialog.asksaveasfilename(defaultextension=".pdf")
        if not file:
            return

        with open(file, "w") as f:
            f.write(content)

        messagebox.showinfo("Done","PDF exported (simple text PDF)")