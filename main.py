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

# GUI
root = tk.Tk()
root.title("Inventory Manager")
root.geometry("520x550")
root.protocol("WM_DELETE_WINDOW", on_exit)  # Exit confirmation

name_var, qty_var, price_var, search_var = tk.StringVar(), tk.StringVar(), tk.StringVar(), tk.StringVar()
inventory = load_data()

# Input Fields
tk.Label(root, text="Product Name:").pack()
tk.Entry(root, textvariable=name_var).pack()
tk.Label(root, text="Quantity:").pack()
tk.Entry(root, textvariable=qty_var).pack()
tk.Label(root, text="Price:").pack()
tk.Entry(root, textvariable=price_var).pack()
tk.Button(root, text="Add Item", command=add_item).pack(pady=5)

# Search Bar
tk.Label(root, text="Search:").pack()
search_entry = tk.Entry(root, textvariable=search_var)
search_entry.pack(pady=5)
search_var.trace_add("write", search_items)

# Treeview with Scrollbar
frame = tk.Frame(root)
frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

tree_scroll = tk.Scrollbar(frame)
tree_scroll.pack(side=tk.RIGHT, fill=tk.Y)

tree = ttk.Treeview(frame, columns=("Nam
