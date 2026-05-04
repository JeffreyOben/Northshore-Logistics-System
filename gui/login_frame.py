import tkinter as tk
from tkinter import messagebox

from database import get_connection
from security import hash_password
from audit import log_activity


class LoginFrame(tk.Frame):
    def __init__(self, parent, on_login_success):
        super().__init__(parent, bg="#0F172A")

        self.parent = parent
        self.on_login_success = on_login_success

        self.build_ui()

    def build_ui(self):
        tk.Label(
            self,
            text="Northshore Logistics System",
            bg="#0F172A",
            fg="white",
            font=("Arial", 28, "bold")
        ).pack(pady=(70, 10))

        tk.Label(
            self,
            text="Secure Logistics Database Platform",
            bg="#0F172A",
            fg="#CBD5E1",
            font=("Arial", 15)
        ).pack(pady=(0, 30))

        card = tk.Frame(self, bg="#1E293B", padx=40, pady=35)
        card.pack()

        tk.Label(
            card,
            text="User Login",
            bg="#1E293B",
            fg="white",
            font=("Arial", 18, "bold")
        ).pack(pady=(0, 20))

        # Username
        tk.Label(card, text="Username", bg="#1E293B", fg="white").pack(anchor="w")
        self.username_entry = tk.Entry(card, width=35)
        self.username_entry.pack(pady=(6, 12), ipady=6)

        # Password
        tk.Label(card, text="Password", bg="#1E293B", fg="white").pack(anchor="w")
        self.password_entry = tk.Entry(card, width=35, show="*")
        self.password_entry.pack(pady=(6, 20), ipady=6)

        # LOGIN BUTTON (fixed)
        login_btn = tk.Label(
            card,
            text="Login",
            width=30,
            bg="#38BDF8",
            fg="#0F172A",
            font=("Arial", 12, "bold"),
            relief="raised",
            bd=2,
            cursor="hand2",
            padx=10,
            pady=8
        )
        login_btn.pack(pady=(0, 10))
        login_btn.bind("<Button-1>", lambda e: self.login())
        login_btn.bind("<Enter>", lambda e: login_btn.config(bg="#0284C7", fg="white"))
        login_btn.bind("<Leave>", lambda e: login_btn.config(bg="#38BDF8", fg="#0F172A"))

        # CREATE ACCOUNT BUTTON (fixed)
        create_btn = tk.Label(
            card,
            text="Create Account",
            width=30,
            bg="#10B981",
            fg="white",
            font=("Arial", 12, "bold"),
            relief="raised",
            bd=2,
            cursor="hand2",
            padx=10,
            pady=8
        )
        create_btn.pack(pady=(0, 10))
        create_btn.bind("<Button-1>", lambda e: self.create_account())
        create_btn.bind("<Enter>", lambda e: create_btn.config(bg="#047857"))
        create_btn.bind("<Leave>", lambda e: create_btn.config(bg="#10B981"))

        tk.Label(
            card,
            text="Default login: admin / admin123",
            bg="#1E293B",
            fg="#CBD5E1",
            font=("Arial", 10)
        ).pack(pady=(8, 0))

    def login(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()

        if not username or not password:
            messagebox.showerror("Login Failed", "Please enter username and password.")
            return

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT username, role, full_name
            FROM users
            WHERE username = ? AND password = ?
        """, (username, hash_password(password)))

        user = cursor.fetchone()
        conn.close()

        if user:
            log_activity(username, "logged in")
            self.on_login_success(user)
        else:
            messagebox.showerror("Login Failed", "Invalid username or password.")

    def create_account(self):
        window = tk.Toplevel(self)
        window.title("Create Account")
        window.geometry("460x430")
        window.configure(bg="#0F172A")

        tk.Label(
            window,
            text="Create New Account",
            bg="#0F172A",
            fg="white",
            font=("Arial", 20, "bold")
        ).pack(pady=(30, 20))

        form = tk.Frame(window, bg="#1E293B", padx=35, pady=30)
        form.pack()

        # Username
        tk.Label(form, text="Username", bg="#1E293B", fg="white").pack(anchor="w")
        username_entry = tk.Entry(form, width=32)
        username_entry.pack(pady=(6, 14), ipady=6)

        # Password
        tk.Label(form, text="Password", bg="#1E293B", fg="white").pack(anchor="w")
        password_entry = tk.Entry(form, width=32, show="*")
        password_entry.pack(pady=(6, 14), ipady=6)

        # Full name
        tk.Label(form, text="Full Name", bg="#1E293B", fg="white").pack(anchor="w")
        fullname_entry = tk.Entry(form, width=32)
        fullname_entry.pack(pady=(6, 18), ipady=6)

        def register():
            username = username_entry.get().strip()
            password = password_entry.get().strip()
            full_name = fullname_entry.get().strip()

            if not username or not password or not full_name:
                messagebox.showerror("Error", "All fields are required")
                return

            try:
                conn = get_connection()
                cursor = conn.cursor()

                cursor.execute("""
                    INSERT INTO users (username, password, role, full_name)
                    VALUES (?, ?, ?, ?)
                """, (username, hash_password(password), "staff", full_name))

                conn.commit()
                conn.close()

                messagebox.showinfo("Success", "Account created successfully")
                window.destroy()

            except Exception as e:
                messagebox.showerror("Error", str(e))

        # REGISTER BUTTON (fixed)
        register_btn = tk.Label(
            form,
            text="Register",
            width=28,
            bg="#38BDF8",
            fg="#0F172A",
            font=("Arial", 12, "bold"),
            relief="raised",
            bd=2,
            cursor="hand2",
            padx=10,
            pady=8
        )
        register_btn.pack()
        register_btn.bind("<Button-1>", lambda e: register())
        register_btn.bind("<Enter>", lambda e: register_btn.config(bg="#0284C7", fg="white"))
        register_btn.bind("<Leave>", lambda e: register_btn.config(bg="#38BDF8", fg="#0F172A"))