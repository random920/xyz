import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import json, os

FILE = "inventory.json"

def load_data():
    if os.path.exists(FILE):
        with open(FILE, "r") as f:
            return json.load(f)
    return []

def save_data():
    with open(FILE, "w") as f:
        json.dump(inventory, f)

def add_item():
    name = name_var.get().strip()
    qty = qty_var.get().strip()
    price = price_var.get().strip()

    if name and qty.isdigit() and price.replace('.', '', 1).isdigit():
        inventory.append({"name": name, "qty": int(qty), "price": float(price)})
        save_data()
        refresh_table()
        clear_fields()
    else:
        messagebox.showwarning("Input Error", "Enter valid name, quantity and price")

def edit_item():
    selected = tree.selection()
    if selected:
        idx = int(selected[0])
        item = inventory[idx]

        new_name = simpledialog.askstring("Edit Name", "Name:", initialvalue=item["name"])
        new_qty = simpledialog.askstring("Edit Quantity", "Quantity:", initialvalue=str(item["qty"]))
        new_price = simpledialog.askstring("Edit Price", "Price:", initialvalue=str(item["price"]))

        if new_name and new_qty.isdigit() and new_price.replace('.', '', 1).isdigit():
            inventory[idx] = {"name": new_name, "qty": int(new_qty), "price": float(new_price)}
            save_data()
            refresh_table()

def delete_item():
    selected = tree.selection()
    if selected:
        idx = int(selected[0])
        item = inventory[idx]
        confirm = messagebox.askyesno("Confirm Delete", f"Delete '{item['name']}'?")
        if confirm:
            inventory.pop(idx)
            save_data()
            refresh_table()

def refresh_table(filtered=None):
    tree.delete(*tree.get_children())
    data = filtered if filtered is not None else inventory
    for i, item in enumerate(data):
        tree.insert("", "end", iid=i, values=(item["name"], item["qty"], f"₹{item['price']}"))

def clear_fields():
    name_var.set("")
    qty_var.set("")
    price_var.set("")

def on_exit():
    if messagebox.askokcancel("Exit", "Do you really want to exit?"):
        root.destroy()

def search_items(*args):
    query = search_var.get().strip().lower()
    if query == "":
        refresh_table()
    else:
        filtered = [item for item in inventory if query in item["name"].lower()]
        refresh_table(filtered)

# ---------- Main Window ----------
root = tk.Tk()
root.title("Inventory Manager")
root.geometry("720x640")
root.configure(bg="#f0f4ff")
root.protocol("WM_DELETE_WINDOW", on_exit)

name_var, qty_var, price_var, search_var = tk.StringVar(), tk.StringVar(), tk.StringVar(), tk.StringVar()
inventory = load_data()

# Style
style = ttk.Style()
style.theme_use("default")
style.configure("Treeview", background="#ffffff", foreground="#000000", rowheight=25, fieldbackground="#ffffff")
style.map("Treeview", background=[("selected", "#cde1ff")])

# ---------- Main Layout Frame ----------
container = tk.Frame(root, bg="#f0f4ff")
container.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

# ---------- Input Fields ----------
tk.Label(container, text="Product Name:", bg="#f0f4ff").grid(row=0, column=0, sticky="e", padx=5, pady=2)
name_entry = tk.Entry(container, textvariable=name_var, width=30)
name_entry.grid(row=0, column=1, padx=5, pady=2)

tk.Label(container, text="Quantity:", bg="#f0f4ff").grid(row=1, column=0, sticky="e", padx=5, pady=2)
qty_entry = tk.Entry(container, textvariable=qty_var, width=30)
qty_entry.grid(row=1, column=1, padx=5, pady=2)

tk.Label(container, text="Price:", bg="#f0f4ff").grid(row=2, column=0, sticky="e", padx=5, pady=2)
price_entry = tk.Entry(container, textvariable=price_var, width=30)
price_entry.grid(row=2, column=1, padx=5, pady=2)

# Enter key navigation
name_entry.bind("<Return>", lambda e: qty_entry.focus_set())
qty_entry.bind("<Return>", lambda e: price_entry.focus_set())
price_entry.bind("<Return>", lambda e: add_item())

tk.Button(container, text="Add Item", command=add_item, bg="#87cefa", fg="white", activebackground="#4682b4", width=25).grid(row=3, column=0, columnspan=2, pady=10)

# ---------- Search ----------
tk.Label(container, text="Search:", bg="#f0f4ff").grid(row=4, column=0, sticky="e", padx=5, pady=5)
search_entry = tk.Entry(container, textvariable=search_var, width=30)
search_entry.grid(row=4, column=1, pady=5)
search_var.trace_add("write", search_items)

# ---------- Table ----------
tree_frame = tk.Frame(container, bg="#f0f4ff")
tree_frame.grid(row=5, column=0, columnspan=2, pady=10)

tree_scroll = tk.Scrollbar(tree_frame)
tree_scroll.pack(side=tk.RIGHT, fill=tk.Y)

tree = ttk.Treeview(tree_frame, columns=("Name", "Qty", "Price"), show="headings", yscrollcommand=tree_scroll.set, height=8)
tree.heading("Name", text="Name")
tree.heading("Qty", text="Quantity")
tree.heading("Price", text="Price")

# Center align columns
tree.column("Name", anchor="center", width=220)
tree.column("Qty", anchor="center", width=100)
tree.column("Price", anchor="center", width=100)

tree.pack(fill=tk.BOTH, expand=True)
tree_scroll.config(command=tree.yview)

# ---------- Buttons ----------
btn_frame = tk.Frame(container, bg="#f0f4ff")
btn_frame.grid(row=6, column=0, columnspan=2, pady=10)

tk.Button(btn_frame, text="Edit", command=edit_item, bg="#32cd32", fg="white", activebackground="#228b22", width=12).pack(side=tk.LEFT, padx=10)
tk.Button(btn_frame, text="Delete", command=delete_item, bg="#ff6347", fg="white", activebackground="#cd5c5c", width=12).pack(side=tk.LEFT, padx=10)

refresh_table()
root.mainloop()
