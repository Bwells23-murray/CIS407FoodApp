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
        
        # creating a container
        container = tk.Frame(self)  
        container.pack(side = "top", fill = "both", expand = True) 
 
        container.grid_rowconfigure(0, weight = 1)
        container.grid_columnconfigure(0, weight = 1)
 
        # initializing frames to an empty array
        self.frames = {}  
 
        # iterating through a tuple consisting
        # of the different page layouts
        for F in (StartPage, LoginPage, RegisterPage, MenuPage, AdminMenuPage, CartPage, PaymentPage, ThankYou):
 
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
            controller.frames[AdminMenuPage].load_menu()
            controller.show_frame(AdminMenuPage)

        adminButton = ttk.Button(self, text="Admin", command=go_to_admin)
        adminButton.grid(row=0, column=1, padx=10, pady=10)
    
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
        print("Button clicked!")
    
    def go_to_cart(self):
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
                    
                    col += 1
                    if col > 1:  # 2 items per row for an kiosk feel likethey have at the mcdonalds 
                        col = 0
                        row_counter += 1
                
                if col != 0:  # Move to next row if we didn't complete the row
                    row_counter += 1
                    
        except requests.exceptions.RequestException as e:
            messagebox.showerror("Error", f"Failed to load menu: {e}")

class CartPage(tk.Frame): 
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = ttk.Label(self, text ="Cart Items", font = LARGEFONT)
        label.grid(row = 0, column = 2, padx = 10, pady = 10)

        payButton = ttk.Button(self, text = "Pay", command = lambda : controller.show_frame(PaymentPage))
        payButton.grid(row = 4, column = 2, padx = 10, pady = 10)

class PaymentPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = ttk.Label(self, text ="Payment Options", font = LARGEFONT)
        label.grid(row = 0, column = 2, padx = 0, pady = 10)

        cardNumLabel = ttk.Label(self, text = "Card Number: ", font = SMALLFONT)
        cardNumLabel.grid(row=1, column = 1, padx = 0, pady = 10)

        cardNumEntry = Entry(self, width=20)
        cardNumEntry.grid(row=1, column=2, padx=0, pady=10)

        enterButton = ttk.Button(self, text="Enter", command=lambda : controller.show_frame(ThankYou))
        enterButton.grid(row=4, column=2, padx=10, pady=5)

        backButton = ttk.Button(self, text="Back", command=lambda: controller.show_frame(CartPage))
        backButton.grid(row=5, column=2, padx=10, pady=5)


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