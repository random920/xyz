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

    if name and qty.isdigit() and price.isdigit():
        inventory.append({"name": name, "qty": int(qty), "price": float(price)})
        save_data()
        refresh_table()
        clear_fields()
    else:
        messagebox.showwarning("Input Error", "Enter valid name, qty and price")

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

def refresh_table():
    tree.delete(*tree.get_children())
    for i, item in enumerate(inventory):
        tree.insert("", "end", iid=i, values=(item["name"], item["qty"], f"₹{item['price']}"))

def clear_fields():
    name_var.set("")
    qty_var.set("")
    price_var.set("")

root = tk.Tk()
root.title("Inventory Manager")
root.geometry("500x500")

name_var, qty_var, price_var = tk.StringVar(), tk.StringVar(), tk.StringVar()
inventory = load_data()

tk.Label(root, text="Product Name:").pack()
tk.Entry(root, textvariable=name_var).pack()
tk.Label(root, text="Quantity:").pack()
tk.Entry(root, textvariable=qty_var).pack()
tk.Label(root, text="Price:").pack()
tk.Entry(root, textvariable=price_var).pack()

tk.Button(root, text="Add Item", command=add_item).pack(pady=5)

tree = ttk.Treeview(root, columns=("Name", "Qty", "Price"), show="headings")
tree.heading("Name", text="Name")
tree.heading("Qty", text="Quantity")
tree.heading("Price", text="Price")
tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

btn_frame = tk.Frame(root)
btn_frame.pack()
tk.Button(btn_frame, text="Edit", command=edit_item).grid(row=0, column=0, padx=5)
tk.Button(btn_frame, text="Delete", command=delete_item).grid(row=0, column=1, padx=5)

refresh_table()
root.mainloop() 