import tkinter as tk

from database import create_tables
from auth import create_admin
from gui.login_frame import LoginFrame
from gui.dashboard_frame import DashboardFrame
from gui.shipment_frame import ShipmentFrame
from gui.inventory_frame import InventoryFrame
from gui.vehicle_frame import VehicleFrame
from gui.driver_frame import DriverFrame
from gui.reports_frame import ReportsFrame
from gui.facility_frame import FacilityFrame
from gui.user_registry_frame import UserRegistryFrame
from gui.security_audit_frame import SecurityAuditFrame


class NorthshoreApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Northshore Logistics System")
        self.configure(bg="#0F172A")

        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        self.geometry(f"{screen_width}x{screen_height}+0+0")
        self.minsize(1200, 750)

        self.current_user = None
        self.current_frame = None

        create_tables()
        create_admin()

        self.show_login()

    def clear_frame(self):
        if self.current_frame:
            self.current_frame.destroy()

    def show_login(self):
        self.clear_frame()
        self.current_frame = LoginFrame(self, self.login_success)
        self.current_frame.pack(fill="both", expand=True)

    def login_success(self, user):
        self.current_user = user
        self.show_dashboard()

    def show_dashboard(self):
        self.clear_frame()
        self.current_frame = DashboardFrame(self, self.current_user)
        self.current_frame.pack(fill="both", expand=True)

    def show_shipments(self):
        self.clear_frame()
        self.current_frame = ShipmentFrame(self)
        self.current_frame.pack(fill="both", expand=True)

    def show_inventory(self):
        self.clear_frame()
        self.current_frame = InventoryFrame(self)
        self.current_frame.pack(fill="both", expand=True)

    def show_vehicles(self):
        self.clear_frame()
        self.current_frame = VehicleFrame(self)
        self.current_frame.pack(fill="both", expand=True)

    def show_drivers(self):
        self.clear_frame()
        self.current_frame = DriverFrame(self)
        self.current_frame.pack(fill="both", expand=True)

    def show_reports(self):
        self.clear_frame()
        self.current_frame = ReportsFrame(self)
        self.current_frame.pack(fill="both", expand=True)

    def show_facility(self):
        self.clear_frame()
        self.current_frame = FacilityFrame(self)
        self.current_frame.pack(fill="both", expand=True)

    def show_user_registry(self):
        self.clear_frame()
        self.current_frame = UserRegistryFrame(self)
        self.current_frame.pack(fill="both", expand=True)

    def show_security_audit(self):
        self.clear_frame()
        self.current_frame = SecurityAuditFrame(self)
        self.current_frame.pack(fill="both", expand=True)


if __name__ == "__main__":
    app = NorthshoreApp()
    app.mainloop()