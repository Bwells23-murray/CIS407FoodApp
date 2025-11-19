import tkinter as tk
from tkinter import ttk
from tkinter.ttk import *
from tkinter import PhotoImage
 

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
        for F in (StartPage, LoginPage, RegisterPage, MenuPage, CartPage):
 
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

        img = PhotoImage(file="CIS407 Project/Assets/McDonalds arch.png")
        image_label = tk.Label(self, image=img)
        image_label.grid(row = 1, column = 2)
 
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
 

        # def getUsername():
        #     return username
        # def getPassword():
        #     return password
        # def buttonCommand():
        #     getUsername(),
        #     getPassword(),
        #     lambda : controller.show_frame(Page3)

        # button to show frame 3 with text
        # layout2
        enterButton = ttk.Button(self, text ="Enter",
                            command = lambda : controller.show_frame(MenuPage))
        
        
    
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
        entry1 = Entry(self, width= 20)
        entry1.grid(row= 1 , column=2)

        #password field
        entry2 = Entry(self, width=20)
        entry2.grid(row=2, column=2)
 
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

        cartPhoto = PhotoImage(file= r"CIS407 Project/Assets/cart.png")
        cartButton = ttk.Button(self, text="Cart", command = lambda : controller.show_frame(CartPage))
        cartButton.grid(row = 0, column= 4, padx=10, pady=10)

class CartPage(tk.Frame): 
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = ttk.Label(self, text ="Cart Items", font = LARGEFONT)
        label.grid(row = 0, column = 2, padx = 10, pady = 10)
 
        
 
 
# Driver Code
app = tkinterApp()
app.mainloop()