from tkinter import *
from tkinter import messagebox
import tkinter.ttk as ttk

class Library:
    def __init__(self, bookslist, name):
        self.booksList = bookslist
        self.name = name
        self.lendDict = {}
    
    def displayBooks(self):
        return self.booksList
    
    def lendBook(self, book, user):
        book = book.strip()
        if book in self.booksList:
            if book not in self.lendDict:
                self.lendDict[book] = user
                return True, f"✓ '{book}' lent to {user}"
            else:
                return False, f"✗ Already lent to {self.lendDict[book]}"
        else:
            return False, "✗ Book not in library"
    
    def addBook(self, book):
        book = book.strip()
        if book in self.booksList:
            return False, "✗ Book already exists"
        else:
            self.booksList.append(book)
            return True, f"✓ '{book}' added successfully"
    
    def returnBook(self, book):
        book = book.strip()
        if book in self.lendDict:
            user = self.lendDict.pop(book)
            return True, f"✓ '{book}' returned by {user}"
        else:
            return False, "✗ Book was not lent out"

# Create library with sample books
library = Library(['Python Basics', 'Java Guide', 'C++ for Beginners', 'Web Development', 
                   'Data Structures', 'Algorithms', 'Database Systems', 'Machine Learning'], 
                  "PythonX Library")

# GUI Functions
def displayBooks():
    books = library.displayBooks()
    availableListbox.delete(0, END)
    borrowedListbox.delete(0, END)
    
    for book in books:
        if book in library.lendDict:
            borrowedListbox.insert(END, f"{book} → {library.lendDict[book]}")
        else:
            availableListbox.insert(END, book)
    
    statsLabel.config(text=f"Total: {len(books)} | Available: {len(books)-len(library.lendDict)} | Lent: {len(library.lendDict)}")

def lendBook():
    if availableListbox.curselection():
        book = availableListbox.get(availableListbox.curselection())
        user = userEntry.get()
        
        if user == "":
            messagebox.showwarning("Input Error", "Enter user name!")
        else:
            success, message = library.lendBook(book, user)
            color = "green" if success else "red"
            resultLabel.config(text=message, fg=color)
            userEntry.delete(0, END)
            displayBooks()
    else:
        messagebox.showwarning("Selection Error", "Select a book from Available list!")

def addBook():
    book = addBookEntry.get()
    
    if book == "":
        messagebox.showwarning("Input Error", "Enter book name!")
    else:
        success, message = library.addBook(book)
        color = "green" if success else "red"
        resultLabel.config(text=message, fg=color)
        addBookEntry.delete(0, END)
        displayBooks()

def returnBook():
    if borrowedListbox.curselection():
        selected = borrowedListbox.get(borrowedListbox.curselection())
        book = selected.split(" → ")[0]
        
        success, message = library.returnBook(book)
        color = "green" if success else "red"
        resultLabel.config(text=message, fg=color)
        displayBooks()
    else:
        messagebox.showwarning("Selection Error", "Select a book from Borrowed list!")

def clearAll():
    userEntry.delete(0, END)
    addBookEntry.delete(0, END)
    resultLabel.config(text="Ready...", fg="black")

# GUI Setup
window = Tk()
window.geometry("800x750")
window.title("Library Management System - Advanced")
window.configure(bg="#f0f8ff")

# Title Frame
titleFrame = Frame(window, bg="#2c3e50", height=60)
titleFrame.pack(fill=X)

titleLabel = Label(titleFrame, text="📚 PYTHONX LIBRARY MANAGEMENT SYSTEM", 
                   font=("Arial", 18, "bold"), bg="#2c3e50", fg="white")
titleLabel.pack(pady=15)

# Main Content Frame
mainFrame = Frame(window, bg="#f0f8ff")
mainFrame.pack(pady=20, padx=20, fill=BOTH, expand=True)

# Left Panel - Available Books
leftFrame = LabelFrame(mainFrame, text="📖 AVAILABLE BOOKS", font=("Arial", 12, "bold"), 
                       bg="#f0f8ff", relief=GROOVE)
leftFrame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

availableScroll = Scrollbar(leftFrame)
availableScroll.pack(side=RIGHT, fill=Y)

availableListbox = Listbox(leftFrame, font=("Courier", 10), width=30, height=15,
                           yscrollcommand=availableScroll.set, selectbackground="#4CAF50")
availableListbox.pack(padx=10, pady=10)

availableScroll.config(command=availableListbox.yview)

# Middle Panel - Borrowed Books
middleFrame = LabelFrame(mainFrame, text="📚 BORROWED BOOKS", font=("Arial", 12, "bold"), 
                         bg="#f0f8ff", relief=GROOVE)
middleFrame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

borrowedScroll = Scrollbar(middleFrame)
borrowedScroll.pack(side=RIGHT, fill=Y)

borrowedListbox = Listbox(middleFrame, font=("Courier", 10), width=35, height=15,
                          yscrollcommand=borrowedScroll.set, selectbackground="#FF9800")
borrowedListbox.pack(padx=10, pady=10)

borrowedScroll.config(command=borrowedListbox.yview)

# Right Panel - Operations
rightFrame = LabelFrame(mainFrame, text="⚡ OPERATIONS", font=("Arial", 12, "bold"), 
                        bg="#f0f8ff", relief=GROOVE)
rightFrame.grid(row=0, column=2, padx=10, pady=10, sticky="nsew")

# Lend Section
lendFrame = LabelFrame(rightFrame, text="Lend Book", font=("Arial", 10), bg="#f0f8ff")
lendFrame.pack(padx=10, pady=10, fill=X)

Label(lendFrame, text="Select from Available list", bg="#f0f8ff").pack()

Label(lendFrame, text="User Name:", bg="#f0f8ff").pack(anchor=W, pady=(5,0))
userEntry = Entry(lendFrame, font=("Arial", 10))
userEntry.pack(fill=X, pady=(0,5))

lendBtn = Button(lendFrame, text="📥 LEND BOOK", font=("Arial", 10, "bold"), 
                 bg="#4CAF50", fg="white", command=lendBook)
lendBtn.pack(fill=X, pady=5)

# Add Book Section
addFrame = LabelFrame(rightFrame, text="Add New Book", font=("Arial", 10), bg="#f0f8ff")
addFrame.pack(padx=10, pady=10, fill=X)

Label(addFrame, text="Book Name:", bg="#f0f8ff").pack(anchor=W, pady=(5,0))
addBookEntry = Entry(addFrame, font=("Arial", 10))
addBookEntry.pack(fill=X, pady=(0,5))

addBtn = Button(addFrame, text="➕ ADD BOOK", font=("Arial", 10, "bold"), 
                bg="#2196F3", fg="white", command=addBook)
addBtn.pack(fill=X, pady=5)

# Return Book Section
returnFrame = LabelFrame(rightFrame, text="Return Book", font=("Arial", 10), bg="#f0f8ff")
returnFrame.pack(padx=10, pady=10, fill=X)

Label(returnFrame, text="Select from Borrowed list", bg="#f0f8ff").pack()

returnBtn = Button(returnFrame, text="📤 RETURN BOOK", font=("Arial", 10, "bold"), 
                   bg="#FF9800", fg="white", command=returnBook)
returnBtn.pack(fill=X, pady=10)

# Result Display
resultFrame = Frame(rightFrame, bg="#f0f8ff")
resultFrame.pack(padx=10, pady=10, fill=X)

resultLabel = Label(resultFrame, text="Ready...", font=("Arial", 10, "bold"), 
                    bg="#f0f8ff", height=2, relief=SUNKEN)
resultLabel.pack(fill=X)

# Bottom Panel - Stats and Actions
bottomFrame = Frame(window, bg="#f0f8ff")
bottomFrame.pack(pady=10, padx=20, fill=X)

# Statistics
statsLabel = Label(bottomFrame, text="", font=("Arial", 11, "bold"), 
                   bg="#f0f8ff", fg="#2c3e50")
statsLabel.pack(side=LEFT, padx=10)

# Action Buttons
actionFrame = Frame(bottomFrame, bg="#f0f8ff")
actionFrame.pack(side=RIGHT)

displayBtn = Button(actionFrame, text="🔄 REFRESH", font=("Arial", 10, "bold"), 
                    bg="#9C27B0", fg="white", command=displayBooks)
displayBtn.pack(side=LEFT, padx=5)

clearBtn = Button(actionFrame, text="🧹 CLEAR", font=("Arial", 10, "bold"), 
                  bg="#607D8B", fg="white", command=clearAll)
clearBtn.pack(side=LEFT, padx=5)

exitBtn = Button(actionFrame, text="🚪 EXIT", font=("Arial", 10, "bold"), 
                 bg="#F44336", fg="white", command=window.destroy)
exitBtn.pack(side=LEFT, padx=5)

# Configure grid weights
mainFrame.grid_columnconfigure(0, weight=1)
mainFrame.grid_columnconfigure(1, weight=1)
mainFrame.grid_columnconfigure(2, weight=1)

# Initial display
displayBooks()

window.mainloop()