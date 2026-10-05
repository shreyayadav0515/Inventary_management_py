import tkinter as tk
from tkinter import ttk, messagebox


# =========================================================
# DATA STORAGE
# =========================================================

inventory = []
expenses = []


# =========================================================
# COLORS
# =========================================================

BACKGROUND = "#F0F9FF"      # Very light blue
SIDEBAR = "#2563EB"         # Bright blue
CARD = "#FFFFFF"            # White
ENTRY = "#E0F2FE"           # Light sky blue
TEXT = "#172554"            # Dark blue text
SUBTEXT = "#475569"         # Gray-blue text

BLUE = "#06B6D4"            # Cyan
GREEN = "#22C55E"           # Green
RED = "#F43F5E"             # Bright red
YELLOW = "#F59E0B"          # Orange-yellow
PURPLE = "#8B5CF6"          # Purple


# =========================================================
# MAIN WINDOW
# =========================================================

root = tk.Tk()
root.title("Inventory and Expense Management System")
root.geometry("1200x720")
root.minsize(1000, 600)
root.configure(bg=BACKGROUND)


# =========================================================
# GENERAL FUNCTIONS
# =========================================================

def clear_entry(entry):
    entry.delete(0, tk.END)


def create_entry(parent):
    entry = tk.Entry(
        parent,
        bg=ENTRY,
        fg=TEXT,
        insertbackground=TEXT,
        relief="flat",
        font=("Segoe UI", 10)
    )
    entry.pack(fill="x", padx=20, pady=(3, 12), ipady=8)
    return entry


def create_button(parent, text, command, color=BLUE):
    button = tk.Button(
        parent,
        text=text,
        command=command,
        bg=color,
        fg="#07111F",
        activebackground="#BAE6FD",
        activeforeground="#07111F",
        relief="flat",
        bd=0,
        cursor="hand2",
        font=("Segoe UI", 10, "bold"),
        padx=12,
        pady=9
    )
    return button


def update_dashboard():
    product_count_label.config(text=str(len(inventory)))
    expense_count_label.config(text=str(len(expenses)))

    total = sum(expense["amount"] for expense in expenses)
    total_expense_label.config(text=f"₹{total:.2f}")

    low_stock_total = sum(
        1 for product in inventory if product["quantity"] <= 5
    )
    low_stock_label.config(text=str(low_stock_total))


# =========================================================
# INVENTORY FUNCTIONS
# =========================================================

def add_product():
    product_id = product_id_entry.get().strip()
    name = product_name_entry.get().strip()
    price_text = price_entry.get().strip()
    quantity_text = quantity_entry.get().strip()

    if not product_id or not name or not price_text or not quantity_text:
        messagebox.showwarning(
            "Incomplete Details",
            "Please fill in all product fields."
        )
        return

    try:
        price = float(price_text)
        quantity = int(quantity_text)

        if price < 0 or quantity < 0:
            raise ValueError

    except ValueError:
        messagebox.showerror(
            "Invalid Details",
            "Price must be a number and quantity must be a positive integer."
        )
        return

    for product in inventory:
        if product["id"] == product_id:
            messagebox.showerror(
                "Duplicate Product ID",
                "A product with this ID already exists."
            )
            return

    product = {
        "id": product_id,
        "name": name,
        "price": price,
        "quantity": quantity
    }

    inventory.append(product)

    clear_entry(product_id_entry)
    clear_entry(product_name_entry)
    clear_entry(price_entry)
    clear_entry(quantity_entry)

    refresh_inventory_table()
    update_dashboard()

    messagebox.showinfo(
        "Product Added",
        "Product added successfully."
    )


def delete_product():
    selected_item = inventory_table.selection()

    if not selected_item:
        messagebox.showwarning(
            "No Product Selected",
            "Select a product from the table before deleting it."
        )
        return

    selected_data = inventory_table.item(selected_item[0])
    product_id = selected_data["values"][0]

    confirm = messagebox.askyesno(
        "Confirm Delete",
        "Are you sure you want to delete this product?"
    )

    if not confirm:
        return

    for product in inventory:
        if product["id"] == product_id:
            inventory.remove(product)
            break

    refresh_inventory_table()
    update_dashboard()

    messagebox.showinfo(
        "Product Deleted",
        "Product deleted successfully."
    )


def update_stock():
    selected_item = inventory_table.selection()

    if not selected_item:
        messagebox.showwarning(
            "No Product Selected",
            "Select a product from the table first."
        )
        return

    selected_data = inventory_table.item(selected_item[0])
    product_id = selected_data["values"][0]

    update_window = tk.Toplevel(root)
    update_window.title("Update Stock")
    update_window.geometry("350x220")
    update_window.configure(bg=CARD)
    update_window.resizable(False, False)

    tk.Label(
        update_window,
        text="Update Product Quantity",
        bg=CARD,
        fg=TEXT,
        font=("Segoe UI", 15, "bold")
    ).pack(pady=(25, 15))

    tk.Label(
        update_window,
        text=f"Product ID: {product_id}",
        bg=CARD,
        fg=SUBTEXT,
        font=("Segoe UI", 10)
    ).pack()

    quantity_box = tk.Entry(
        update_window,
        bg=ENTRY,
        fg=TEXT,
        insertbackground=TEXT,
        relief="flat",
        font=("Segoe UI", 11)
    )
    quantity_box.pack(padx=40, pady=15, fill="x", ipady=8)

    def save_quantity():
        try:
            new_quantity = int(quantity_box.get())

            if new_quantity < 0:
                raise ValueError

        except ValueError:
            messagebox.showerror(
                "Invalid Quantity",
                "Enter a valid positive integer."
            )
            return

        for product in inventory:
            if product["id"] == product_id:
                product["quantity"] = new_quantity
                break

        refresh_inventory_table()
        update_dashboard()
        update_window.destroy()

        messagebox.showinfo(
            "Stock Updated",
            "Product quantity updated successfully."
        )

    create_button(
        update_window,
        "Save Quantity",
        save_quantity,
        GREEN
    ).pack(pady=5)


def search_product():
    search_text = search_entry.get().strip().lower()

    for item in search_table.get_children():
        search_table.delete(item)

    if not search_text:
        messagebox.showwarning(
            "Search",
            "Enter a product ID or product name."
        )
        return

    found = False

    for product in inventory:
        if (
            product["id"].lower() == search_text
            or product["name"].lower() == search_text
        ):
            search_table.insert(
                "",
                tk.END,
                values=(
                    product["id"],
                    product["name"],
                    f"₹{product['price']:.2f}",
                    product["quantity"]
                )
            )
            found = True

    if not found:
        messagebox.showinfo(
            "Search Result",
            "Product not found."
        )


def refresh_inventory_table():
    for item in inventory_table.get_children():
        inventory_table.delete(item)

    for product in inventory:
        inventory_table.insert(
            "",
            tk.END,
            values=(
                product["id"],
                product["name"],
                f"₹{product['price']:.2f}",
                product["quantity"]
            )
        )


# =========================================================
# EXPENSE FUNCTIONS
# =========================================================

def add_expense():
    category = category_entry.get().strip()
    description = description_entry.get().strip()
    amount_text = amount_entry.get().strip()

    if not category or not description or not amount_text:
        messagebox.showwarning(
            "Incomplete Details",
            "Please fill in all expense fields."
        )
        return

    try:
        amount = float(amount_text)

        if amount < 0:
            raise ValueError

    except ValueError:
        messagebox.showerror(
            "Invalid Amount",
            "Enter a valid expense amount."
        )
        return

    expense = {
        "category": category,
        "description": description,
        "amount": amount
    }

    expenses.append(expense)

    clear_entry(category_entry)
    clear_entry(description_entry)
    clear_entry(amount_entry)

    refresh_expense_table()
    update_dashboard()

    messagebox.showinfo(
        "Expense Added",
        "Expense added successfully."
    )


def refresh_expense_table():
    for item in expense_table.get_children():
        expense_table.delete(item)

    for expense in expenses:
        expense_table.insert(
            "",
            tk.END,
            values=(
                expense["category"],
                expense["description"],
                f"₹{expense['amount']:.2f}"
            )
        )


def show_low_stock():
    for item in low_stock_table.get_children():
        low_stock_table.delete(item)

    found = False

    for product in inventory:
        if product["quantity"] <= 5:
            low_stock_table.insert(
                "",
                tk.END,
                values=(
                    product["id"],
                    product["name"],
                    product["quantity"]
                )
            )
            found = True

    if not found:
        messagebox.showinfo(
            "Low Stock Report",
            "There are no low-stock products."
        )


# =========================================================
# SIDEBAR
# =========================================================

sidebar = tk.Frame(root, bg=SIDEBAR, width=235)
sidebar.pack(side="left", fill="y")
sidebar.pack_propagate(False)

tk.Label(
    sidebar,
    text="STOCKIFY",
    bg=SIDEBAR,
    fg=BLUE,
    font=("Segoe UI", 23, "bold")
).pack(pady=(35, 3))

tk.Label(
    sidebar,
    text="Inventory Management",
    bg=SIDEBAR,
    fg=SUBTEXT,
    font=("Segoe UI", 9)
).pack(pady=(0, 35))


def sidebar_button(text, command):
    button = tk.Button(
        sidebar,
        text=text,
        command=command,
        bg=SIDEBAR,
        fg=TEXT,
        activebackground="#26354D",
        activeforeground=BLUE,
        anchor="w",
        relief="flat",
        bd=0,
        cursor="hand2",
        font=("Segoe UI", 10, "bold"),
        padx=25,
        pady=13
    )
    button.pack(fill="x")
    return button


# =========================================================
# MAIN CONTENT AREA
# =========================================================

content = tk.Frame(root, bg=BACKGROUND)
content.pack(side="right", fill="both", expand=True)

header = tk.Frame(content, bg=BACKGROUND)
header.pack(fill="x", padx=30, pady=(25, 10))

tk.Label(
    header,
    text="Dashboard",
    bg=BACKGROUND,
    fg=TEXT,
    font=("Segoe UI", 27, "bold")
).pack(side="left")

tk.Label(
    header,
    text="Expense Tracker and Inventory System",
    bg=BACKGROUND,
    fg=SUBTEXT,
    font=("Segoe UI", 10)
).pack(side="right", pady=10)


# =========================================================
# DASHBOARD CARDS
# =========================================================

cards = tk.Frame(content, bg=BACKGROUND)
cards.pack(fill="x", padx=30, pady=12)


def dashboard_card(title, value, color):
    card = tk.Frame(cards, bg=CARD, height=105)
    card.pack(side="left", fill="both", expand=True, padx=6)
    card.pack_propagate(False)

    tk.Label(
        card,
        text=title,
        bg=CARD,
        fg=SUBTEXT,
        font=("Segoe UI", 10)
    ).pack(anchor="w", padx=18, pady=(15, 3))

    label = tk.Label(
        card,
        text=value,
        bg=CARD,
        fg=color,
        font=("Segoe UI", 22, "bold")
    )
    label.pack(anchor="w", padx=18)

    return label


product_count_label = dashboard_card(
    "Total Products", "0", BLUE
)

expense_count_label = dashboard_card(
    "Expense Records", "0", GREEN
)

total_expense_label = dashboard_card(
    "Total Expenses", "₹0.00", YELLOW
)

low_stock_label = dashboard_card(
    "Low Stock Products", "0", RED
)


# =========================================================
# TABS
# =========================================================

style = ttk.Style()
style.theme_use("clam")

style.configure(
    "TNotebook",
    background=BACKGROUND,
    borderwidth=0
)

style.configure(
    "TNotebook.Tab",
    background=CARD,
    foreground=TEXT,
    padding=(20, 10),
    font=("Segoe UI", 10, "bold")
)

style.map(
    "TNotebook.Tab",
    background=[("selected", BLUE)],
    foreground=[("selected", "#07111F")]
)

style.configure(
    "Treeview",
    background=CARD,
    fieldbackground=CARD,
    foreground=TEXT,
    rowheight=35,
    borderwidth=0,
    font=("Segoe UI", 10)
)

style.configure(
    "Treeview.Heading",
    background=BLUE,
    foreground="#07111F",
    font=("Segoe UI", 10, "bold"),
    padding=8
)

style.map(
    "Treeview",
    background=[("selected", "#0369A1")],
    foreground=[("selected", TEXT)]
)

notebook = ttk.Notebook(content)
notebook.pack(fill="both", expand=True, padx=30, pady=15)


# =========================================================
# INVENTORY TAB
# =========================================================

inventory_tab = tk.Frame(notebook, bg=BACKGROUND)
notebook.add(inventory_tab, text="  Inventory  ")

product_form = tk.Frame(inventory_tab, bg=CARD, width=285)
product_form.pack(side="left", fill="y", padx=(0, 15))
product_form.pack_propagate(False)

tk.Label(
    product_form,
    text="Add Product",
    bg=CARD,
    fg=TEXT,
    font=("Segoe UI", 16, "bold")
).pack(anchor="w", padx=20, pady=(25, 18))

tk.Label(
    product_form,
    text="Product ID",
    bg=CARD,
    fg=SUBTEXT
).pack(anchor="w", padx=20)

product_id_entry = create_entry(product_form)

tk.Label(
    product_form,
    text="Product Name",
    bg=CARD,
    fg=SUBTEXT
).pack(anchor="w", padx=20)

product_name_entry = create_entry(product_form)

tk.Label(
    product_form,
    text="Product Price",
    bg=CARD,
    fg=SUBTEXT
).pack(anchor="w", padx=20)

price_entry = create_entry(product_form)

tk.Label(
    product_form,
    text="Quantity",
    bg=CARD,
    fg=SUBTEXT
).pack(anchor="w", padx=20)

quantity_entry = create_entry(product_form)

create_button(
    product_form,
    "＋  Add Product",
    add_product,
    GREEN
).pack(fill="x", padx=20, pady=(8, 10))

create_button(
    product_form,
    "Clear Boxes",
    lambda: [
        clear_entry(product_id_entry),
        clear_entry(product_name_entry),
        clear_entry(price_entry),
        clear_entry(quantity_entry)
    ],
    PURPLE
).pack(fill="x", padx=20)


inventory_area = tk.Frame(inventory_tab, bg=BACKGROUND)
inventory_area.pack(side="right", fill="both", expand=True)

inventory_toolbar = tk.Frame(inventory_area, bg=BACKGROUND)
inventory_toolbar.pack(fill="x", pady=(0, 10))

create_button(
    inventory_toolbar,
    "Update Selected Stock",
    update_stock,
    BLUE
).pack(side="left", padx=4)

create_button(
    inventory_toolbar,
    "Delete Selected Product",
    delete_product,
    RED
).pack(side="left", padx=4)

inventory_table = ttk.Treeview(
    inventory_area,
    columns=("ID", "Name", "Price", "Quantity"),
    show="headings"
)

inventory_table.heading("ID", text="Product ID")
inventory_table.heading("Name", text="Product Name")
inventory_table.heading("Price", text="Price")
inventory_table.heading("Quantity", text="Quantity")

inventory_table.column("ID", width=120)
inventory_table.column("Name", width=240)
inventory_table.column("Price", width=130)
inventory_table.column("Quantity", width=110)

inventory_table.pack(fill="both", expand=True)


# =========================================================
# SEARCH TAB
# =========================================================

search_tab = tk.Frame(notebook, bg=BACKGROUND)
notebook.add(search_tab, text="  Search Product  ")

search_panel = tk.Frame(search_tab, bg=CARD)
search_panel.pack(fill="x", pady=(0, 15))

tk.Label(
    search_panel,
    text="Enter Product ID or Name:",
    bg=CARD,
    fg=SUBTEXT,
    font=("Segoe UI", 10)
).pack(side="left", padx=(20, 10), pady=20)

search_entry = tk.Entry(
    search_panel,
    bg=ENTRY,
    fg=TEXT,
    insertbackground=TEXT,
    relief="flat",
    width=35,
    font=("Segoe UI", 10)
)
search_entry.pack(side="left", padx=10, ipady=8)

create_button(
    search_panel,
    "Search Product",
    search_product,
    BLUE
).pack(side="left", padx=10)

search_table = ttk.Treeview(
    search_tab,
    columns=("ID", "Name", "Price", "Quantity"),
    show="headings"
)

search_table.heading("ID", text="Product ID")
search_table.heading("Name", text="Product Name")
search_table.heading("Price", text="Price")
search_table.heading("Quantity", text="Quantity")

search_table.pack(fill="both", expand=True)


# =========================================================
# EXPENSE TAB
# =========================================================

expense_tab = tk.Frame(notebook, bg=BACKGROUND)
notebook.add(expense_tab, text="  Expenses  ")

expense_form = tk.Frame(expense_tab, bg=CARD, width=285)
expense_form.pack(side="left", fill="y", padx=(0, 15))
expense_form.pack_propagate(False)

tk.Label(
    expense_form,
    text="Add Expense",
    bg=CARD,
    fg=TEXT,
    font=("Segoe UI", 16, "bold")
).pack(anchor="w", padx=20, pady=(25, 18))

tk.Label(
    expense_form,
    text="Expense Category",
    bg=CARD,
    fg=SUBTEXT
).pack(anchor="w", padx=20)

category_entry = create_entry(expense_form)

tk.Label(
    expense_form,
    text="Description",
    bg=CARD,
    fg=SUBTEXT
).pack(anchor="w", padx=20)

description_entry = create_entry(expense_form)

tk.Label(
    expense_form,
    text="Amount",
    bg=CARD,
    fg=SUBTEXT
).pack(anchor="w", padx=20)

amount_entry = create_entry(expense_form)

create_button(
    expense_form,
    "＋  Add Expense",
    add_expense,
    GREEN
).pack(fill="x", padx=20, pady=(8, 10))

create_button(
    expense_form,
    "Clear Boxes",
    lambda: [
        clear_entry(category_entry),
        clear_entry(description_entry),
        clear_entry(amount_entry)
    ],
    PURPLE
).pack(fill="x", padx=20)


expense_area = tk.Frame(expense_tab, bg=BACKGROUND)
expense_area.pack(side="right", fill="both", expand=True)

expense_table = ttk.Treeview(
    expense_area,
    columns=("Category", "Description", "Amount"),
    show="headings"
)

expense_table.heading("Category", text="Category")
expense_table.heading("Description", text="Description")
expense_table.heading("Amount", text="Amount")

expense_table.column("Category", width=160)
expense_table.column("Description", width=280)
expense_table.column("Amount", width=130)

expense_table.pack(fill="both", expand=True)


# =========================================================
# LOW STOCK TAB
# =========================================================

low_stock_tab = tk.Frame(notebook, bg=BACKGROUND)
notebook.add(low_stock_tab, text="  Low Stock Report  ")

create_button(
    low_stock_tab,
    "Refresh Low Stock Report",
    show_low_stock,
    YELLOW
).pack(anchor="w", pady=(0, 15))

low_stock_table = ttk.Treeview(
    low_stock_tab,
    columns=("ID", "Name", "Quantity"),
    show="headings"
)

low_stock_table.heading("ID", text="Product ID")
low_stock_table.heading("Name", text="Product Name")
low_stock_table.heading("Quantity", text="Quantity")

low_stock_table.column("ID", width=160)
low_stock_table.column("Name", width=280)
low_stock_table.column("Quantity", width=150)

low_stock_table.pack(fill="both", expand=True)


# =========================================================
# SIDEBAR BUTTONS
# =========================================================

sidebar_button(
    "▣   Dashboard",
    lambda: notebook.select(0)
)

sidebar_button(
    "▤   Inventory",
    lambda: notebook.select(0)
)

sidebar_button(
    "⌕   Search Product",
    lambda: notebook.select(1)
)

sidebar_button(
    "₹   Expenses",
    lambda: notebook.select(2)
)

sidebar_button(
    "⚠   Low Stock",
    lambda: notebook.select(3)
)


def exit_application():
    answer = messagebox.askyesno(
        "Exit Application",
        "Are you sure you want to exit?"
    )

    if answer:
        root.destroy()


sidebar_button("⏻   Exit", exit_application)


# =========================================================
# START APPLICATION
# =========================================================

update_dashboard()
root.mainloop()
