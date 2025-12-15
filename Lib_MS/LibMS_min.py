from tkinter import *
from tkinter import messagebox

# Library class (UPDATED to track lending properly)
class Library:
    def __init__(self, bookslist, name):
        self.booksList = bookslist
        self.name = name
        self.lendDict = {}
    
    def getAvailableBooks(self):
        # Return only books that are NOT lent out
        available = []
        for book in self.booksList:
            if book not in self.lendDict:
                available.append(book)
        return available
    
    def getAllBooks(self):
        # Return all books in library
        return self.booksList
    
    def lendBook(self, book, user):
        book = book.strip()
        if book in self.booksList:
            if book not in self.lendDict:
                self.lendDict[book] = user
                return f"Book '{book}' lent to {user}"
            else:
                return f"Book already lent to {self.lendDict[book]}"
        else:
            return "Book not in library"
    
    def addBook(self, book):
        book = book.strip()
        if book in self.booksList:
            return "Book already exists"
        else:
            self.booksList.append(book)
            return f"Book '{book}' added"
    
    def returnBook(self, book):
        book = book.strip()
        if book in self.lendDict:
            self.lendDict.pop(book)
            return f"Book '{book}' returned"
        else:
            return "Book was not lent out"

# Create library with sample books
library = Library(['Python Basics', 'Java Guide', 'C++ for Beginners', 'Web Development'], "PythonX Library")

# GUI Functions (UPDATED with proper logic)
def displayBooks():
    available_books = library.getAvailableBooks()
    all_books = library.getAllBooks()
    
    # Clear and update listbox
    bookListbox.delete(0, END)
    for book in available_books:
        bookListbox.insert(END, book)
    
    # Show correct counts in message
    messagebox.showinfo("Library Status", 
                       f"Total books in library: {len(all_books)}\n"
                       f"Available for lending: {len(available_books)}\n"
                       f"Currently lent out: {len(library.lendDict)}")

def lendBook():
    book = bookEntry.get()
    user = userEntry.get()
    
    if book == "" or user == "":
        messagebox.showwarning("Input Error", "Enter both book and user!")
    else:
        result = library.lendBook(book, user)
        messagebox.showinfo("Lend Status", result)
        bookEntry.delete(0, END)
        userEntry.delete(0, END)
        displayBooks()  # Refresh the display

def addBook():
    book = newBookEntry.get()
    
    if book == "":
        messagebox.showwarning("Input Error", "Enter book name!")
    else:
        result = library.addBook(book)
        messagebox.showinfo("Add Status", result)
        newBookEntry.delete(0, END)
        displayBooks()  # Refresh the display

def returnBook():
    book = returnBookEntry.get()
    
    if book == "":
        messagebox.showwarning("Input Error", "Enter book name!")
    else:
        result = library.returnBook(book)
        messagebox.showinfo("Return Status", result)
        returnBookEntry.delete(0, END)
        displayBooks()  # Refresh the display

def resetFields():
    bookEntry.delete(0, END)
    userEntry.delete(0, END)
    newBookEntry.delete(0, END)
    returnBookEntry.delete(0, END)

def showLentBooks():
    if library.lendDict:
        lent_info = "Currently Lent Books:\n"
        for book, user in library.lendDict.items():
            lent_info += f"• {book} → {user}\n"
        messagebox.showinfo("Lent Books Info", lent_info)
    else:
        messagebox.showinfo("Lent Books Info", "No books are currently lent out.")

# GUI Setup (same layout, just added a button)
window = Tk()
window.geometry("650x500")  # Slightly wider
window.title("Library Management System")

# Title
titleLabel = Label(window, text="LIBRARY MANAGEMENT", font=("Serif", 16, "bold"))
titleLabel.place(x=200, y=10)

# Book Display Section
displayLabel = Label(window, text="Available Books:", font=("Serif", 12))
displayLabel.place(x=20, y=50)

bookListbox = Listbox(window, width=35, height=12)
bookListbox.place(x=20, y=80)

# Lend Book Section
lendLabel = Label(window, text="Lend a Book:", font=("Serif", 12))
lendLabel.place(x=320, y=50)

bookLabel = Label(window, text="Book Name:", font=("Serif", 10))
bookLabel.place(x=320, y=80)

bookEntry = Entry(window, width=25)
bookEntry.place(x=420, y=80)

userLabel = Label(window, text="User Name:", font=("Serif", 10))
userLabel.place(x=320, y=110)

userEntry = Entry(window, width=25)
userEntry.place(x=420, y=110)

lendBtn = Button(window, text="Lend Book", font=("Sans", 10), bg="white", command=lendBook)
lendBtn.place(x=320, y=140)

# Add Book Section
addLabel = Label(window, text="Add New Book:", font=("Serif", 12))
addLabel.place(x=320, y=180)

newBookLabel = Label(window, text="Book Name:", font=("Serif", 10))
newBookLabel.place(x=320, y=210)

newBookEntry = Entry(window, width=25)
newBookEntry.place(x=420, y=210)

addBtn = Button(window, text="Add Book", font=("Sans", 10), bg="white", command=addBook)
addBtn.place(x=320, y=240)

# Return Book Section
returnLabel = Label(window, text="Return a Book:", font=("Serif", 12))
returnLabel.place(x=320, y=280)

returnBookLabel = Label(window, text="Book Name:", font=("Serif", 10))
returnBookLabel.place(x=320, y=310)

returnBookEntry = Entry(window, width=25)
returnBookEntry.place(x=420, y=310)

returnBtn = Button(window, text="Return Book", font=("Sans", 10), bg="white", command=returnBook)
returnBtn.place(x=320, y=340)

# Action Buttons
displayBtn = Button(window, text="Display Books", font=("Sans", 12), bg="lightblue", command=displayBooks)
displayBtn.place(x=20, y=320)

lentBtn = Button(window, text="Show Lent Books", font=("Sans", 12), bg="lightyellow", command=showLentBooks)
lentBtn.place(x=150, y=320)

resetBtn = Button(window, text="Reset Fields", font=("Sans", 12), bg="white", command=resetFields)
resetBtn.place(x=20, y=370)

exitBtn = Button(window, text="Exit", font=("Sans", 12), bg="white", command=window.destroy)
exitBtn.place(x=150, y=370)

# Status Label (optional - shows current counts)
statusLabel = Label(window, text="Click 'Display Books' to see library status", 
                    font=("Serif", 10), fg="blue")
statusLabel.place(x=20, y=420)

# Initial display of books
displayBooks()

window.mainloop()