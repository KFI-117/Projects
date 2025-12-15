from tkinter import *
from tkinter import messagebox

# Price data (same as original)
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

# Store buying data (same dictionary concept)
buyingData = {}

# Function to add product (replaces enterProducts loop)
def addProduct():
    product = enterProduct.get()
    quantity = enterQuantity.get()
    
    if product == "" or quantity == "":
        messagebox.showwarning("Input Error", "All fields are required!")
    else:
        try:
            qty = int(quantity)
            # Same dictionary update as original
            if product in priceData:
                if product in buyingData:
                    buyingData[product] += qty
                else:
                    buyingData[product] = qty
                
                # Clear entries (same pattern as your CRUD app)
                enterProduct.delete(0, "end")
                enterQuantity.delete(0, "end")
                
                # Update display (simple approach)
                updateDisplay()
                messagebox.showinfo("Success", "Product added!")
            else:
                messagebox.showwarning("Invalid Product", "Product not in price list!")
                
        except ValueError:
            messagebox.showerror("Input Error", "Quantity must be a number!")

# Function to calculate bill (same as original makeBill but with GUI)
def calculateBill():
    if not buyingData:
        messagebox.showwarning("Empty", "No products added!")
        return
    
    membership = enterMembership.get()
    
    if membership == "":
        messagebox.showwarning("Input Error", "Enter membership!")
        return
    
    # Same calculation logic as original
    billAmount = 0
    billText = "BILL:\n"
    
    for product, quantity in buyingData.items():
        subtotal = priceData[product] * quantity
        billAmount += subtotal
        billText += f"{product}: ₹{priceData[product]} x {quantity} = ₹{subtotal}\n"
    
    billText += f"\nTotal: ₹{billAmount}\n"
    
    # Same discount logic as original getDiscount
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
        billText += f"Discount: {discount}% for {membership}\n"
    else:
        billText += "No discount (less than ₹25)\n"
    
    billText += f"Final: ₹{billAmount:.2f}"
    
    # Show in messagebox (same as your CRUD app messages)
    messagebox.showinfo("Final Bill", billText)

# Function to reset (same pattern as your resetFields)
def resetAll():
    global buyingData
    buyingData = {}
    enterProduct.delete(0, "end")
    enterQuantity.delete(0, "end")
    enterMembership.delete(0, "end")
    displayBox.delete(0, END)
    messagebox.showinfo("Reset", "All cleared!")

# Simple display update (like your show() function)
def updateDisplay():
    displayBox.delete(0, END)
    for product, quantity in buyingData.items():
        displayBox.insert(END, f"{product}: {quantity}")

# GUI Part (EXACT same pattern as your teaching)
window = Tk()
window.geometry("600x500")
window.title("Cashier System")

# Labels (same as your CRUD app)
productLabel = Label(window, text="Product Name:", font=("Serif", 12))
productLabel.place(x=20, y=30)

quantityLabel = Label(window, text="Quantity:", font=("Serif", 12))
quantityLabel.place(x=20, y=70)

membershipLabel = Label(window, text="Membership:", font=("Serif", 12))
membershipLabel.place(x=20, y=110)

cartLabel = Label(window, text="Cart Items:", font=("Serif", 12))
cartLabel.place(x=20, y=150)

# Entry boxes (same as your CRUD app)
enterProduct = Entry(window)
enterProduct.place(x=150, y=30)

enterQuantity = Entry(window)
enterQuantity.place(x=150, y=70)

enterMembership = Entry(window)
enterMembership.place(x=150, y=110)

# Display box (same as your Listbox)
displayBox = Listbox(window, width=30, height=10)
displayBox.place(x=150, y=150)

# Buttons (same pattern as your CRUD app)
addBtn = Button(window, text="Add Product", font=("Sans", 12), bg="white", command=addProduct)
addBtn.place(x=350, y=200)

calculateBtn = Button(window, text="Calculate Bill", font=("Sans", 12), bg="white", command=calculateBill)
calculateBtn.place(x=480, y=200)

resetBtn = Button(window, text="Reset", font=("Sans", 12), bg="white", command=resetAll)
resetBtn.place(x=430, y=250)

exitBtn = Button(window, text="Exit", font=("Sans", 12), bg="white", command=window.destroy)
exitBtn.place(x=435, y=300)

# Price list display (static - just for reference)
priceLabel = Label(window, text="Available Products & Prices:", font=("Serif", 12))
priceLabel.place(x=350, y=30)

# Show price list
priceText = ""
for product, price in priceData.items():
    priceText += f"{product}: ₹{price}\n"

priceDisplay = Label(window, text=priceText, font=("Courier", 10), justify=LEFT)
priceDisplay.place(x=350, y=60)

window.mainloop()