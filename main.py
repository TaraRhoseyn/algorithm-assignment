import csv
import os
import tkinter as tk
from tkinter import ttk

book_data = []
isbn = 0
title = 1
author = 2
length = 3
date_of_publication = 4
asc = 'asc'
desc = 'desc'
books_sorted = False


def view_books(data):
    '''
    Utility function to print list of lists

    @param data: list to iterate over
    '''
    for row in data:
        print("\n")
        for i in row:
            print(i)


def read_data_from_csv(filename):
    '''
    Reads data from CSV file and outputs it to a list of lists
    
    @param filename: file path of CSV file
    @return data: list of lists containing book data from CSV file
    @raise Exception: raises an exception
    '''
    data = []
    try:
        with open(filename, 'r', newline='') as csvfile:
            csvreader = csv.reader(csvfile)
            for row in csvreader:
                data.append(row)
        return data
    except Exception as e:
        raise Exception(f"An error occurred while tyring to read the csv data: {e}")


def write_data_to_csv(data, attribute, order):
    '''
    Writes data from list to a CSV file

    @param data: list with data to be exported to a CSV file
    @param attribute: which book attribute (e.g. author/title/etc) will be in filename
    @param order: which order (asc/desc/) will be in filename
    @raise Exception: raises an exception
    '''
    output_file = set_filename(attribute, order)
    try:
        with open(output_file, mode='w', newline='') as file:
            writer = csv.writer(file)
            for row in data:
                writer.writerow(row)
        print("\nSUCCESS: New sorted data is available at: "+output_file+"\n")
    except Exception as e:
        print(f"An error occurred while tyring to write the csv data: {e}")


def get_attribute_name(attribute):
    '''
    Utility function to generate string value back from book attribute

    @param attribute: book attribute (e.g. author/title/etc)
    '''
    value = ''
    if attribute == 0: 
        value = 'isbn'
    elif attribute == 1:
        value = 'title'
    elif attribute == 2:
        value = 'author'
    elif attribute == 3:
        value = 'length'
    elif attribute == 4:
        value = 'date_of_publication'
    return value


def set_filename(attribute, order):
    '''
    Utility function to generate a filename based on book attribute and order

    @param attribute: which book attribute (e.g. author/title/etc) will be in filename
    @param order: which order (asc/desc/) will be in filename
    @return outputfile: str of filename that will be written to
    '''
    value = get_attribute_name(attribute)
    print(value)
    output_file = 'data/sorted_by_'+value+'_'+order+'_data.csv'
    return output_file


def sort_books(attribute, order):
    '''
    Iterative quicksort algorithm to sort books by attribute (e.g. author/title/etc)
    and order (asc/desc)

    @attribute: int value representing inner list index where specific attribute is found (e.g. author/title/etc)
    @order: str value of either asc/desc which will dictate what order the sort will go in
    @return book_data: list of lists containing sorted data 
    '''
    value = get_attribute_name(attribute)
    print("Sorting books by "+value+" in "+order+"ending order "+"...")
    if calc_length(book_data) <= 1:
        return book_data
    # Create a stack for storing subarray indices
    stack = [(0, calc_length(book_data) - 1)]  #
    while stack:
        low, high = stack.pop()
        if low < high:
            # selects pivot point from right-most element
            if attribute == 3: 
                pivot = int(book_data[high][attribute])
            else:
                pivot = book_data[high][attribute]
            # initalise pointer that's smaller than the pivot:
            i = low - 1
            for j in range(low, high):
                if attribute == 3: 
                    if (order == 'asc' and int(book_data[j][attribute]) <= pivot) or (order == 'desc' and int(book_data[j][attribute]) >= pivot):
                        i += 1
                        # swaps elements:
                        book_data[i], book_data[j] = book_data[j], book_data[i]
                else:
                    if (order == 'asc' and book_data[j][attribute] <= pivot) or (order == 'desc' and book_data[j][attribute] >= pivot):
                        i += 1
                        # swaps elements:
                        book_data[i], book_data[j] = book_data[j], book_data[i]
            book_data[i + 1], book_data[high] = book_data[high], book_data[i + 1]
            stack.append((low, i))
            stack.append((i + 2, high))
    if attribute == 3:
        for k in book_data:
            k[attribute] = str(k[attribute])
    write_data_to_csv(book_data, attribute, order)
    global books_sorted
    books_sorted = True
    return book_data


def check_sorted_books(attribute):
    '''
    '''
    order = ''
    value = get_attribute_name(attribute)
    attribute_found = False
    filename = ''
    sorted_files = os.listdir('data')
    for file in sorted_files:
        '''
        Returns data that's sorted by ascending order by default
        '''
        if (value in file) and ('asc' in file):
            attribute_found = True
            order = 'asc'
            filename = 'data/'+file
            break
    return attribute_found, order, filename
        

def search_for_book(search_term, attribute):
    '''
    Uses a binary search algorithm to go through
    data sorted by ascending order to turn a search result

    @param search_term: string value to test for equality
    @param attribute: book attribute that is searched for
    '''
    try:
        attribute_found, order, filename = check_sorted_books(attribute)
        if attribute_found:
            sorted_data = read_data_from_csv(filename)
        else:
            raise Exception("Sorted book data not found.")
        low = 0
        high = calc_length(sorted_data) - 1
        while low <= high:
            middle = (high + low) // 2
            # Compare the search element 'search term' with the element at the 'attribute' index
            # searches from ascending order by default
            if sorted_data[middle][attribute] < search_term:
                low = middle + 1
            elif sorted_data[middle][attribute] > search_term:
                high = middle - 1
            elif sorted_data[middle][attribute] == search_term:
                return sorted_data[middle], ""
        raise Exception(
            "Search term does not match any book data. Please check your ISBN.")
    except Exception as e:
        return None, str(e)


def sort_all_books():
    sort_books(isbn, asc)
    sort_books(isbn, desc)
    sort_books(title, asc)
    sort_books(title, desc)
    sort_books(author, asc)
    sort_books(author, desc)
    sort_books(length, asc)
    sort_books(length, desc)
    sort_books(date_of_publication, asc)
    sort_books(date_of_publication, desc)


def calc_length(book_data):
    '''
    Utility function to calculate length of list

    @param book_data: list of lists containing unsorted book data
    @return count: int of book_data length
    '''
    count = 0
    for i in book_data:
        count += 1
    return count


def add_book(book_data, new_book): 
    index = calc_length(book_data)
    return book_data[:index] + [new_book] + book_data[index:]
    

def delete_book(isbn, book_data):
    '''
    Deletes a book based on ISBN supplied
    It attempts to match the ISBN to one in 
    our unsorted book data. Once the match
    is found via a linear search, the index of 
    that match is used to delete the item
    using sequential replacing of elements

    @param isbn: value to search for a match
    @param book_data: list of lists containing unsorted book data
    @raise Exception: raises an exception that the ISBN supplied doesn't any found
    '''
    index_for_delete = -1  # init index
    for i in range(calc_length(book_data)):
        book = book_data[i]
        if book[0] == isbn: # searches for a match
            index_for_delete = i
            print(f"Found the book with ISBN {isbn} at index {i}")
            break  # exits once match is found
    if index_for_delete >= 0:
        '''
        The function now takes the list at the point
        of the index of the book that should be deleted
        and replaces each inner list with the inner list
        of the next index point
        '''
        for j in range(index_for_delete, calc_length(book_data) - 1):
            book_data[j] = book_data[j + 1]
        book_data.pop()  # remove last element (copy of previous element)
        print(f"Deleted the book with ISBN {isbn} at index {index_for_delete}.")
        sort_all_books()
    else:
        raise Exception(f"Book with ISBN {isbn} is not present, and therefore cannot be deleted.")


def launch_gui():
    global book_data
    book_data = read_data_from_csv('library_data.csv')

    def add_btn_clicked():
        global book_data
        isbn_val = isbn_input.get()
        title_val = title_input.get()
        author_val = author_input.get()
        length_val = length_input.get()
        date_val = date_input.get()
        new_book = [isbn_val, title_val, author_val, length_val, date_val]
        try:
            new_book_data = add_book(book_data, new_book)
            book_data = new_book_data
            sort_all_books()
            add_result.config(text="New book added. Books have been re-sorted.")
        except Exception as e:
            add_result.config(text="An error has occurred, please ensure all fields are correct")
            raise Exception(f"An error occurred while trying to add a new book: {e}")


    def sort_btn_clicked():
        sort_all_books()
        go_to_main_menu()


    def search_btn_clicked():
        '''
        can only search if books are already sorted
        '''
        search_term = search_input.get()
        if books_sorted:
            result, err_msg = search_for_book(search_term, isbn)
            if result is not None:
                isbn_val, title_val, author_val, length_val, date_val = result
                formatted_result = f"Title: {title_val}\nAuthor: {author_val}\nPage length: {length_val}\nDate published: {date_val}\nISBN: {isbn_val}"
                search_result.config(text=formatted_result)
                search_result_label.config(text="Search result:")
            else:
                search_result.config(text=err_msg)
        else:
            search_result_label.config(text="Sort books before searching.")


    def exit():
        window.destroy()


    def show_screen(frame):
        frame.pack()
        current_screen.append(frame)
    

    def hide_screen(frame):
        frame.pack_forget()
        current_screen.pop()

    
    def go_to_main_menu():
        hide_screen(starting_screen)
        show_screen(main_menu)


    def back_from_search():
        back_btn.place_forget()
        search_screen_label.grid_forget()
        search_input.grid_forget()
        search_submit.grid_forget()
        search_result_label.grid_forget()
        search_result.grid_forget()
        search_title.grid_forget()
        hide_screen(search_screen)
        show_screen(main_menu)


    def back_from_add():
        back_btn.place_forget()
        adding_title.grid_forget()
        isbn_label.grid_forget()
        isbn_input.grid_forget()
        title_label.grid_forget()
        title_input.grid_forget()
        author_label.grid_forget()
        author_input.grid_forget()
        length_label.grid_forget()
        length_input.grid_forget()
        date_label.grid_forget()
        date_input.grid_forget()
        add_submit.grid_forget()
        add_result.grid_forget()
        hide_screen(add_screen)
        show_screen(main_menu)


    def back_from_display():
        back_btn.place_forget()
        display_title.pack_forget()
        attribute_frame.pack_forget()
        order_frame.pack_forget()
        show_data_btn.pack_forget()
        scroll_x.pack_forget()
        text_widget.pack_forget()
        hide_screen(display_screen)
        show_screen(main_menu)


    def back_from_delete():
        back_btn.place_forget()
        delete_title.grid_forget()
        delete_label.grid_forget()
        delete_input.grid_forget()
        hide_screen(delete_screen)
        show_screen(main_menu)

    
    def delete_btn_clicked():
        global book_data
        isbn_for_deletion = delete_input.get()
        delete_book(isbn_for_deletion, book_data)
        delete_result.config(text="The book has been deleted. Books have been re-sorted.")


    def go_to_display():
        hide_screen(main_menu)
        show_screen(display_screen)
        search_btn.pack_forget()
        add_btn.pack_forget()
        remove_btn.pack_forget()
        global back_btn
        back_btn = ttk.Button(window, text="Back to main menu", style="Secondary.TButton", command=back_from_display)
        back_btn.place(x=10,y=10)
        global display_title
        display_title = ttk.Label(display_screen, text="Displaying sorted book data", font=title_font)
        display_title.pack(pady=50)
        global attribute_frame
        attribute_frame = ttk.Frame(display_screen)
        attribute_frame.pack(side='top', padx=5)
        global attribute_label
        attribute_label = ttk.Label(attribute_frame, text="Select attribute:")
        attribute_label.pack(side='left')
        global attribute_variable
        attribute_variable = tk.StringVar()
        attribute_variable.set("isbn")
        attributes = ["isbn", "title", "author", "length", "date_of_publication"]
        # attributes = [0, 1, 2, 3, 4]
        for attribute in attributes:
            ttk.Radiobutton(attribute_frame, text=attribute, variable=attribute_variable, value=attribute).pack(side='left', padx=5)
        global order_frame
        order_frame = ttk.Frame(display_screen)
        order_frame.pack(side='top', padx=5)
        global order_label 
        order_label = ttk.Label(order_frame, text="Select order:")
        order_label.pack(side='left')
        global order_variable
        order_variable = tk.StringVar()
        order_variable.set("asc")
        global orders
        orders = ["asc", "desc"]
        for order in orders:
            ttk.Radiobutton(order_frame, text=order, variable=order_variable, value=order).pack(side='left', padx=5, pady=5)


        def show_data():
            selected_attribute = attribute_variable.get()
            selected_order = order_variable.get()
            filename = 'data/sorted_by_'+selected_attribute+'_'+selected_order+'_data.csv'
            data = read_data_from_csv(filename)
            text_widget.delete("1.0", tk.END)
            for row in data:
                text_widget.insert(tk.END, ", ".join(row) + "\n")
            show_data_btn.pack(pady=50)
            scroll_x.pack(side=tk.BOTTOM, fill=tk.X, ipadx=10, ipady=10)
            text_widget.pack(fill="both", expand=True)
            
        
        global show_data_btn
        show_data_btn = ttk.Button(display_screen, text="Show sorted data", command=show_data)
        show_data_btn.pack(pady=50)
        global scroll_x
        scroll_x = tk.Scrollbar(display_screen, orient=tk.HORIZONTAL)
        # scroll_x.pack(side=tk.BOTTOM, fill=tk.X, ipadx=10, ipady=10)
        global text_widget
        text_widget = tk.Text(display_screen, wrap=tk.NONE, xscrollcommand=scroll_x.set)
        # text_widget.pack(fill="both", expand=True)
        scroll_x.config(command=text_widget.xview)


        def show_data():
            selected_attribute = attribute_variable.get()
            selected_order = order_variable.get()
            filename = 'data/sorted_by_'+selected_attribute+'_'+selected_order+'_data.csv'
            data = read_data_from_csv(filename)
            text_widget.delete("1.0", tk.END)
            for row in data:
                text_widget.insert(tk.END, ", ".join(row) + "\n")


    def go_to_delete():
        hide_screen(main_menu)
        show_screen(delete_screen)
        search_btn.pack_forget()
        add_btn.pack_forget()
        remove_btn.pack_forget()
        global back_btn
        back_btn = ttk.Button(window, text="Back to main menu", style="Secondary.TButton", command=back_from_delete)
        back_btn.place(x=10,y=10)
        global delete_title
        delete_title = ttk.Label(delete_screen, text="Remove a book", font=title_font)
        delete_title.grid(row=0, columnspan=5, pady=50)
        global delete_label
        delete_label = ttk.Label(delete_screen, text="Delete a book by supplying it's ISBN:")
        delete_label.grid(row=1, columnspan=5, pady=(5, 5))
        global delete_input
        delete_input = ttk.Entry(delete_screen)
        delete_input.grid(row=2, columnspan=5, pady=(5, 5))
        global delete_submit
        delete_submit = ttk.Button(delete_screen, text="Submit", command=delete_btn_clicked)
        delete_submit.grid(row=3, columnspan=5, pady=50)
        global delete_result
        delete_result = ttk.Label(delete_screen, text="")
        delete_result.grid(row=5, columnspan=5, pady=(5, 5))


    def go_to_add():
        hide_screen(main_menu)
        show_screen(add_screen)
        search_btn.pack_forget()
        add_btn.pack_forget()
        remove_btn.pack_forget()
        global back_btn
        back_btn = ttk.Button(window, text="Back to main menu", style="Secondary.TButton", command=back_from_add)
        back_btn.place(x=10,y=10)
        global adding_title
        adding_title = ttk.Label(add_screen, text="Add a book", font=title_font)
        adding_title.grid(row=0, columnspan=5, pady=50)
        global isbn_label
        isbn_label = ttk.Label(add_screen, text="Add ISBN:")
        isbn_label.grid(row=1, column=1)
        global isbn_input
        isbn_input = ttk.Entry(add_screen)
        isbn_input.grid(row=1, column=2)
        global title_label
        title_label = ttk.Label(add_screen, text="Add book title:")
        title_label.grid(row=2, column=1)
        global title_input
        title_input = ttk.Entry(add_screen)
        title_input.grid(row=2, column=2)
        global author_label
        author_label = ttk.Label(add_screen, text="Add book author:")
        author_label.grid(row=3, column=1)
        global author_input
        author_input = ttk.Entry(add_screen)
        author_input.grid(row=3, column=2)
        global length_label
        length_label = ttk.Label(add_screen, text="Add page length:")
        length_label.grid(row=4, column=1)
        global length_input
        length_input = ttk.Entry(add_screen)
        length_input.grid(row=4, column=2)
        global date_label
        date_label = ttk.Label(add_screen, text="Add publication date (YYYY-MM-DD):")
        date_label.grid(row=5, column=1)
        global date_input
        date_input = ttk.Entry(add_screen)
        date_input.grid(row=5, column=2)
        global add_submit
        add_submit = ttk.Button(add_screen, text="Submit", command=add_btn_clicked)
        add_submit.grid(row=6, columnspan=5, pady=50)
        global add_result
        add_result = ttk.Label(add_screen, text="")
        add_result.grid(row=7, columnspan=5, pady=(5, 5))
 

    def go_to_search():
        hide_screen(main_menu)
        show_screen(search_screen)
        search_btn.pack_forget()
        add_btn.pack_forget()
        remove_btn.pack_forget()
        global back_btn
        back_btn = ttk.Button(window, text="Back to main menu", style="Secondary.TButton", command=back_from_search)
        back_btn.place(x=10,y=10)
        global search_title
        search_title = ttk.Label(search_screen, text="Search for a book", font=title_font)
        search_title.grid(row=0, columnspan=5, pady=50)
        global search_screen_label
        search_screen_label = ttk.Label(search_screen, text="Search for a book with ISBN:")
        search_screen_label.grid(row=1, columnspan=5, pady=(5, 5))
        global search_input
        search_input = ttk.Entry(search_screen)
        search_input.grid(row=2, columnspan=5, pady=(5, 5))
        global search_submit
        search_submit = ttk.Button(search_screen, text="Submit", command=search_btn_clicked)
        search_submit.grid(row=3, columnspan=5, pady=50)
        global search_result_label
        search_result_label = ttk.Label(search_screen, text="")
        search_result_label.grid(row=4, columnspan=5, pady=(5, 5))
        global search_result
        search_result = ttk.Label(search_screen, text="")
        search_result.grid(row=5, columnspan=5, pady=(5, 5))
        

    # inits:
    window = tk.Tk()
    window.attributes("-fullscreen", True)
    window.configure(bg='lightgray')
    window.title("Library Data Application")
    current_screen = []
    starting_screen = tk.Frame(window, background="lightgray")
    main_menu = tk.Frame(window, background="lightgray")
    search_screen = tk.Frame(window, background="lightgray")
    add_screen = tk.Frame(window, background="lightgray")
    delete_screen = tk.Frame(window, background="lightgray") 
    display_screen = tk.Frame(window, background="lightgray")
    # shows starting screen as default:
    show_screen(starting_screen)
    # styling:
    primary_btn_col= '#FB40AF'
    style = ttk.Style()
    style.theme_use("alt")
    style.configure("TLabel", foreground="black", background="lightgray", font=("Helvetica", 16))
    style.configure("TRadiobutton", background="lightgray", font=("Helvetica", 16))
    style.configure("TButton", foreground="black", background=primary_btn_col, font=("Helvetica", 16))
    style.configure("Secondary.TButton", foreground="black", background='darkgray', font=("Helvetica", 16))
    style.configure("TEntry", foreground="black", height=10, width=40)
    # exits:
    exit_btn = ttk.Button(window, text="Exit application", style="Secondary.TButton", command=exit)
    exit_btn.place(x=window.winfo_screenwidth() - exit_btn.winfo_reqwidth() - 10, y=10)
    # title:
    title_font = ("Helvetica", 30)
    small_font = ("Helvetica", 9)
    title = ttk.Label(starting_screen, text="Library Data Application", font=title_font)
    title.grid(row=0, columnspan=5, pady=50)
    menu_title = ttk.Label(main_menu, text="Library Data Application", font=title_font)
    menu_title.grid(row=0, columnspan=5, pady=50)
    # sorts:
    menu_explainer = ttk.Label(starting_screen, text="Begin by sorting books. This will sort books by all attributes (title, author, page length, date of publication, and ISBN) and by both ascending and descending order.", wraplength=700, justify='center')
    menu_explainer.grid(row=1, columnspan=5, pady=(10, 10))
    sort_btn = ttk.Button(starting_screen, text="Sort all books", command=sort_btn_clicked)
    sort_btn.grid(row=2, columnspan=5, padx=10, pady=10)
    # MAIN MENU
    menu_explainer = ttk.Label(main_menu, text="Books have been sorted. You can now do the following:")
    menu_explainer.grid(row=1, columnspan=5, pady=(10, 3))
    # trigger display:
    display_btn = ttk.Button(main_menu, text="Display sorted books", command=go_to_display)
    display_btn.grid(row=2, column=1, padx=10, pady=20)
    # trigger search:
    search_btn = ttk.Button(main_menu, text="Search for a book", command=go_to_search)
    search_btn.grid(row=2, column=2, padx=10, pady=20)
    # trigger add a book:
    add_btn = ttk.Button(main_menu, text="Add a book", command=go_to_add)
    add_btn.grid(row=2, column=3, padx=10, pady=20)
    # trigger remove a book:
    remove_btn = ttk.Button(main_menu, text="Remove a book", command=go_to_delete)
    remove_btn.grid(row=2, column=4, padx=10, pady=20)
    window.mainloop()


if __name__ == "__main__":
    launch_gui()