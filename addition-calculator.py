import tkinter as tk
from tkinter import font


def calculate_product():
    """Read inputs, compute product, and display the result."""
    try:
        num1 = float(entry1.get())
        num2 = float(entry2.get())
        product = num1 * num2
        # Format: show as integer if whole number, else up to 6 decimal places
        formatted = f"{product:,.6f}".rstrip("0").rstrip(".")
        result_var.set(f"{formatted}")
        result_label.config(fg="#22C55E")   # green on success
        error_label.config(text="")
    except ValueError:
        result_var.set("—")
        result_label.config(fg="#EF4444")   # red on error
        error_label.config(text="⚠  Please enter valid numbers in both fields.")


def clear_fields():
    """Reset all inputs and output."""
    entry1.delete(0, tk.END)
    entry2.delete(0, tk.END)
    result_var.set("—")
    result_label.config(fg=TEXT_MUTED)
    error_label.config(text="")
    entry1.focus()


# ── Palette ──────────────────────────────────────────────────────────────────
BG        = "#0F172A"   # deep navy canvas
SURFACE   = "#1E293B"   # card surface
BORDER    = "#334155"   # subtle border
ACCENT    = "#6366F1"   # indigo accent
ACCENT_HV = "#4F46E5"   # hover shade
TEXT      = "#F1F5F9"   # primary text
TEXT_MUTED= "#94A3B8"   # labels / placeholders
SUCCESS   = "#22C55E"
ERROR     = "#EF4444"
RADIUS    = 8


# ── Window ───────────────────────────────────────────────────────────────────
root = tk.Tk()
root.title("Product Calculator")
root.configure(bg=BG)
root.resizable(False, False)

# Centre on screen
W, H = 420, 440
root.geometry(f"{W}x{H}+{(root.winfo_screenwidth()-W)//2}+{(root.winfo_screenheight()-H)//2}")

# ── Fonts ────────────────────────────────────────────────────────────────────
f_title   = font.Font(family="Helvetica Neue", size=17, weight="bold")
f_label   = font.Font(family="Helvetica Neue", size=10, weight="bold")
f_entry   = font.Font(family="Helvetica Neue", size=13)
f_result  = font.Font(family="Helvetica Neue", size=28, weight="bold")
f_small   = font.Font(family="Helvetica Neue", size=9)


# ── Card frame ───────────────────────────────────────────────────────────────
card = tk.Frame(root, bg=SURFACE, bd=0, highlightthickness=1,
                highlightbackground=BORDER)
card.place(relx=0.5, rely=0.5, anchor="center", width=360, height=400)


# ── Header ───────────────────────────────────────────────────────────────────
header = tk.Frame(card, bg=ACCENT, height=6)
header.pack(fill="x", side="top")

tk.Label(card, text="Product Calculator", font=f_title,
         bg=SURFACE, fg=TEXT).pack(pady=(22, 2))
tk.Label(card, text="Multiply two numbers instantly",
         font=f_small, bg=SURFACE, fg=TEXT_MUTED).pack()


# ── Input helper ─────────────────────────────────────────────────────────────
def make_entry(parent, label_text):
    frame = tk.Frame(parent, bg=SURFACE)
    frame.pack(fill="x", padx=30, pady=(14, 0))
    tk.Label(frame, text=label_text, font=f_label,
             bg=SURFACE, fg=TEXT_MUTED).pack(anchor="w")
    e = tk.Entry(frame, font=f_entry, bg="#0F172A", fg=TEXT,
                 insertbackground=TEXT, relief="flat",
                 highlightthickness=1, highlightbackground=BORDER,
                 highlightcolor=ACCENT)
    e.pack(fill="x", ipady=8, pady=(4, 0))
    return e


entry1 = make_entry(card, "FIRST NUMBER")
entry2 = make_entry(card, "SECOND NUMBER")

# Bind Enter key
entry1.bind("<Return>", lambda e: entry2.focus())
entry2.bind("<Return>", lambda e: calculate_product())


# ── Buttons ───────────────────────────────────────────────────────────────────
btn_row = tk.Frame(card, bg=SURFACE)
btn_row.pack(fill="x", padx=30, pady=(20, 0))

def btn_style(btn, bg, fg=TEXT):
    btn.configure(bg=bg, fg=fg, activebackground=ACCENT_HV,
                  activeforeground=TEXT, relief="flat", bd=0,
                  font=f_label, cursor="hand2")

calc_btn = tk.Button(btn_row, text="Calculate  ×",
                     command=calculate_product)
btn_style(calc_btn, ACCENT)
calc_btn.pack(side="left", expand=True, fill="x", ipady=9, padx=(0, 6))

clear_btn = tk.Button(btn_row, text="Clear",
                      command=clear_fields)
btn_style(clear_btn, BORDER, TEXT_MUTED)
clear_btn.pack(side="left", fill="x", ipady=9, ipadx=16)


# ── Result area ───────────────────────────────────────────────────────────────
result_frame = tk.Frame(card, bg=BG, highlightthickness=1,
                        highlightbackground=BORDER)
result_frame.pack(fill="x", padx=30, pady=(18, 0))

tk.Label(result_frame, text="RESULT", font=f_label,
         bg=BG, fg=TEXT_MUTED).pack(pady=(10, 0))

result_var = tk.StringVar(value="—")
result_label = tk.Label(result_frame, textvariable=result_var,
                        font=f_result, bg=BG, fg=TEXT_MUTED)
result_label.pack(pady=(2, 12))


# ── Error message ─────────────────────────────────────────────────────────────
error_label = tk.Label(card, text="", font=f_small, bg=SURFACE, fg=ERROR,
                       wraplength=300, justify="center")
error_label.pack(pady=(8, 0))


entry1.focus()
root.mainloop()
