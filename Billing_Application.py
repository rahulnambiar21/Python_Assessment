from tkinter import *
from tkinter import messagebox
import mysql.connector

# Function to connect to MySQL
def connect_to_mysql():
    try:
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="billing_app"
        )
        return mydb, mydb.cursor()
    except mysql.connector.Error as err:
        print("Error connecting to MySQL:", err)
        return None, None

# Function to retrieve product names from database
def get_product_names(cursor):
    try:
        cursor.execute("SELECT product_name FROM products")
        products = cursor.fetchall()
        return [product[0] for product in products]
    except mysql.connector.Error as err:
        print("Error fetching product names:", err)
        return []

# Function to add a bill to the database
def add_bill(customer_name, selected_products):
    try:
        # Connect to MySQL
        mydb, cursor = connect_to_mysql()
        if not mydb or not cursor:
            return
        
        # Insert customer into customers table
        cursor.execute("INSERT INTO customers (customer_name) VALUES (%s)", (customer_name,))
        customer_id = cursor.lastrowid  # Get the ID of the last inserted customer
        
        # Insert each product into bills table
        for product, quantity, total_price in selected_products:
            cursor.execute("INSERT INTO bills (customer_id, product_name, quantity, total_price) VALUES (%s, %s, %s, %s)",
                           (customer_id, product, quantity, total_price))
        
        # Commit changes and close connection
        mydb.commit()
        mydb.close()
        
        messagebox.showinfo("Success", "Bill generated successfully")
        entry_customer.delete(0,'end')
        entry_quantity.delete(0,'end')
        product_listbox.delete(0,'end')
    except mysql.connector.Error as err:
        print("Error inserting bill:", err)
        messagebox.showerror("Error", "Failed to generate bill. Please try again later.")

# Function to calculate total price based on selected products and quantities
def calculate_total(selected_products):
    total_price = sum(total_price for _, _, total_price in selected_products)
    return round(total_price, 2)

## Function to handle adding a product to the bill
def add_product():
    product = product_var.get()
    quantity = quantity_var.get()

    try:
        # Retrieve price of selected product
        cursor.execute("SELECT price FROM products WHERE product_name = %s", (product,))
        row = cursor.fetchone()
        if row is not None:
            price = row[0]
            total_price = price * quantity
            selected_products.append((product, quantity, total_price))
            product_listbox.insert(END, f"{product} - Quantity: {quantity} - Total: ${total_price:.2f}")
            total_price_var.set(f"Total Price: ${calculate_total(selected_products):.2f}")
        else:
            messagebox.showwarning("Product Not Found", f"Product '{product}' not found in database.")
    except mysql.connector.Error as err:
        print("Error retrieving product price:", err)
        messagebox.showerror("Error", "Failed to retrieve product price. Please try again later.")


# Create the main Tkinter window
root=Tk()
root.geometry("600x380")
root.title("My Tkinter Example")
root.resizable(width=False,height=False)

# Connect to MySQL
mydb, cursor = connect_to_mysql()
if not mydb or not cursor:
    messagebox.showerror("Error", "Failed to connect to the database. Please check your connection settings.")
    root.destroy()
    exit()

# Variables
customer_name_var = StringVar()
product_var = StringVar()
quantity_var = IntVar()
total_price_var = StringVar()
total_price_var.set("Total Price: Rs. 0.00")
selected_products = []

# Customer details
label_customer = Label(root, text="Customer Name:")
label_customer.grid(row=0, column=0, padx=10, pady=10)
entry_customer = Entry(root, textvariable=customer_name_var)
entry_customer.grid(row=0, column=1, padx=10, pady=10)

# Product selection
label_product = Label(root, text="Select Product:")
label_product.grid(row=1, column=0, padx=10, pady=10)
product_var.set("Select a Product")
products = get_product_names(cursor)
product_dropdown = OptionMenu(root,product_var,*products)
product_dropdown.grid(row=1, column=1, padx=10, pady=10)

# Quantity selection
label_quantity = Label(root, text="Quantity:")
label_quantity.grid(row=1, column=2, padx=10, pady=10)
entry_quantity = Entry(root, textvariable=quantity_var)
entry_quantity.grid(row=1, column=3, padx=10, pady=10)

# Button to add product to bill
add_button = Button(root, text="Add Product", command=add_product)
add_button.grid(row=1, column=4, padx=10, pady=10)

# Listbox to display selected products
product_listbox = Listbox(root, width=60)
product_listbox.grid(row=2, columnspan=5, padx=10, pady=10)

# Label for total price
label_total = Label(root, textvariable=total_price_var)
label_total.grid(row=3, column=0, columnspan=5, padx=10, pady=10)

# Button to generate bill
generate_bill_button = Button(root, text="Generate Bill", command=lambda: add_bill(customer_name_var.get(), selected_products))
generate_bill_button.grid(row=4, columnspan=5, padx=10, pady=10)

# Start the Tkinter main loop
root.mainloop()

# Close MySQL connection
if mydb.is_connected():
    mydb.close()
