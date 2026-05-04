import tkinter as tk
from tkinter import ttk

# ===== COLORS =====
BG = "#0F172A"          # dark background
TEXT = "#F8FAFC"        # white text
MUTED = "#CBD5E1"       # grey text
PRIMARY = "#38BDF8"     # blue
PRIMARY_DARK = "#0284C7"
DANGER = "#DC2626"
DANGER_DARK = "#991B1B"

ENTRY_BG = "#FFFFFF"    # white input
ENTRY_TEXT = "#000000"  # black text

# ===== FONTS =====
FONT_TITLE = ("Arial", 24, "bold")
FONT_SUBTITLE = ("Arial", 14, "bold")
FONT_LABEL = ("Arial", 11, "bold")
FONT_NORMAL = ("Arial", 11)


# ===== MAIN THEME FUNCTION =====
def apply_theme(window):
    window.configure(bg=BG)

    style = ttk.Style(window)
    style.theme_use("clam")

    # Table styling
    style.configure(
        "Treeview",
        background="white",
        foreground="black",
        fieldbackground="white",
        rowheight=28,
        font=FONT_NORMAL
    )

    style.configure(
        "Treeview.Heading",
        background=PRIMARY_DARK,
        foreground="white",
        font=("Arial", 11, "bold")
    )

    # Apply styles recursively
    def style_widget(widget):
        try:
            if isinstance(widget, tk.Frame):
                widget.configure(bg=BG)

            elif isinstance(widget, tk.Label):
                widget.configure(
                    bg=BG,
                    fg=TEXT,
                    font=FONT_LABEL
                )

            elif isinstance(widget, tk.Entry):
                widget.configure(
                    bg=ENTRY_BG,
                    fg=ENTRY_TEXT,
                    insertbackground=ENTRY_TEXT,
                    relief="solid",
                    bd=2,
                    font=FONT_NORMAL,
                    highlightbackground=PRIMARY,
                    highlightcolor=PRIMARY
                )

            elif isinstance(widget, tk.Button):
                widget.configure(
                    bg=PRIMARY,
                    fg="#0F172A",
                    activebackground=PRIMARY_DARK,
                    activeforeground="white",
                    font=("Arial", 11, "bold"),
                    relief="raised",
                    cursor="hand2",
                    highlightbackground=BG
                )

            elif isinstance(widget, tk.Text):
                widget.configure(
                    bg="white",
                    fg="black",
                    insertbackground="black",
                    font=FONT_NORMAL,
                    relief="solid",
                    bd=2,
                    highlightbackground=PRIMARY
                )

        except Exception:
            pass

        for child in widget.winfo_children():
            style_widget(child)

    style_widget(window)


# ===== OPTIONAL HELPERS =====
def apply_window_style(window, title=None, size=None):
    if title:
        window.title(title)
    if size:
        window.geometry(size)
    window.configure(bg=BG)


def label(parent, text, font=FONT_LABEL, fg=TEXT):
    return tk.Label(parent, text=text, font=font, bg=BG, fg=fg)


def entry(parent, width=30, show=None):
    return tk.Entry(
        parent,
        width=width,
        show=show,
        bg=ENTRY_BG,
        fg=ENTRY_TEXT,
        insertbackground=ENTRY_TEXT,
        font=FONT_NORMAL,
        relief="solid",
        bd=2
    )


def button(parent, text, command, width=18, bg=PRIMARY):
    return tk.Button(
        parent,
        text=text,
        command=command,
        width=width,
        bg=bg,
        fg="#0F172A",
        activebackground=PRIMARY_DARK,
        activeforeground="white",
        font=("Arial", 12, "bold"),
        relief="raised",
        cursor="hand2",
        padx=10,
        pady=6
    )


def danger_button(parent, text, command, width=18):
    return tk.Button(
        parent,
        text=text,
        command=command,
        width=width,
        bg=DANGER,
        fg="white",
        activebackground=DANGER_DARK,
        activeforeground="white",
        font=("Arial", 12, "bold"),
        relief="raised",
        cursor="hand2",
        padx=10,
        pady=6
    )