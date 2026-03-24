class Library:
    def __init__(self, bookslist, name):
        self.booksList = bookslist
        self.name = name
        self.lendDict = {}

    def displayBooks(self):
        print(f'We have following books in our library: {self.name}')
        for book in self.booksList:
            print(book)

    def lendBook(self, book, user):
        # Clean the input to avoid mismatch from spaces/newlines
        book = book.strip()
        if book in self.booksList:
            if book not in self.lendDict:
                self.lendDict[book] = user
                print("Book has been lended. Database updated.")
            else:
                print(f'Book is already being used by {self.lendDict[book]}')
        else:
            print("Apologies! We don't have this book in our library")

    def addBook(self, book):
        book = book.strip()
        if book in self.booksList:
            print("Book already exists")
        else:
            self.booksList.append(book)
            with open(databaseName, 'a') as bookDatabase:
                bookDatabase.write('\n' + book)
            print("Book added")

    def returnBook(self, book):
        book = book.strip()
        if book in self.lendDict:
            self.lendDict.pop(book)
            print("Book returned successfully")
        else:
            print("The book does not exist in the Book Lending Database")


def main():
    while True:
        print(f'Welcome to the {library.name} library. Following are the options:')
        print('''
        1. Display Books
        2. Lend a Book
        3. Add a Book
        4. Return a Book
        ''')
        userInput = input('Press Q to quit and C to continue: ').strip().upper()
        if userInput == 'C':
            try:
                userChoice = int(input("Select an option to continue: "))
            except ValueError:
                print("Please enter a valid number pythonoption")
                continue

            if userChoice == 1:
                library.displayBooks()
            elif userChoice == 2:
                book = input("Enter the name of the book you want to lend: ").strip()
                user = input("Enter the name of the user: ").strip()
                library.lendBook(book, user)
            elif userChoice == 3:
                book = input("Enter the name of the book you want to add: ").strip()
                library.addBook(book)
            elif userChoice == 4:
                book = input("Enter the name of the book you want to return: ").strip()
                library.returnBook(book)
            else:
                print("Please choose a valid option")
        elif userInput == 'Q':
            break
        else:
            print("Please enter a valid option")


if __name__ == '__main__':
    booksList = []
    databaseName = input("Enter the name of the database file with extension: ").strip()
    with open(databaseName, 'r') as bookDatabase:
        for book in bookDatabase:
            booksList.append(book.strip())  # Strip here is key
    library = Library(booksList, "PythonX")
    main()