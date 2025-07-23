import pandas as pd

# Note: ISBN is a unique identifier for each book

def load_books():  
    """Loads books from the Excel file."""
    try:
        df = pd.read_excel("books_in_library.xlsx")
        df['ISBN'] = df['ISBN'].astype(str).str.strip()  # Ensure ISBN is a string
        if 'Issued_Copies' not in df.columns:  # Add Issued_Copies column if missing
            df['Issued_Copies'] = 0
        return df
    except FileNotFoundError:
        print("The file is not found. Creating a new one...")
        return pd.DataFrame(columns=["Title", "Author", "ISBN", "Copies", "Issued_Copies"])

def save_books(df):  
    """Saves the books after modifications."""
    df.to_excel("books_in_library.xlsx", index=False)

def view_books():
    """Displays all books."""
    df = load_books()
    print(df)

def search_books(key):
    """Searches for a book by title."""
    df = load_books()
    results = df[df['Title'].str.contains(key, case=False, na=False)]
    if results.empty:
        print("No books found.")
    else:
        print("Books found:\n", results)

def add_book(title, author, isbn, copies):
    """Adds a new book to the library."""
    df = load_books()
    isbn = str(isbn).strip()
    
    if isbn in df['ISBN'].values:
        print("Error: Book with this ISBN already exists.")
    else:
        new_book = pd.DataFrame([[title, author, isbn, copies, 0]], columns=df.columns)
        df = pd.concat([df, new_book], ignore_index=True)
        df.reset_index(drop=True, inplace=True)
        save_books(df)
        print("Book added successfully.")

def update_book(isbn, new_title=None, new_author=None, new_copies=None):
    """Updates book details."""
    df = load_books()
    isbn = str(isbn).strip()
    index = df[df['ISBN'] == isbn].index
    if not index.empty:
        if new_title:
            df.at[index[0], 'Title'] = new_title
        if new_author:
            df.at[index[0], 'Author'] = new_author
        if new_copies is not None:
            df.at[index[0], 'Copies'] = int(new_copies)
        save_books(df)
        print("Book updated successfully.")
    else:
        print("Book not found.")

def remove_book(isbn):
    """Removes a book from the library."""
    df = load_books()
    isbn = str(isbn).strip()
    initial_count = len(df)
    df = df[df['ISBN'] != isbn]
    if len(df) < initial_count:
        save_books(df)
        print("Book removed successfully.")
    else:
        print("Book not found.")

def issue_book(isbn, copies_to_issue):
    """Issues a book to a user."""
    df = load_books()
    isbn = str(isbn).strip()
    index = df[df['ISBN'] == isbn].index
    if not index.empty:
        available_copies = int(df.at[index[0], 'Copies'])
        if available_copies >= copies_to_issue:
            df.at[index[0], 'Copies'] -= copies_to_issue
            df.at[index[0], 'Issued_Copies'] += copies_to_issue  # Track issued copies
            save_books(df)
            print("Book issued successfully.")
        else:
            print("Not enough copies available.")
    else:
        print("Book not found.")

def return_book(isbn, copies_to_return):
    """Handles book returns."""
    df = load_books()
    isbn = str(isbn).strip()
    index = df[df['ISBN'] == isbn].index
    if not index.empty:
        issued_copies = int(df.at[index[0], 'Issued_Copies'])  
        if copies_to_return > issued_copies:
            print(f" You are trying to return {copies_to_return} copies, but only {issued_copies} were issued.")
        else:
            df.at[index[0], 'Copies'] += copies_to_return
            df.at[index[0], 'Issued_Copies'] -= copies_to_return
            save_books(df)
            print("Book returned successfully.")
    else:
        print("Book not found.")

# Main program loop
if __name__ == "__main__":
    while True:
        print("\nLibrary Management System")
        print("-------------------------")
        print("1 => View all Books")
        print("2 => Search for a Book")
        print("3 => Add a Book")
        print("4 => Update a Book")
        print("5 => Remove a Book")
        print("6 => Issue a Book")
        print("7 => Return a Book")
        print("8 => Exit")
        
        ch = input("Enter your choice: ")

        if ch == "1":
            view_books()
        elif ch == "2":
            key = input("Enter search keyword: ")
            search_books(key)
        elif ch == "3":
            title = input("Enter Title: ")
            author = input("Enter Author: ")
            isbn = input("Enter ISBN: ")
            copies = input("Enter No. of Copies: ")
            add_book(title, author, isbn, copies)
        elif ch == "4":
            isbn = input("Enter ISBN to update: ")
            new_title = input("New Title (leave blank to keep unchanged): ") or None
            new_author = input("New Author (leave blank to keep unchanged): ") or None
            new_copies = input("New Copies (leave blank to keep unchanged): ") or None
            update_book(isbn, new_title, new_author, new_copies)
        elif ch == "5":
            isbn = input("Enter ISBN to remove: ")
            remove_book(isbn)
        elif ch == "6":
            isbn = input("Enter ISBN to issue: ")
            copies_to_issue = int(input("Enter number of copies to issue: "))
            issue_book(isbn, copies_to_issue)
        elif ch == "7":
            isbn = input("Enter ISBN to return: ")
            copies_to_return = int(input("Enter number of copies to return: "))
            return_book(isbn, copies_to_return)
        elif ch == "8":
            print("Exiting Library Management System. Goodbye!")
            break
        else:
            print("Invalid choice. Try again.")
