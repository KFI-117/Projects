from tkinter import *
from tkinter import messagebox
import tkinter.ttk as ttk  # For Combobox

# Price data dictionary (moved to global scope for easy access)
priceData = {
    'Biscuit': 30,
    'Chicken': 250,
    'Egg': 10,
    'Fish': 200,
    'Coke': 50,
    'Bread': 30,
    'Apple': 350,
    'Onion': 55
}

# Store buying data
buyingData = {}

# Function to add product
def addProduct():
    product = productCombo.get()
    quantity = quantityEntry.get()
    
    if product == "" or quantity == "":
        messagebox.showwarning("Input Error", "Please select product and enter quantity!")
    else:
        try:
            qty = int(quantity)
            # Add to buyingData dictionary
            if product in buyingData:
                buyingData[product] += qty
            else:
                buyingData[product] = qty
            
            # Update the display listbox
            updateProductList()
            
            # Clear the quantity entry
            quantityEntry.delete(0, END)
            messagebox.showinfo("Success", f"{qty} {product}(s) added to cart!")
            
        except ValueError:
            messagebox.showerror("Input Error", "Quantity must be a number!")

# Function to remove selected product
def removeProduct():
    try:
        # Get selected item from listbox
        selected = productListbox.get(productListbox.curselection())
        # Extract product name (format: "Product: Quantity")
        product = selected.split(":")[0].strip()
        
        # Remove from buyingData
        if product in buyingData:
            del buyingData[product]
            updateProductList()
            messagebox.showinfo("Removed", f"{product} removed from cart!")
    except:
        messagebox.showwarning("Selection Error", "Please select a product to remove!")

# Update the product listbox
def updateProductList():
    # Clear the listbox
    productListbox.delete(0, END)
    
    # Add all products from buyingData
    for product, quantity in buyingData.items():
        productListbox.insert(END, f"{product}: {quantity}")

# Calculate bill function (similar to makeBill in original)
def calculateBill():
    if not buyingData:  # Check if cart is empty
        messagebox.showwarning("Empty Cart", "Please add products first!")
        return
    
    membership = membershipCombo.get()
    
    if membership == "":
        messagebox.showwarning("Input Error", "Please select membership type!")
        return
    
    # Calculate total bill amount
    billAmount = 0
    billDetails = "BILL DETAILS:\n"
    billDetails += "=" * 30 + "\n"
    
    for product, quantity in buyingData.items():
        if product in priceData:
            subtotal = priceData[product] * quantity
            billAmount += subtotal
            billDetails += f"{product}: ₹{priceData[product]} x {quantity} = ₹{subtotal}\n"
    
    billDetails += "=" * 30 + "\n"
    billDetails += f"Total before discount: ₹{billAmount}\n"
    
    # Apply discount (same logic as original getDiscount function)
    discount = 0
    if billAmount >= 25:
        if membership == 'Gold':
            discount = 5
            billAmount = billAmount * 0.95
        elif membership == 'Silver':
            discount = 3
            billAmount = billAmount * 0.97
        elif membership == 'Bronze':
            discount = 1
            billAmount = billAmount * 0.99
        
        billDetails += f"Discount applied: {discount}% for {membership} membership\n"
    else:
        billDetails += "No discount (amount less than ₹25)\n"
    
    billDetails += "=" * 30 + "\n"
    billDetails += f"FINAL AMOUNT TO PAY: ₹{billAmount:.2f}"
    
    # Show bill in messagebox
    messagebox.showinfo("Final Bill", billDetails)
    
    # Also update the bill display text widget
    billText.delete(1.0, END)  # Clear previous bill
    billText.insert(END, billDetails)

# Reset/clear all function
def resetAll():
    global buyingData
    buyingData = {}  # Clear the dictionary
    updateProductList()  # Update listbox
    quantityEntry.delete(0, END)  # Clear quantity
    billText.delete(1.0, END)  # Clear bill display
    membershipCombo.set('')  # Reset membership selection
    messagebox.showinfo("Reset", "All data cleared!")

# GUI Part
window = Tk()
window.geometry("800x500")
window.title("Cashier System - Student Project")

# Title Label
titleLabel = Label(window, text="SUPERMARKET CASHIER SYSTEM", 
                   font=("Arial", 16, "bold"), fg="blue")
titleLabel.place(x=250, y=10)

# Product Selection Frame
productFrame = LabelFrame(window, text="Product Selection", font=("Arial", 12))
productFrame.place(x=20, y=50, width=350, height=200)

# Product Dropdown
productLabel = Label(productFrame, text="Select Product:", font=("Arial", 10))
productLabel.place(x=10, y=20)

productCombo = ttk.Combobox(productFrame, values=list(priceData.keys()), 
                            font=("Arial", 10), width=15)
productCombo.place(x=120, y=20)

# Quantity Entry
quantityLabel = Label(productFrame, text="Quantity:", font=("Arial", 10))
quantityLabel.place(x=10, y=60)

quantityEntry = Entry(productFrame, font=("Arial", 10), width=10)
quantityEntry.place(x=120, y=60)

# Add Product Button
addBtn = Button(productFrame, text="Add Product", font=("Arial", 10, "bold"), 
                bg="lightgreen", command=addProduct)
addBtn.place(x=20, y=100)

# Remove Product Button
removeBtn = Button(productFrame, text="Remove Product", font=("Arial", 10, "bold"), 
                   bg="lightcoral", command=removeProduct)
removeBtn.place(x=140, y=100)

# Cart Display Frame
cartFrame = LabelFrame(window, text="Shopping Cart", font=("Arial", 12))
cartFrame.place(x=400, y=50, width=350, height=200)

# Listbox for cart items with scrollbar
scrollbar = Scrollbar(cartFrame)
scrollbar.pack(side=RIGHT, fill=Y)

productListbox = Listbox(cartFrame, font=("Arial", 10), width=30, height=8,
                         yscrollcommand=scrollbar.set)
productListbox.pack(padx=10, pady=10)

scrollbar.config(command=productListbox.yview)

# Membership Frame
membershipFrame = LabelFrame(window, text="Customer Membership", font=("Arial", 12))
membershipFrame.place(x=20, y=270, width=350, height=80)

# Membership Dropdown
membershipLabel = Label(membershipFrame, text="Membership:", font=("Arial", 10))
membershipLabel.place(x=10, y=20)

membershipCombo = ttk.Combobox(membershipFrame, 
                               values=['Gold', 'Silver', 'Bronze', 'None'], 
                               font=("Arial", 10), width=15)
membershipCombo.place(x=120, y=20)

# Bill Display Frame
billFrame = LabelFrame(window, text="Bill Details", font=("Arial", 12))
billFrame.place(x=400, y=270, width=350, height=180)

# Text widget for bill display
billText = Text(billFrame, font=("Courier", 9), width=40, height=10)
billText.pack(padx=10, pady=10)

# Buttons Frame
buttonFrame = Frame(window)
buttonFrame.place(x=20, y=370, width=350, height=50)

# Calculate Bill Button
calculateBtn = Button(buttonFrame, text="Calculate Bill", font=("Arial", 12, "bold"), 
                      bg="lightblue", command=calculateBill)
calculateBtn.place(x=20, y=10)

# Reset Button
resetBtn = Button(buttonFrame, text="Reset All", font=("Arial", 12, "bold"), 
                  bg="orange", command=resetAll)
resetBtn.place(x=180, y=10)

# Exit Button
exitBtn = Button(window, text="Exit", font=("Arial", 12, "bold"), 
                 bg="red", fg="white", command=window.destroy)
exitBtn.place(x=370, y=460)

# Initial update of product list
updateProductList()

window.mainloop()