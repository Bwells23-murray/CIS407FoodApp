import tkinter as tk
from tkinter import ttk
from tkinter.ttk import *
from tkinter import PhotoImage
import requests
 

LARGEFONT =("Verdana", 18)
SMALLFONT = ("Veranda", 10)
 
class tkinterApp(tk.Tk):
    
    # __init__ function for class tkinterApp 
    def __init__(self, *args, **kwargs): 
        
        # __init__ function for class Tk
        tk.Tk.__init__(self, *args, **kwargs)

        self.title("McDougals App")
        self.geometry("300x550")
        
        # creating a container
        container = tk.Frame(self)  
        container.pack(side = "top", fill = "both", expand = True) 
 
        container.grid_rowconfigure(0, weight = 1)
        container.grid_columnconfigure(0, weight = 1)
 
        # initializing frames to an empty array
        self.frames = {}  
 
        # iterating through a tuple consisting
        # of the different page layouts
        for F in (StartPage, LoginPage, RegisterPage, MenuPage, CartPage, PaymentPage):
 
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
 
        #username field
        username = Entry(self, width= 20)
        username.grid(row= 1 , column=2)

        #password field
        password = Entry(self, width=20)
        password.grid(row=2, column=2)

        result_label = ttk.Label(self, font=SMALLFONT)

        def make_api_call():
            user_input = username.get() 
            password_input = password.get()

            # Construct your API endpoint and payload
            api_url = "http://localhost:5000/login" # Replace with your API endpoint
            payload = {"param1": user_input, "param2": password_input}

            try:
                response = requests.post(api_url, json=payload) # Or .get(), .put(), etc.
                response.raise_for_status() # Raise an exception for bad status codes

                api_response_data = response.json()
                # Process the API response data here
                result_label.config(text=f"API Response: {api_response_data}")

            except requests.exceptions.RequestException as e:
                result_label.config(text=f"API Error: {e}")
            except ValueError: # If response is not valid JSON
                result_label.config(text="Error: Invalid JSON response from API")
 
        def buttonCommand():
            #lambda : controller.show_frame(MenuPage),
            make_api_call()
            
        # button to show frame 3 with text
        # layout2
        enterButton = ttk.Button(self, text ="Enter",
                            command = buttonCommand)
        
        
    
        # putting the button in its place by 
        # using grid
        enterButton.grid(row = 3, column = 2, padx = 10, pady = 10)
 
 
 
 
# third window frame registerPage
class RegisterPage(tk.Frame): 
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = ttk.Label(self, text ="Please Register", font = LARGEFONT)
        label.grid(row = 0, column = 2, padx = 10, pady = 10)
 
        #username field
        username = Entry(self, width= 20)
        username.grid(row= 1 , column=2)

        #password field
        password = Entry(self, width=20)
        password.grid(row=2, column=2)
 
        # button to show frame 3 with text
        # layout2
        enterButton = ttk.Button(self, text ="Enter",
                            command = lambda : controller.show_frame(MenuPage))
    
        # putting the button in its place by 
        # using grid
        enterButton.grid(row = 3, column = 2, padx = 10, pady = 10)

class MenuPage(tk.Frame): 
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = ttk.Label(self, text ="Menu Items", font = LARGEFONT)
        label.grid(row = 0, column = 2, padx = 10, pady = 10)

        def addItemCommand ():
            print("Button clicked!")

        breakfastLabel = ttk.Label(self, text = "Breakfast", font = SMALLFONT)
        breakfastLabel.grid(row = 1, column = 1, padx = 10, pady = 10)

        pancakeButton = ttk.Button(self, text = "Pancakes", command = addItemCommand)
        pancakeButton.grid(row = 2, column = 1, padx=10, pady=10)

        bsButton = ttk.Button(self, text = "Breakfast Sandwich", command = addItemCommand)
        bsButton.grid(row = 2, column = 2, padx=10, pady=10)

        dinnerLabel = ttk.Label(self, text = "Dinner", font = SMALLFONT)
        dinnerLabel.grid(row = 3, column = 1, padx = 10, pady = 10)

        burgerButton = ttk.Button(self, text = "Burger", command = addItemCommand)
        burgerButton.grid(row = 4, column = 1, padx=10, pady=10)

        nuggetsButton = ttk.Button(self, text = "Nuggets", command = addItemCommand)
        nuggetsButton.grid(row = 4, column = 2, padx=10, pady=10)

        sidesLabel = ttk.Label(self, text = "Sides", font = SMALLFONT)
        sidesLabel.grid(row = 5, column = 1, padx = 10, pady = 10)

        friesButton = ttk.Button(self, text = "Fries", command = addItemCommand)
        friesButton.grid(row = 6, column = 1, padx=10, pady=10)

        asButton = ttk.Button(self, text = "Apple Slices", command = addItemCommand)
        asButton.grid(row = 6, column = 2, padx=10, pady=10)

        dessertLabel = ttk.Label(self, text = "Dessert", font = SMALLFONT)
        dessertLabel.grid(row = 7, column = 1, padx = 10, pady = 10)

        psButton = ttk.Button(self, text = "Pie Slice", command = addItemCommand)
        psButton.grid(row = 8, column = 1, padx=10, pady=10)

        cookieButton = ttk.Button(self, text = "Cookie", command = addItemCommand)
        cookieButton.grid(row = 8, column = 2, padx=10, pady=10)

        cartButton = ttk.Button(self, text="Cart", command = lambda : controller.show_frame(CartPage))
        cartButton.grid(row = 0, column= 4, padx=10, pady=10)

class CartPage(tk.Frame): 
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = ttk.Label(self, text ="Cart Items", font = LARGEFONT)
        label.grid(row = 0, column = 2, padx = 10, pady = 10)

        payButton = ttk.Button(self, text = "Pay", command = lambda : controller.show_frame(PaymentPage))
        payButton.grid(row = 4, column = 2, padx = 10, pady = 10)

class PaymentPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent,)
        label = ttk.Label(self, text ="Payment Options", font = LARGEFONT)
        label.grid(row = 0, column = 2, padx = 0, pady = 10)

        cardNumLabel = ttk.Label(self, text = "Card Number: ", font = SMALLFONT)
        cardNumLabel.grid(row=1, column = 1, padx = 0, pady = 10)

        cardNumEntry = Entry(self, width=20)
        cardNumEntry.grid(row=1, column=2, padx=0, pady=10)


        
 
 
# Driver Code
app = tkinterApp()
app.mainloop()