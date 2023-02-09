from tkinter import Tk, Frame, Button, Menu, filedialog, Label, Text, messagebox
from tkinter.ttk import Progressbar
import requests
from bs4 import BeautifulSoup

requests.packages.urllib3.disable_warnings()
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 '
                  'Safari/537.36'}


# Class containing the functions related to the price comparing tool as well as GUI functions
class Controller:

    def __init__(self):
        self.grocery_list = []
        self.menu_bar = None
        self.window = Tk()
        self.bar = None
        self.frame = None
        self.text_box = None
        self.total_price = 0
        self.create_gui()
        self.window.mainloop()

    # Retrieves grocery items from textbox and processes them
    def submit_grocery_list(self):

        if self.grocery_list:
            messagebox.showerror(title="Error !!!", message="Please reset the program before submitting again")
            return

        self.grocery_list = self.text_box.get("1.0", "end").strip().split("\n")

        if self.grocery_list == ['']:
            return

        self.text_box.delete("1.0", "end")
        self.handle_grocery_list()
        self.show_data()

    # Selects a grocery list text file and processes it
    def open_file(self):

        self.reset()
        path = filedialog.askopenfilename(title="Open File okay?")

        self.extract_grocery_items(path)
        self.handle_grocery_list()
        self.show_data()

    # Extracts grocery items from a text file
    def extract_grocery_items(self, path):

        self.grocery_list = []

        file_holder = open(path)
        info = file_holder.readlines()
        file_holder.close()

        for item in info:
            self.grocery_list.append(item.strip())

    # Takes in a product and returns the cheapest item from the walmart website
    def walmart(self, product):

        try:
            product.replace(' ', '+')

            response = requests.get(f'https://www.walmart.com/search?q={product}', headers=headers, verify=False)

            soup = BeautifulSoup(response.text, 'html.parser')
            walmart_prices = self.extract_items(soup, ('div', 'mr1 mr2-xl b black lh-copy f5 f4-l', (67, -6)))
            walmart_names = self.extract_items(soup, ('span', 'normal dark-gray mb0 mt1 lh-title f6 f5-l', (91, -7)))

            items = self.combine_data(walmart_names, walmart_prices)
            cheapest_item = self.extract_minimum_items(items)

        except:
            return "Could not find " + product, "$0.00"

        return cheapest_item

    # Extracts the name and price data from the website
    def extract_items(self, soup, data):

        items = soup.find_all(data[0], class_=data[1])
        item_data = []

        for i in range(len(items)):
            if i > 5:
                break
            line = str(items[i])[data[2][0]:data[2][1]]
            item_data.append(line)

        return item_data

    # Merges the prices and data into an array of tuples
    def combine_data(self, names, prices):

        if len(names) >= len(prices):
            merged_list = [(names[i], prices[i]) for i in range(0, len(prices))]
        else:
            merged_list = [(names[i], prices[i]) for i in range(0, len(names))]

        return merged_list

    # Returns the cheapest item from the list of items
    def extract_minimum_items(self, items):

        lowest_price = '$' + str(min([float(x[1].strip('$')) for x in items]))

        for item in items:
            if item[1] == lowest_price:
                return item

    # Controls progress bar and processes the grocery list
    def handle_grocery_list(self):

        bar_increment = (100 / len(self.grocery_list))
        self.total_price = 0
        item_list = []
        for item in self.grocery_list:
            product = self.walmart(item)
            item_list.append(product)
            self.total_price += float(product[1].strip('$'))

            self.bar['value'] += bar_increment
            self.window.update_idletasks()
        self.grocery_list = item_list
        self.bar['value'] = 0
        self.window.update_idletasks()

    # Outputs the cheapest items as well as total price to the textbox
    def show_data(self):

        for item in self.grocery_list:
            self.text_box.insert("end", item[0] + "\t" + item[1] + "\n")

        self.text_box.insert("insert", "\nTotal Price : $" + str(format(self.total_price, ".2f")))
        self.text_box.configure(state="disabled")

# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%         GUI Functions         %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

    # This function calls all the necessary functions to construct the GUI
    def create_gui(self):

        self.window.title("Price Comparer Tool")
        self.menu_bar = self.create_dropdown_menu()
        self.window.config(menu=self.menu_bar)
        self.frame = Frame(self.window)
        self.frame.pack()
        Label(self.frame, bg="#0071ce", text="Walmart Grocery Shopping Tool", fg="#ffc220",
              height=1, relief='raised', width=30, font=("Rockwell", 25, "bold")).pack(side="top", expand=1, fill='x')
        self.text_box = Text(self.frame, height=15, width=90, font=("Rockwell", 15, "bold"))
        self.text_box.pack()
        self.text_box.bind("<Configure>", self.reset_tabstop)
        open_button = Button(text="Submit", command=self.submit_grocery_list)
        open_button.pack(side="left", padx=30)
        self.bar = Progressbar(self.window, orient="horizontal", length=800)
        self.bar.pack(pady=10, padx=10)

    # Creates the dropdown menu
    def create_dropdown_menu(self):

        menu_bar = Menu(self.window)
        file_menu = Menu(menu_bar, tearoff=0)

        file_menu.add_command(label="Open File", command=self.open_file)
        file_menu.add_command(label="Instructions", command=self.open_instructions)
        file_menu.add_command(label="Reset", command=self.reset)
        file_menu.add_command(label="Exit", command=self.window.destroy)
        menu_bar.add_cascade(label="File", menu=file_menu)

        return menu_bar

    # Opens the instruction menu
    @staticmethod
    def open_instructions():
        messagebox.showinfo(title="Instructions", message="Submit items either through a text file (File>Open File)"
                                                          "or by entering each item into the textbox on a new line and "
                                                          "pressing submit.\n\n"
                                                          "File>Reset can be used to reset the program and enter new "
                                                          "items.\n")

    # Function used to align text in text box
    def reset_tabstop(self, event):
        event.widget.configure(tabs=(event.width - 8, "right"))

    # Resets the program so a new list can be processed
    def reset(self):

        self.grocery_list = []
        self.text_box.configure(state="normal")
        self.text_box.delete("1.0", "end")
        self.total_price = 0
