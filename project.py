from tkinter import *
from tkinter import ttk, messagebox
from datetime import datetime

# Data
name = "The Urban Table"
gst = 0.050
discount = 0

categories1 = {
    "Pizzas": {"Margherita Pizza": 250, "Farmhouse Pizza": 280, "Paneer Tikka Pizza": 320},
    "Burgers": {"Veggie Burger": 100, "Cheese Veggie Burger": 120, "Spicy Veg Burger": 140},
    "Sides and Starters": {"French Fries": 100, "Garlic Bread": 130, "Spring Rolls": 140, "Cheese Balls": 160},
}

categories2 = {
    "Pizzas": {"Chicken Delight Pizza": 300, "BBQ Chicken Pizza": 340, "Pepperoni Pizza": 370},
    "Burgers": {"Chicken Burger": 120, "Cheese Chicken Burger": 140, "Spicy Chicken Burger": 160},
    "Sides and Starters": {"Spicy Chicken Fries": 150, "Chicken Nuggets": 180, "Chicken Cheese Balls": 200},
}

categories3 = {
    "Desserts": {"Choco Lava Cake": 180, "Cheesecake": 250, "Chocolate Brownie": 270, "Chocolate Mousse": 280},
    "Beverages": {"Coke(500ml)": 50, "Sprite": 50, "Espresso": 100, "Cold Coffee": 120, "Cappuccino": 130}
}

# ---------------- WINDOW DESIGN ----------------
window = Tk()
window.title("Restaurant Ordering and Billing System")
window.geometry("600x750")
window.configure(bg="#FAF3E0")  # soft warm cream tone (background)

# ---------------- SCROLLABLE WRAPPER ----------------
container = Frame(window)
container.pack(fill=BOTH, expand=1)

canvas = Canvas(container, bg=window["bg"], highlightthickness=0)
vsb = ttk.Scrollbar(container, orient=VERTICAL, command=canvas.yview)
canvas.configure(yscrollcommand=vsb.set)

vsb.pack(side=RIGHT, fill=Y)
canvas.pack(side=LEFT, fill=BOTH, expand=1)

content_frame = Frame(canvas, bg=window["bg"])
inner_id = canvas.create_window((0, 0), window=content_frame, anchor="nw")

def _on_canvas_config(e):
    canvas.itemconfig(inner_id, width=e.width)
    canvas.configure(scrollregion=canvas.bbox("all"))

canvas.bind("<Configure>", _on_canvas_config)
content_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

def _on_mousewheel(event):
    delta = int(-1 * (event.delta / 120)) if event.delta else 0
    canvas.yview_scroll(delta, "units")

window.bind_all("<MouseWheel>", _on_mousewheel)
# -----------------------------------------------------

# ---------------- HEADER ----------------
header = Label(
    content_frame,
    text=name,
    font=("Georgia", 28, "bold"),
    bg="#4E342E",        # dark espresso brown
    fg="#FFD700",        # golden yellow text
    pady=10
)
header.pack(fill=X)

btn = None
entries = {}
prices = {}

# ---------------- CATEGORY FRAMES ----------------
def create_category_frame(root, category_name, items, color, title_color):
    frame = LabelFrame(
        root,
        text=category_name,
        font=("Georgia", 16, "bold"),
        bg=color,
        fg=title_color,
        padx=10,
        pady=10,
        labelanchor='n'
    )
    frame.pack(fill=X, padx=25, pady=10)

    Label(frame, text="Item", font=("Arial", 14, "bold"), width=20, bg=color, fg=title_color).grid(row=0, column=0)
    Label(frame, text="Price (₹)", font=("Arial", 14, "bold"), width=10, bg=color, fg=title_color).grid(row=0, column=1)
    Label(frame, text="Quantity", font=("Arial", 14, "bold"), width=10, bg=color, fg=title_color).grid(row=0, column=2)

    row_index = 1
    for item, price in items.items():
        Label(frame, text=item, font=("Arial", 12), width=20, bg=color, fg="white").grid(row=row_index, column=0)
        Label(frame, text=str(price), font=("Arial", 12), width=10, bg=color, fg="white").grid(row=row_index, column=1, padx=5)
        qty_entry = Spinbox(frame, width=10, from_=0, to=20, bg="#FFFBEA", fg="#2F1503", justify="center")
        qty_entry.grid(row=row_index, column=2, padx=5)
        qty_entry.insert(0, "0")
        entries[item] = qty_entry
        prices[item] = price
        row_index += 1

# ---------------- BUTTONS FOR CATEGORIES ----------------
def veg():
    veg_b.config(bg="#7CB342", fg="white", state=DISABLED)
    Label(content_frame, text="Vegetarian Delights 🥗", font=("Georgia", 20, "bold"), bg="#FAF3E0", fg="#4E342E").pack(anchor="center", pady=5)
    for category in categories1.keys():
        create_category_frame(content_frame, category, categories1[category], "#8BC34A", "#FFFBEA")

    global btn
    if btn:
        btn.pack_forget()
    btn = Button(content_frame, text="Generate Bill", font=("Georgia", 18, "bold"), bg="#6A1B9A", fg="white", activebackground="#4A0072", command=cal_bill)
    btn.pack(padx=10, pady=25)

def nonveg():
    nonveg_b.config(bg="#E53935", fg="white", state=DISABLED)
    Label(content_frame, text="Non-Vegetarian Feast 🍗", font=("Georgia", 20, "bold"), bg="#FAF3E0", fg="#4E342E").pack(anchor="center", pady=5)
    for category in categories2.keys():
        create_category_frame(content_frame, category, categories2[category], "#D84315", "#FFF8E1")

    global btn
    if btn:
        btn.pack_forget()
    btn = Button(content_frame, text="Generate Bill", font=("Georgia", 18, "bold"), bg="#6A1B9A", fg="white", activebackground="#4A0072", command=cal_bill)
    btn.pack(padx=10, pady=25)

def db():
    db_b.config(bg="#8E24AA", fg="white", state=DISABLED)
    Label(content_frame, text="Desserts & Beverages 🍰☕", font=("Georgia", 20, "bold"), bg="#FAF3E0", fg="#4E342E").pack(anchor="center", pady=5)
    for category in categories3.keys():
        create_category_frame(content_frame, category, categories3[category], "#AB47BC", "#FFFBEA")

    global btn
    if btn:
        btn.pack_forget()
    btn = Button(content_frame, text="Generate Bill", font=("Georgia", 18, "bold"), bg="#6A1B9A", fg="white", activebackground="#4A0072", command=cal_bill)
    btn.pack(padx=10, pady=25)

# ---------------- MENU CHOICE SECTION ----------------
label1 = Label(
    content_frame,
    text="What are you craving today?",
    font=("Georgia", 18, "bold"),
    bg="#FAF3E0",
    fg="#3E2723",
    pady=15
)
label1.pack(fill=X, padx=10, pady=15)

veg_b = Button(content_frame, text="Veg Menu", font=("Georgia", 16, "bold"), bg="#AED581", fg="#2F1503", activebackground="#7CB342", width=20, command=veg)
nonveg_b = Button(content_frame, text="Non-Veg Menu", font=("Georgia", 16, "bold"), bg="#EF9A9A", fg="#2F1503", activebackground="#E53935", width=20, command=nonveg)
db_b = Button(content_frame, text="Desserts & Beverages", font=("Georgia", 16, "bold"), bg="#CE93D8", fg="#2F1503", activebackground="#8E24AA", width=20, command=db)

veg_b.pack(padx=10, pady=15)
nonveg_b.pack(padx=10, pady=15)
db_b.pack(padx=10, pady=15)

# ---------------- BILL CALCULATION FUNCTION ----------------
def cal_bill():
    total = 0
    ordered_items = []

    for item, entry in entries.items():
        try:
            qty = int(entry.get())
        except:
            qty = 0
        if qty > 0:
            price = prices[item]
            subtotal = qty * price
            total += subtotal
            ordered_items.append((item, price, qty, subtotal))

    if not ordered_items:
        messagebox.showinfo("Empty Order", "Please select at least one item.")
        return

    if total >= 500 and total <= 1000:
        discount = 0.02
    elif total >= 1001 and total <= 2000:
        discount = 0.05
    elif total >= 2001:
        discount = 0.1
    else:
        discount = 0

    discount_amt = total * discount
    subtotal_after_discount = total - discount_amt
    gst_amt = subtotal_after_discount * gst
    final_total = subtotal_after_discount + gst_amt

    # ---------------- BILL WINDOW ----------------
    bill_window = Toplevel(window)
    bill_window.title("Your Bill")
    bill_window.geometry("550x700")
    bill_window.configure(bg="#FFF8E1")  # warm light yellow

    Label(bill_window, text=name, font=("Georgia", 26, "bold"), bg="#4E342E", fg="#FFD700", pady=10).pack(fill=X)
    Label(bill_window, text="Invoice", font=("Georgia", 20, "bold"), bg="#FFF8E1", fg="#4E342E", pady=10).pack()
    now = datetime.now().strftime("%d-%m-%Y %I:%M %p")
    Label(bill_window, text=f"{'Date & Time:':<35}{now}", font=("Courier New", 12), bg="#FFF8E1", fg="#4E342E").pack(pady=5,anchor="nw")

    bill_text = Text(bill_window, font=("Courier New", 12), bg="white", fg="#3E2723", padx=10, pady=10)
    bill_text.pack(fill=BOTH, expand=True)

    bill_text.insert(END, f"{'Item':25}{'Qty':>6}{'Price':>10}{'Total':>10}\n")
    bill_text.insert(END, "-"*52 + "\n")

    for item, price, qty, subtotal in ordered_items:
        bill_text.insert(END, f"{item:24}{qty:>6}{price:>10}{subtotal:>10}\n")
    bill_text.insert(END, "-"*52 + "\n")
    bill_text.insert(END, f"{'Subtotal':35}{total:>15.2f}\n")
    bill_text.insert(END, f"{f'Discount ({int(discount*100)}%)':35}{discount_amt:>15.2f}\n")
    bill_text.insert(END, f"{'GST (5%)':35}{gst_amt:>15.2f}\n")
    bill_text.insert(END, "-"*52 + "\n")
    bill_text.insert(END, f"{'Final Total':35}{final_total:>15.2f}\n")
    bill_text.insert(END, "\n\n        ☕ Thank you for dining with us ☕\n\n")
    bill_text.insert(END, "         Visit again at The Urban Table 💛\n")

# ---------------- END BILL FUNCTION ----------------
window.update_idletasks()
canvas.configure(scrollregion=canvas.bbox("all"))
window.mainloop()