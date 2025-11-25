import tkinter as tk
from tkinter import ttk, messagebox
from tkinter.ttk import *
from tkinter import PhotoImage
import requests
from PIL import Image, ImageTk
from io import BytesIO
import os
 

LARGEFONT =("Verdana", 18)
SMALLFONT = ("Veranda", 10)
API_BASE_URL = "http://localhost:5000"
 
class tkinterApp(tk.Tk):
    
    # __init__ function for class tkinterApp 
    def __init__(self, *args, **kwargs): 
        
        # __init__ function for class Tk
        tk.Tk.__init__(self, *args, **kwargs)

        self.title("McDougals App")
        self.geometry("600x700")
        
        # Store user session data
        self.user_id = None
        self.username = None
        self.cart = []  # List to store cart items
        self.menu_items = []  # Store menu items from API
        self.selected_restaurant_id = 1  # Default restaurant
        
        # creating a container
        container = tk.Frame(self)  
        container.pack(side = "top", fill = "both", expand = True) 
 
        container.grid_rowconfigure(0, weight = 1)
        container.grid_columnconfigure(0, weight = 1)
 
        # initializing frames to an empty array
        self.frames = {}  
 
        # iterating through a tuple consisting
        # of the different page layouts
        for F in (StartPage, LoginPage, RegisterPage, MenuPage, AdminMenuPage, AddPage, EditPage, CartPage, RestaurantSelectionPage, PaymentPage, ThankYou):
 
            frame = F(container, self)
 
            # initializing frame of that object from
            # startpage, LoginPage, RegisterPage respectively with 
            # for loop
            self.frames[F] = frame 
 
            frame.grid(row = 0, column = 0, sticky ="nsew")
 
        self.show_frame(StartPage)
 
    # to display the current frame passed as
    # parameter
    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()
 
# first window frame startpage
 
class StartPage(tk.Frame):
    def __init__(self, parent, controller): 
        tk.Frame.__init__(self, parent)
        
        # label of frame Layout 2
        label = ttk.Label(self, text ="Welcome to McDougals", font = LARGEFONT)
        
        # putting the grid in its place by using
        # grid
        label.grid(row = 0, column = 1, padx = 10, pady = 10) 
 
        loginButton = ttk.Button(self, text ="Login",
        command = lambda : controller.show_frame(LoginPage))
    
        # putting the button in its place by
        # using grid
        loginButton.grid(row = 4, column = 1, padx = 10, pady = 10)
 
        ## button to show frame 2 with text layout2
        registerButton = ttk.Button(self, text ="Register",
        command = lambda : controller.show_frame(RegisterPage))
    
        # putting the button in its place by
        # using grid
        registerButton.grid(row = 5, column = 1, padx = 10, pady = 10)
 
         
 
 
# second window frame page1 
class LoginPage(tk.Frame):
    
    def __init__(self, parent, controller):
        
        tk.Frame.__init__(self, parent)
        label = ttk.Label(self, text ="Please Login", font = LARGEFONT)
        label.grid(row = 0, column = 2, padx = 10, pady = 10)
 
        username_label = ttk.Label(self, text="Username:", font=SMALLFONT)
        username_label.grid(row=1, column=1, padx=10, pady=5, sticky="e")
        
        #username field
        username = Entry(self, width= 20)
        username.grid(row= 1 , column=2, padx=10, pady=5)

        password_label = ttk.Label(self, text="Password:", font=SMALLFONT)
        password_label.grid(row=2, column=1, padx=10, pady=5, sticky="e")
        
        #password field
        password = Entry(self, width=20, show="*")
        password.grid(row=2, column=2, padx=10, pady=5)

        result_label = ttk.Label(self, text="", font=SMALLFONT)
        result_label.grid(row=4, column=2, padx=10, pady=5)

        def login_user():
            user_input = username.get() 
            password_input = password.get()

            if not user_input or not password_input:
                messagebox.showerror("Error", "Please enter both username and password")
                return

            api_url = f"{API_BASE_URL}/login"
            payload = {"username": user_input, "password": password_input}

            try:
                response = requests.post(api_url, json=payload)
                response.raise_for_status()

                api_response_data = response.json()
                
                # Store user session data
                controller.user_id = api_response_data.get('userId')
                controller.username = user_input
                
                messagebox.showinfo("Success", f"Welcome back, {user_input}!")
                username.delete(0, tk.END)
                password.delete(0, tk.END)
                result_label.config(text="")
                
                # Load menu and navigate
                controller.frames[MenuPage].load_menu()
                controller.show_frame(MenuPage)

            except requests.exceptions.RequestException as e:
                messagebox.showerror("Login Failed", "Invalid username or password")
                result_label.config(text="Login failed", foreground="red")
 
        # button to show frame 3 with text
        # layout2
        enterButton = ttk.Button(self, text ="Login",
                            command = login_user)
        
        
    
        # putting the button in its place by 
        # using grid
        enterButton.grid(row = 3, column = 2, padx = 10, pady = 10)
        
        backButton = ttk.Button(self, text="Back", command=lambda: controller.show_frame(StartPage))
        backButton.grid(row=5, column=2, padx=10, pady=5)
 
 
 
 
# third window frame registerPage
class RegisterPage(tk.Frame): 
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = ttk.Label(self, text ="Please Register", font = LARGEFONT)
        label.grid(row = 0, column = 2, padx = 10, pady = 10)
 
        username_label = ttk.Label(self, text="Username:", font=SMALLFONT)
        username_label.grid(row=1, column=1, padx=10, pady=5, sticky="e")
        
        #username field
        username = Entry(self, width= 20)
        username.grid(row= 1 , column=2, padx=10, pady=5)

        email_label = ttk.Label(self, text="Email:", font=SMALLFONT)
        email_label.grid(row=2, column=1, padx=10, pady=5, sticky="e")
        
        #email field
        email = Entry(self, width=20)
        email.grid(row=2, column=2, padx=10, pady=5)

        password_label = ttk.Label(self, text="Password:", font=SMALLFONT)
        password_label.grid(row=3, column=1, padx=10, pady=5, sticky="e")
        
        #password field
        password = Entry(self, width=20, show="*")
        password.grid(row=3, column=2, padx=10, pady=5)

        def register_user():
            user_input = username.get()
            email_input = email.get()
            password_input = password.get()

            if not user_input or not email_input or not password_input:
                messagebox.showerror("Error", "Please fill in all fields")
                return

            api_url = f"{API_BASE_URL}/register"
            payload = {"username": user_input, "email": email_input, "password": password_input}

            try:
                response = requests.post(api_url, json=payload)
                response.raise_for_status()

                api_response_data = response.json()
                
                messagebox.showinfo("Success", f"Account created successfully! Please login.")
                username.delete(0, tk.END)
                email.delete(0, tk.END)
                password.delete(0, tk.END)
                controller.show_frame(LoginPage)

            except requests.exceptions.RequestException as e:
                messagebox.showerror("Registration Failed", "Username or email already exists")
 
        # button to show frame 3 with text
        # layout2
        enterButton = ttk.Button(self, text ="Register",
                            command = register_user)
    
        # putting the button in its place by 
        # using grid
        enterButton.grid(row = 4, column = 2, padx = 10, pady = 10)
        
        backButton = ttk.Button(self, text="Back", command=lambda: controller.show_frame(StartPage))
        backButton.grid(row=5, column=2, padx=10, pady=5)

class MenuPage(tk.Frame): 
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        
        label = ttk.Label(self, text ="Menu Items", font = LARGEFONT)
        label.grid(row = 0, column = 2, padx = 10, pady = 10)

        cartButton = ttk.Button(self, text="Cart", command = lambda : self.go_to_cart())
        cartButton.grid(row = 0, column= 4, padx=10, pady=10)
        
        logoutButton = ttk.Button(self, text="Logout", command=lambda: controller.show_frame(StartPage))
        logoutButton.grid(row=0, column=0, padx=10, pady=10)

        def go_to_admin():
            # Check if user is admin (userId 2)
            if controller.user_id == 2:
                controller.frames[AdminMenuPage].load_menu()
                controller.show_frame(AdminMenuPage)
            else:
                messagebox.showerror("Access Denied", "You must be logged in as an admin to access this page.")

        # Only show admin button if user is admin
        self.adminButton = ttk.Button(self, text="Admin", command=go_to_admin)
        if controller.user_id == 2:
            self.adminButton.grid(row=0, column=1, padx=10, pady=10)
    
        canvas = tk.Canvas(self, borderwidth=0)
        scrollbar = tk.Scrollbar(self, orient="vertical", command=canvas.yview)
        self.menu_frame = tk.Frame(canvas)
        
        self.menu_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=self.menu_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.grid(row=1, column=0, columnspan=5, sticky="nsew", padx=10, pady=10)
        scrollbar.grid(row=1, column=5, sticky="ns")
        
       
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)

    def load_menu(self):
        # Clear existing menu items
        for widget in self.menu_frame.winfo_children():
            widget.destroy()

        api_url = f"{API_BASE_URL}/menu"
        
        try:
            response = requests.get(api_url)
            response.raise_for_status()
            menu_items = response.json()
            self.controller.menu_items = menu_items
            
            print(f"Loaded {len(menu_items)} menu items from API")
            for item in menu_items:
                print(f"  - {item.get('name')} (Category: {item.get('category')})")
            
            # Group items by category
            categories = {}
            for item in menu_items:
                category = item.get('category', 'other')
                if category not in categories:
                    categories[category] = []
                categories[category].append(item)
            
            print(f"\nGrouped into {len(categories)} categories: {list(categories.keys())}")
            
            # Display items by category
            row_counter = 0
            for category, items in categories.items():
                # Category label
                cat_label = ttk.Label(self.menu_frame, text=category.capitalize(), font=SMALLFONT)
                cat_label.grid(row=row_counter, column=0, columnspan=2, padx=10, pady=5, sticky="w")
                row_counter += 1
                
                # Items in this category
                col = 0
                for item in items:
                    item_frame = tk.Frame(self.menu_frame, relief=tk.RIDGE, borderwidth=1)
                    item_frame.grid(row=row_counter, column=col, padx=5, pady=5, sticky="nsew")
                    
                    # Load and display image
                    image_url = item.get('image_url')
                    if image_url:
                        try:
                            # for handling images in our application from our database
                            if image_url.startswith('http://') or image_url.startswith('https://'):
                                # Download image from URL
                                img_response = requests.get(image_url, timeout=5)
                                img_response.raise_for_status()
                                img_data = Image.open(BytesIO(img_response.content))
                            else:
                                # Handle local file path
                                # Get the directory of the current script
                                script_dir = os.path.dirname(os.path.abspath(__file__))
                                
                                # Try different path combinations
                                possible_paths = [
                                    image_url,  # Absolute path
                                    os.path.join(script_dir, image_url),  
                                    os.path.join(script_dir, 'Assets', image_url),  # In Assets folder (all of ours are curretnly in there, but this offers use for when admins add)
                                    os.path.join(script_dir, 'Assets', os.path.basename(image_url))  
                                ]
                                
                                img_data = None
                                for path in possible_paths:
                                    if os.path.exists(path):
                                        img_data = Image.open(path)
                                        break
                                
                                if img_data is None:
                                    raise FileNotFoundError(f"Image not found: {image_url}")
                            
                            # resize the images to be uniform, some of them will end up stretched rip
                            img_data = img_data.resize((100, 100), Image.Resampling.LANCZOS)
                            photo = ImageTk.PhotoImage(img_data)
                            
                            # Display image
                            img_label = tk.Label(item_frame, image=photo)
                            img_label.image = photo  
                            img_label.pack(padx=5, pady=5)
                        except Exception as e:
                            # if our images fair to load show (no image)
                            placeholder = ttk.Label(item_frame, text="[No Image]", foreground="gray")
                            placeholder.pack(padx=5, pady=5)
                            print(f"Error loading image for {item['name']}: {e}")
                    
                    name_label = ttk.Label(item_frame, text=item['name'], font=("Verdana", 9, "bold"))
                    name_label.pack(padx=5, pady=2)
                    
                    price_label = ttk.Label(item_frame, text=f"${item['price']:.2f}")
                    price_label.pack(padx=5, pady=2)
                    
                    add_btn = ttk.Button(item_frame, text="Add to Cart", 
                                        command=lambda i=item: self.add_to_cart(i))
                    add_btn.pack(padx=5, pady=5)
                    
                    col += 1
                    if col > 1:  # 2 items per row for an kiosk feel likethey have at the mcdonalds 
                        col = 0
                        row_counter += 1
                
                if col != 0:  # Move to next row if we didn't complete the row
                    row_counter += 1
                    
        except requests.exceptions.RequestException as e:
            messagebox.showerror("Error", f"Failed to load menu: {e}")

    def add_to_cart(self, item):
        # Add item to cart with quantity 1
        existing_item = None
        for cart_item in self.controller.cart:
            if cart_item['item_id'] == item['item_id']:
                existing_item = cart_item
                break
        
        if existing_item:
            existing_item['quantity'] += 1
        else:
            self.controller.cart.append({
                'item_id': item['item_id'],
                'name': item['name'],
                'price': item['price'],
                'quantity': 1
            })
        
        messagebox.showinfo("Success", f"{item['name']} added to cart!")
    
    def go_to_cart(self):
        self.controller.frames[CartPage].load_cart()
        self.controller.show_frame(CartPage)

class AdminMenuPage(tk.Frame): 
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        
        label = ttk.Label(self, text ="Admin Menu Management", font = LARGEFONT)
        label.grid(row = 0, column = 2, padx = 10, pady = 10)
        
        backButton = ttk.Button(self, text="Back to Menu", command=lambda: controller.show_frame(MenuPage))
        backButton.grid(row=0, column=0, padx=10, pady=10)
        
        logoutButton = ttk.Button(self, text="Logout", command=lambda: controller.show_frame(StartPage))
        logoutButton.grid(row=0, column=1, padx=10, pady=10)

        add_btn = ttk.Button(self, text="Add", command=lambda: controller.show_frame(AddPage))
        add_btn.grid(row=0, column=3, padx=10, pady=10)
    
        canvas = tk.Canvas(self, borderwidth=0)
        scrollbar = tk.Scrollbar(self, orient="vertical", command=canvas.yview)
        self.menu_frame = tk.Frame(canvas)
        
        self.menu_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=self.menu_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.grid(row=1, column=0, columnspan=5, sticky="nsew", padx=10, pady=10)
        scrollbar.grid(row=1, column=5, sticky="ns")
        
       
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)

    def load_menu(self):
        # Clear existing menu items
        for widget in self.menu_frame.winfo_children():
            widget.destroy()

        api_url = f"{API_BASE_URL}/menu"
        
        try:
            response = requests.get(api_url)
            response.raise_for_status()
            menu_items = response.json()
            self.controller.menu_items = menu_items
            
            print(f"Loaded {len(menu_items)} menu items from API")
            for item in menu_items:
                print(f"  - {item.get('name')} (Category: {item.get('category')})")
            
            # Group items by category
            categories = {}
            for item in menu_items:
                category = item.get('category', 'other')
                if category not in categories:
                    categories[category] = []
                categories[category].append(item)
            
            print(f"\nGrouped into {len(categories)} categories: {list(categories.keys())}")
            
            # Display items by category
            row_counter = 0
            for category, items in categories.items():
                # Category label
                cat_label = ttk.Label(self.menu_frame, text=category.capitalize(), font=SMALLFONT)
                cat_label.grid(row=row_counter, column=0, columnspan=2, padx=10, pady=5, sticky="w")
                row_counter += 1
                
                # Items in this category
                col = 0
                for item in items:
                    item_frame = tk.Frame(self.menu_frame, relief=tk.RIDGE, borderwidth=1)
                    item_frame.grid(row=row_counter, column=col, padx=5, pady=5, sticky="nsew")
                    
                    # Load and display image
                    image_url = item.get('image_url')
                    if image_url:
                        try:
                            # for handling images in our application from our database
                            if image_url.startswith('http://') or image_url.startswith('https://'):
                                # Download image from URL
                                img_response = requests.get(image_url, timeout=5)
                                img_response.raise_for_status()
                                img_data = Image.open(BytesIO(img_response.content))
                            else:
                                # Handle local file path
                                # Get the directory of the current script
                                script_dir = os.path.dirname(os.path.abspath(__file__))
                                
                                # Try different path combinations
                                possible_paths = [
                                    image_url,  # Absolute path
                                    os.path.join(script_dir, image_url),  
                                    os.path.join(script_dir, 'Assets', image_url),  # In Assets folder (all of ours are curretnly in there, but this offers use for when admins add)
                                    os.path.join(script_dir, 'Assets', os.path.basename(image_url))  
                                ]
                                
                                img_data = None
                                for path in possible_paths:
                                    if os.path.exists(path):
                                        img_data = Image.open(path)
                                        break
                                
                                if img_data is None:
                                    raise FileNotFoundError(f"Image not found: {image_url}")
                            
                            # resize the images to be uniform, some of them will end up stretched rip
                            img_data = img_data.resize((100, 100), Image.Resampling.LANCZOS)
                            photo = ImageTk.PhotoImage(img_data)
                            
                            # Display image
                            img_label = tk.Label(item_frame, image=photo)
                            img_label.image = photo  
                            img_label.pack(padx=5, pady=5)
                        except Exception as e:
                            # if our images fair to load show (no image)
                            placeholder = ttk.Label(item_frame, text="[No Image]", foreground="gray")
                            placeholder.pack(padx=5, pady=5)
                            print(f"Error loading image for {item['name']}: {e}")
                    
                    name_label = ttk.Label(item_frame, text=item['name'], font=("Verdana", 9, "bold"))
                    name_label.pack(padx=5, pady=2)
                    
                    price_label = ttk.Label(item_frame, text=f"${item['price']:.2f}")
                    price_label.pack(padx=5, pady=2)

                    edit_btn = ttk.Button(item_frame, text="Edit", 
                                         command=lambda i=item: self.edit_item(i))
                    edit_btn.pack(padx=5, pady=5)

                    delete_btn = ttk.Button(item_frame, text="Delete",
                                           command=lambda i=item: self.delete_item(i))
                    delete_btn.pack(padx=5, pady=5)
                    
                    col += 1
                    if col > 1:  # 2 items per row for an kiosk feel likethey have at the mcdonalds 
                        col = 0
                        row_counter += 1
                
                if col != 0:  # Move to next row if we didn't complete the row
                    row_counter += 1
                    
        except requests.exceptions.RequestException as e:
            messagebox.showerror("Error", f"Failed to load menu: {e}")
    
    def edit_item(self, item):
        edit_page = self.controller.frames[EditPage]
        edit_page.load_item(item)
        self.controller.show_frame(EditPage)
    
    def delete_item(self, item):
        result = messagebox.askyesno("Confirm Delete", 
                                     f"Are you sure you want to delete {item['name']}?")
        if not result:
            return
        
        try:
            api_url = f"{API_BASE_URL}/admin/menu-items/{item['item_id']}"
            params = {'userId': self.controller.user_id}
            response = requests.delete(api_url, params=params)
            response.raise_for_status()
            
            messagebox.showinfo("Success", f"{item['name']} deleted successfully!")
            self.load_menu()
            
        except requests.exceptions.RequestException as e:
            messagebox.showerror("Error", "Failed to delete menu item")

class AddPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = ttk.Label(self, text ="Add Item", font = LARGEFONT)
        label.grid(row = 0, column = 2, padx = 10, pady = 10)

        nameLabel = ttk.Label(self, text = "Item Name: ", font = SMALLFONT)
        nameLabel.grid(row=1, column = 1, padx = 0, pady = 10)

        nameEntry = Entry(self, width=20)
        nameEntry.grid(row=1, column=2, padx=0, pady=10)

        priceLabel = ttk.Label(self, text = "Item Price: ", font = SMALLFONT)
        priceLabel.grid(row=2, column = 1, padx = 0, pady = 10)

        priceEntry = Entry(self, width=20)
        priceEntry.grid(row=2, column=2, padx=0, pady=10)

        categoryLabel = ttk.Label(self, text = "Category: ", font = SMALLFONT)
        categoryLabel.grid(row=3, column = 1, padx = 0, pady = 10)

        categoryEntry = Entry(self, width=20)
        categoryEntry.grid(row=3, column=2, padx=0, pady=10)

        imageLabel = ttk.Label(self, text = "Item Image: ", font = SMALLFONT)
        imageLabel.grid(row=4, column = 1, padx = 0, pady = 10)

        imageEntry = Entry(self, width=20)
        imageEntry.grid(row=4, column=2, padx=0, pady=10)
        
        descLabel = ttk.Label(self, text = "Description: ", font = SMALLFONT)
        descLabel.grid(row=5, column = 1, padx = 0, pady = 10)

        descEntry = Entry(self, width=20)
        descEntry.grid(row=5, column=2, padx=0, pady=10)

        def add_item():
            name = nameEntry.get()
            price = priceEntry.get()
            category = categoryEntry.get()
            image_url = imageEntry.get()
            description = descEntry.get()
            
            if not name or not price or not category:
                messagebox.showerror("Error", "Please fill in name, price, and category")
                return
            
            try:
                price_float = float(price)
            except ValueError:
                messagebox.showerror("Error", "Price must be a number")
                return
            
            payload = {
                'userId': controller.user_id,
                'name': name,
                'description': description,
                'price': price_float,
                'category': category,
                'image_url': image_url
            }
            
            try:
                api_url = f"{API_BASE_URL}/admin/menu-items"
                response = requests.post(api_url, json=payload)
                response.raise_for_status()
                
                messagebox.showinfo("Success", "Menu item added successfully!")
                nameEntry.delete(0, tk.END)
                priceEntry.delete(0, tk.END)
                categoryEntry.delete(0, tk.END)
                imageEntry.delete(0, tk.END)
                descEntry.delete(0, tk.END)
                
                controller.frames[AdminMenuPage].load_menu()
                controller.show_frame(AdminMenuPage)
                
            except requests.exceptions.RequestException as e:
                messagebox.showerror("Error", "Failed to add menu item")

        enterBtn = ttk.Button(self, text="Add Item", command=add_item)
        enterBtn.grid(row=6, column = 2, padx=0, pady = 10)
        
        backBtn = ttk.Button(self, text="Back", command=lambda: controller.show_frame(AdminMenuPage))
        backBtn.grid(row=7, column = 2, padx=0, pady = 10)

class EditPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.current_item = None
        
        label = ttk.Label(self, text ="Edit Item", font = LARGEFONT)
        label.grid(row = 0, column = 2, padx = 10, pady = 10)

        nameLabel = ttk.Label(self, text = "Item Name: ", font = SMALLFONT)
        nameLabel.grid(row=1, column = 1, padx = 0, pady = 10)

        self.nameEntry = Entry(self, width=20)
        self.nameEntry.grid(row=1, column=2, padx=0, pady=10)

        priceLabel = ttk.Label(self, text = "Item Price: ", font = SMALLFONT)
        priceLabel.grid(row=2, column = 1, padx = 0, pady = 10)

        self.priceEntry = Entry(self, width=20)
        self.priceEntry.grid(row=2, column=2, padx=0, pady=10)

        categoryLabel = ttk.Label(self, text = "Category: ", font = SMALLFONT)
        categoryLabel.grid(row=3, column = 1, padx = 0, pady = 10)

        self.categoryEntry = Entry(self, width=20)
        self.categoryEntry.grid(row=3, column=2, padx=0, pady=10)

        imageLabel = ttk.Label(self, text = "Item Image: ", font = SMALLFONT)
        imageLabel.grid(row=4, column = 1, padx = 0, pady = 10)

        self.imageEntry = Entry(self, width=20)
        self.imageEntry.grid(row=4, column=2, padx=0, pady=10)
        
        descLabel = ttk.Label(self, text = "Description: ", font = SMALLFONT)
        descLabel.grid(row=5, column = 1, padx = 0, pady = 10)

        self.descEntry = Entry(self, width=20)
        self.descEntry.grid(row=5, column=2, padx=0, pady=10)

        enterBtn = ttk.Button(self, text="Update Item", command=self.update_item)
        enterBtn.grid(row=6, column = 2, padx=0, pady = 10)
        
        backBtn = ttk.Button(self, text="Back", command=lambda: controller.show_frame(AdminMenuPage))
        backBtn.grid(row=7, column = 2, padx=0, pady = 10)
    
    def load_item(self, item):
        self.current_item = item
        self.nameEntry.delete(0, tk.END)
        self.nameEntry.insert(0, item.get('name', ''))
        self.priceEntry.delete(0, tk.END)
        self.priceEntry.insert(0, str(item.get('price', '')))
        self.categoryEntry.delete(0, tk.END)
        self.categoryEntry.insert(0, item.get('category', ''))
        self.imageEntry.delete(0, tk.END)
        self.imageEntry.insert(0, item.get('image_url', ''))
        self.descEntry.delete(0, tk.END)
        self.descEntry.insert(0, item.get('description', ''))
    
    def update_item(self):
        if not self.current_item:
            messagebox.showerror("Error", "No item selected")
            return
        
        name = self.nameEntry.get()
        price = self.priceEntry.get()
        category = self.categoryEntry.get()
        image_url = self.imageEntry.get()
        description = self.descEntry.get()
        
        if not name or not price or not category:
            messagebox.showerror("Error", "Please fill in name, price, and category")
            return
        
        try:
            price_float = float(price)
        except ValueError:
            messagebox.showerror("Error", "Price must be a number")
            return
        
        payload = {
            'userId': self.controller.user_id,
            'name': name,
            'description': description,
            'price': price_float,
            'category': category,
            'image_url': image_url
        }
        
        try:
            api_url = f"{API_BASE_URL}/admin/menu-items/{self.current_item['item_id']}"
            response = requests.put(api_url, json=payload)
            response.raise_for_status()
            
            messagebox.showinfo("Success", "Menu item updated successfully!")
            self.controller.frames[AdminMenuPage].load_menu()
            self.controller.show_frame(AdminMenuPage)
            
        except requests.exceptions.RequestException as e:
            messagebox.showerror("Error", "Failed to update menu item")

class CartPage(tk.Frame): 
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        
        # Top button bar
        button_frame = tk.Frame(self)
        button_frame.pack(fill=tk.X, pady=5)
        
        backButton = ttk.Button(button_frame, text="Back", command=lambda: controller.show_frame(MenuPage))
        backButton.pack(side=tk.LEFT, padx=10)
        
        self.payButton = ttk.Button(button_frame, text="Proceed to Checkout", command=self.go_to_payment)
        self.payButton.pack(side=tk.RIGHT, padx=10)
        
        label = ttk.Label(self, text ="Cart Items", font = LARGEFONT)
        label.pack(pady=10)
        
        # Canvas for scrolling cart items
        canvas_frame = tk.Frame(self)
        canvas_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        canvas = tk.Canvas(canvas_frame, borderwidth=0)
        scrollbar = tk.Scrollbar(canvas_frame, orient="vertical", command=canvas.yview)
        self.cart_frame = tk.Frame(canvas)
        
        self.cart_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=self.cart_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.total_label = ttk.Label(self, text="Total: $0.00", font=LARGEFONT)
        self.total_label.pack(pady=10)
    
    def load_cart(self):
        # Clear existing cart display
        for widget in self.cart_frame.winfo_children():
            widget.destroy()
        
        if not self.controller.cart:
            empty_label = ttk.Label(self.cart_frame, text="Your cart is empty", font=SMALLFONT)
            empty_label.pack(pady=20)
            self.total_label.config(text="Total: $0.00")
            return
        
        total = 0
        for idx, item in enumerate(self.controller.cart):
            item_frame = tk.Frame(self.cart_frame, relief=tk.RIDGE, borderwidth=1)
            item_frame.pack(fill=tk.X, padx=10, pady=5)
            
            name_label = ttk.Label(item_frame, text=item['name'], font=("Verdana", 10, "bold"))
            name_label.grid(row=0, column=0, padx=10, pady=5, sticky="w")
            
            qty_label = ttk.Label(item_frame, text=f"Qty: {item['quantity']}")
            qty_label.grid(row=0, column=1, padx=10, pady=5)
            
            item_total = item['price'] * item['quantity']
            price_label = ttk.Label(item_frame, text=f"${item_total:.2f}")
            price_label.grid(row=0, column=2, padx=10, pady=5)
            
            remove_btn = ttk.Button(item_frame, text="Remove", 
                                   command=lambda i=idx: self.remove_item(i))
            remove_btn.grid(row=0, column=3, padx=10, pady=5)
            
            total += item_total
        
        self.total_label.config(text=f"Total: ${total:.2f}")
    
    def remove_item(self, index):
        if 0 <= index < len(self.controller.cart):
            self.controller.cart.pop(index)
            self.load_cart()
    
    def go_to_payment(self):
        print(f"Cart contents: {self.controller.cart}")
        print(f"Cart length: {len(self.controller.cart)}")
        
        if not self.controller.cart:
            messagebox.showerror("Error", "Your cart is empty!")
            return
        
        print("Loading restaurants...")
        self.controller.frames[RestaurantSelectionPage].load_restaurants()
        print("Showing RestaurantSelectionPage...")
        self.controller.show_frame(RestaurantSelectionPage)

class RestaurantSelectionPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        
        label = ttk.Label(self, text ="Select Restaurant Location", font = LARGEFONT)
        label.grid(row = 0, column = 2, padx = 10, pady = 10)
        
        backButton = ttk.Button(self, text="Back", command=lambda: controller.show_frame(CartPage))
        backButton.grid(row=0, column=0, padx=10, pady=10)
        
        # Frame for restaurant selection
        self.restaurant_frame = tk.Frame(self)
        self.restaurant_frame.grid(row=1, column=0, columnspan=5, padx=20, pady=20)
        
        self.selected_restaurant = None
        
        continueButton = ttk.Button(self, text="Continue to Payment", command=self.continue_to_payment)
        continueButton.grid(row=2, column=2, padx=10, pady=10)
    
    def load_restaurants(self):
        # Clear existing restaurant buttons
        for widget in self.restaurant_frame.winfo_children():
            widget.destroy()
        
        try:
            # Get restaurants from API
            response = requests.get(f"{API_BASE_URL}/restaurants")
            response.raise_for_status()
            restaurants = response.json()
            
            # Get delivery personnel info
            try:
                drivers_response = requests.get(f"{API_BASE_URL}/delivery-personnel")
                drivers_response.raise_for_status()
                drivers_data = drivers_response.json()
                print(f"Drivers response: {drivers_data}")
                drivers = {driver['delivery_person_id']: driver['name'] 
                          for driver in drivers_data}
                print(f"Drivers dict: {drivers}")
            except Exception as e:
                print(f"Error fetching drivers: {e}")
                drivers = {}
            
            # Create radio buttons for restaurant selection
            self.selected_restaurant = tk.IntVar()
            if restaurants:
                self.selected_restaurant.set(restaurants[0]['restaurant_id'])
            
            for idx, restaurant in enumerate(restaurants):
                driver_name = drivers.get(restaurant.get('delivery_person_id'), 'Not assigned')
                
                rb = ttk.Radiobutton(
                    self.restaurant_frame,
                    text=f"{restaurant['name']} - {restaurant['location']} (Driver: {driver_name})",
                    variable=self.selected_restaurant,
                    value=restaurant['restaurant_id']
                )
                rb.pack(anchor=tk.W, pady=5)
                
        except requests.exceptions.RequestException as e:
            # Fallback to default restaurant if API fails
            messagebox.showwarning("Warning", "Could not load restaurants. Using default location.")
            self.selected_restaurant = tk.IntVar(value=1)
    
    def continue_to_payment(self):
        if self.selected_restaurant is None:
            messagebox.showerror("Error", "Please select a restaurant location")
            return
        
        # Store selected restaurant in controller
        self.controller.selected_restaurant_id = self.selected_restaurant.get()
        
        # Continue to payment
        self.controller.frames[PaymentPage].prepare_payment()
        self.controller.show_frame(PaymentPage)

class PaymentPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        
        label = ttk.Label(self, text ="Payment Options", font = LARGEFONT)
        label.grid(row = 0, column = 2, padx = 0, pady = 10)
        
        self.total_label = ttk.Label(self, text="Total: $0.00", font=SMALLFONT)
        self.total_label.grid(row=1, column=2, padx=10, pady=5)

        cardNumLabel = ttk.Label(self, text = "Card Number: ", font = SMALLFONT)
        cardNumLabel.grid(row=2, column = 1, padx = 0, pady = 10)

        self.cardNumEntry = Entry(self, width=20)
        self.cardNumEntry.grid(row=2, column=2, padx=0, pady=10)
        
        cardHolderLabel = ttk.Label(self, text = "Card Holder: ", font = SMALLFONT)
        cardHolderLabel.grid(row=3, column = 1, padx = 0, pady = 10)

        self.cardHolderEntry = Entry(self, width=20)
        self.cardHolderEntry.grid(row=3, column=2, padx=0, pady=10)

        enterButton = ttk.Button(self, text="Place Order", command=self.place_order)
        enterButton.grid(row=4, column=2, padx=10, pady=5)

        backButton = ttk.Button(self, text="Back", command=lambda: controller.show_frame(CartPage))
        backButton.grid(row=5, column=2, padx=10, pady=5)
    
    def prepare_payment(self):
        total = sum(item['price'] * item['quantity'] for item in self.controller.cart)
        self.total_label.config(text=f"Total: ${total:.2f}")
    
    def place_order(self):
        card_number = self.cardNumEntry.get()
        card_holder = self.cardHolderEntry.get()
        
        if not card_number or not card_holder:
            messagebox.showerror("Error", "Please fill in all payment details")
            return
        
        if not self.controller.user_id:
            messagebox.showerror("Error", "Please login first")
            return
        
        # Get selected restaurant ID
        restaurant_id = getattr(self.controller, 'selected_restaurant_id', 1)
        
        # Calculate total
        total = sum(item['price'] * item['quantity'] for item in self.controller.cart)
        
        # Prepare order items
        items = [{
            'itemId': item['item_id'],
            'quantity': item['quantity'],
            'price': item['price']
        } for item in self.controller.cart]
        
        # API payload
        payload = {
            'userId': self.controller.user_id,
            'items': items,
            'totalAmount': total,
            'cardNumber': card_number,
            'cardHolder': card_holder,
            'restaurantId': restaurant_id
        }
        
        try:
            api_url = f"{API_BASE_URL}/order"
            response = requests.post(api_url, json=payload)
            response.raise_for_status()
            
            result = response.json()
            messagebox.showinfo("Success", result.get('message', 'Order placed successfully!'))
            
            # Clear cart and fields
            self.controller.cart = []
            self.cardNumEntry.delete(0, tk.END)
            self.cardHolderEntry.delete(0, tk.END)
            
            self.controller.show_frame(ThankYou)
            
        except requests.exceptions.RequestException as e:
            error_msg = "Order failed"
            try:
                error_data = e.response.json()
                error_msg = error_data.get('error', error_msg)
            except:
                pass
            messagebox.showerror("Order Failed", error_msg)


class ThankYou(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = ttk.Label(self, text ="Thank You for Your Order.", font = LARGEFONT)
        label.grid(row = 0, column = 2, padx = 0, pady = 10)

        exitButton = ttk.Button(self, text="Exit", command=lambda: controller.show_frame(StartPage))
        exitButton.grid(row=1, column=2, padx=0, pady=10)

        
 
 
# Driver Code
app = tkinterApp()
app.mainloop()