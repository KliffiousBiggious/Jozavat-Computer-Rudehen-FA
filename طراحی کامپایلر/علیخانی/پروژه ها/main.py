import tkinter as tk
from tkinter import ttk
import os, sys
from compiler import compile_cpp


def resource_path(path):
    try:
        base = sys._MEIPASS
    except:
        base = os.path.abspath(".")
    return os.path.join(base, path)


def open_pdf():
    os.startfile("project.pdf")


def run_compile():
    token_table.delete(*token_table.get_children())
    tree_box.delete("1.0", tk.END)

    result = compile_cpp(code_box.get("1.0", tk.END))

    if result[0] != "OK":
        status.config(text=f"{result[0]}: {result[1]}", fg="red")
        return

    status.config(text="Compilation Successful ✅", fg="green")

    for t in result[1]["tokens"]:
        token_table.insert("", "end", values=t)

    for node in result[1]["parse_tree"]:
        tree_box.insert(tk.END, node + "\n")


# ---------- GUI ----------
root = tk.Tk()
root.title("Educational C++ Compiler")
root.geometry("1000x720")

tk.Label(root, text="Educational C++ Compiler", font=("Arial", 16, "bold")).pack()
tk.Label(root, text="Amir Mahdi Mehrabian", font=("Arial", 12, "bold")).pack()

desc = (
    "این پروژه مربوط به درس طراحی کامپایلر می‌باشد و هدف آن\n"
    "پیاده‌سازی یک کامپایلر آموزشی برای زیرمجموعه‌ای از زبان ++C است.\n"
    "در این پروژه مراحل تحلیل لغوی، نحوی و معنایی بر روی\n"
    "دستورات مرتبط با اشاره‌گرها بررسی و پیاده‌سازی شده است.\n"
    "این کامپایلر صرفاً آموزشی بوده و یک کامپایلر کامل زبان ++C نیست."
)
tk.Label(root, text=desc, fg="navy", justify="center").pack(pady=5)

link = tk.Label(root, text="📄 باز کردن فایل PDF پروژه", fg="blue", cursor="hand2")
link.pack()
link.bind("<Button-1>", lambda e: open_pdf())

code_box = tk.Text(root, height=15, width=120)
code_box.pack(pady=5)

tk.Button(root, text="Compile", command=run_compile, bg="green", fg="white").pack(pady=5)
status = tk.Label(root, text="")
status.pack()

tabs = ttk.Notebook(root)
tabs.pack(expand=True, fill="both")

frame1 = ttk.Frame(tabs)
tabs.add(frame1, text="Token Table")
token_table = ttk.Treeview(frame1, columns=("Type", "Value"), show="headings")
token_table.heading("Type", text="Token Type")
token_table.heading("Value", text="Value")
token_table.pack(expand=True, fill="both")

frame2 = ttk.Frame(tabs)
tabs.add(frame2, text="Parse Tree")
tree_box = tk.Text(frame2)
tree_box.pack(expand=True, fill="both")

root.mainloop()
