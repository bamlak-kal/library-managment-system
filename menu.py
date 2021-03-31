#A python main program which provides the required menu options to the librarian for the program functionalities. The menu could be based on Python Graphical User Interface-GUI (namely the tkinter python module). In that case, the GUI must use only one window.

from tkinter.ttk import *
import tkinter as tk
import csv
import Modules.booksearch as booksearch
import Modules.bookreturn as bookreturn
import Modules.bookcheckout as bookcheckout
import Modules.bookweed as bookweed

#Refresh for removing all children of a parent i.e. master window and frames
def Refresh(element):
    for widget in element.winfo_children():
        widget.destroy()
    return element

#Page_Access for converting an index into a page, 0 = dashboard function, 1 = weed function
def Page_Access(pageID):
    #unbinding mousescroll wheel from the canvas on weeding page
    window.unbind_all('<MouseWheel>')

    if pageID == 0:
        Dashboard()
    elif pageID == 1:
        Weed()

#header function which creates the top, side navigation boxes and body frame
def Header():
    #specifying the global selected car and resetting the window
    global selected
    Refresh(window)

    #configureing the window to accomodate frames
    window.columnconfigure(0, weight=1)
    window.columnconfigure(1, weight=5)
    window.rowconfigure(0, weight=1)
    window.rowconfigure(1, weight=10)

    #upper navigation frame - contains heading text and light/dask mode buttons
    frm_upperNav = Frame(window, style="one.TFrame")
    frm_upperNav.grid(row=0, column=0, columnspan=2, sticky="nesw")
    frm_upperNav.grid_propagate(0)

    lbl_tTitle = Label(frm_upperNav, textvariable = headerText, style="uHed.TLabel")
    lbl_tTitle.pack(side=tk.LEFT, padx=(30,0), pady=10)

    #color pallet change buttons dark mode and light mode (top right)
    #darkmode button
    btn_darkMode = tk.Button(   frm_upperNav, 
                                text="Dark", 
                                width=5, 
                                relief=tk.RIDGE, 
                                fg=colorPallet[0], 
                                font=('Arial', 11, "bold"), 
                                bg=colorPallet[1], 
                                #lambda function passes two arguments to color change function, dark/light and the current page which should be home
                                command= lambda: Change_Colors("dark","home")
                            )
    btn_darkMode.pack(side=tk.RIGHT, padx=(10,20))

    #light mode button
    btn_lightMode = tk.Button(  frm_upperNav, 
                                text="Light", 
                                width=5, 
                                relief=tk.RIDGE, 
                                fg=colorPallet[0], 
                                font=('Arial', 11, "bold"), 
                                bg=colorPallet[1],
                                #lambda function passes two arguments to color change function, dark/light and the current page which should be home
                                command= lambda: Change_Colors("light","home")
                                )
    btn_lightMode.pack(side=tk.RIGHT)

    #side navigation frame - contains navigation buttons
    frm_sideNav = Frame(window, style="sNav.TFrame")
    frm_sideNav.grid(row=1, column=0, rowspan=2, sticky="nesw")
    frm_sideNav.grid_propagate(0)

    #side navigation buttons creation
    titles = ["Dashboard", "Book Weed"]
    Label(frm_sideNav, background=colorPallet[2]).pack(side=tk.TOP, padx=80, pady=(5,0))
    for x in range(2):
        btn_nav = tk.Button(frm_sideNav, 
                            text=titles[x], 
                            bg=colorPallet[2], 
                            fg=colorPallet[0], 
                            font=('Arial', 12), 
                            relief=tk.FLAT,
                            #lambda function that runs page access with a unique argument i for each button
                            command=lambda i=x:
                                Page_Access(i)
                            )
        btn_nav.pack(side=tk.TOP, pady=3, fill=tk.X)

    #side navigation logout button creation
    btn_logout = tk.Button( frm_sideNav, 
                            text="Logout", 
                            bg=colorPallet[2], 
                            fg=colorPallet[0], 
                            font=('Arial', 12), 
                            relief=tk.FLAT, 
                            #lambda function that takes user back to login page
                            command= lambda: 
                                Login_Page("","")
                            )
    Hover(btn_logout, "add")
    btn_logout.pack(side=tk.BOTTOM, pady=15, fill=tk.X)

    #main body frame creation for reuse
    frm_body = Frame(window, style="body.TFrame")
    frm_body.grid(row=1, column=1, sticky="nesw")
    frm_body.grid_propagate(0)

    # starting page based on selected
    if selected == "":
        Page_Access(0)
    else:
        pageID = titles.index(selected)
        Page_Access(pageID)

#Button_Hover for highlighting navigation button for current page
def Button_Hover():
    global selected
    #list of navigation (nav) buttons
    navButtons = []

    #appending side navigation button objects into a navButtons list
    headerFrames = window.winfo_children()
    sNav = headerFrames[1]
    for child in sNav.winfo_children():
        navButtons.append(child)

    #removing the first widget from navBuuttons
    navButtons = navButtons[1:]

    #highlighting the button that has the same text as the selected page
    for btn_nav in navButtons:
        #if the button is of the selected page
        if btn_nav['text'] == selected:
            #configuring the button so it has the correct color and no command
            btn_nav.config(bg = colorPallet[3])
            btn_nav.bind('<Button-1>', "break")
            #removing the hover property for the button
            Hover(btn_nav, "remove")
        else:
            #give the button the hover property and the correct color
            btn_nav.config(bg = colorPallet[2])
            btn_nav.unbind("<Button 1>")
            Hover(btn_nav, "add")

#a Hover for binding a function to navigation buttons
def Hover(btn_nav, operation):
    #if statment to either add the binding or remove the binding from an event
    if operation == "add":
        #enter event - when cursor is on button - make color light blue
        btn_nav.bind("<Enter>", lambda e: btn_nav.config(bg=colorPallet[3]))

        #leave event - when cursor is off button - make color dark blue
        btn_nav.bind("<Leave>", lambda e: btn_nav.config(bg=colorPallet[2]))
    elif operation == "remove":
        btn_nav.bind("<Leave>", lambda e: btn_nav.config(bg=colorPallet[3]))

#Change_Colors for changing the color pallet of the whole window
def Change_Colors(color, page):
    #editing the global colorPallet
    global colorPallet
    if color == "light":
        #                  WHITE        RED         BLUE      L-BLUE       BLACK
        colorPallet = {0:"#e8e8e8",1:"#f05454",2:"#30475e",3:"#416180",4:"black"}
    elif color == "dark":
        #                  WHITE       D-Purp      BLUE        Purp        BLACK
        colorPallet = {0:"#e8e8e8",1:"#2d132c",2:"#160f30",3:"#441E4B",4:"black"}

    #updating styles based on new colors
    Define_Styles()

    #sending user to current page after color change
    if page == "login":
        Login_Page("","")
    elif page == "home":
        Header()

#Page_Innit for initialising every page
def Page_Innit():
    #changing the title to the name of the selected page
    headerText.set(selected)

    #updating navigation buttons
    Button_Hover()

    #retrieveing frm_body to be updated
    headerFrames = window.winfo_children()

    #deleting all child widgets of frm_body
    frm_body = Refresh(headerFrames[2])
    return frm_body

#Dashboard: page to facilitate searching, checking out and returning books
def Dashboard():
    #updating global selected with new heading
    global selected
    selected = "Dashboard"

    #page innit returns the frame body to be reused
    frm_body = Page_Innit()

    ################# Left frame in dashboard - contains search, add/remove basket buttons and cart

    frm_dashboard = Frame(frm_body, style="body.TFrame")
    frm_dashboard.pack(side=tk.LEFT, fill=tk.Y, padx=(20,0), pady=20)

    ################# Search label frame with an input field, search button and error label

    lblfrm_search = tk.LabelFrame(frm_dashboard, text="Seach Book", relief=tk.RIDGE, fg="white", bg=colorPallet[3], bd=3, font=('Arial', 13))
    lblfrm_search.pack(side=tk.TOP, fill=tk.BOTH, padx=0, pady=(0,10))

    lbl_errSearch= Label(lblfrm_search, width=20, text="", style="body.TLabel")
    lbl_errSearch.pack(side=tk.TOP, padx=10, pady=10)

    #frame to horizontally align input field and search button
    frm_searchInput = Frame(lblfrm_search, style="body.TFrame")
    frm_searchInput.pack(side=tk.TOP, fill=tk.X, padx=0, pady=(0,20))

    ent_searchBar = Entry(frm_searchInput, width=14, font=('Arial', 12))
    ent_searchBar.pack(side=tk.LEFT, fill=tk.X, expand=1, padx=10, pady=0)

    btn_search = tk.Button(frm_searchInput, 
                            text="Search", 
                            width=10, 
                            relief=tk.RIDGE, 
                            fg=colorPallet[0], 
                            font=('Arial', 11, "bold"), 
                            bg=colorPallet[1], 
                            #lambda function for updating treeview based on search inputs
                            command= lambda: 
                                #function takes the value of the search bar, database treeview widget and error label
                                booksearch.Treeview_Update(ent_searchBar.get(), tree_search, lbl_errSearch)
                            )
    btn_search.pack(side=tk.LEFT, padx=(0,10), pady=0)

    ################## Frame containing add and remove items from cart buttons

    frm_addRemoveCart = Frame(frm_dashboard, style="body.TFrame")
    frm_addRemoveCart.pack(side=tk.TOP, fill=tk.X, padx=0, pady=(0,10))

    #button for adding books into cart
    btn_addCart = tk.Button(frm_addRemoveCart, 
                            text="Add to Cart", 
                            width=15, 
                            relief=tk.RIDGE, 
                            fg=colorPallet[0], 
                            font=('Arial', 11, "bold"), 
                            bg=colorPallet[1], 
                            #lambda function for adding selected items to cart
                            command= lambda: 
                                #function takes the database treeview widget and cart treeview widget
                                Add_to_Cart(tree_search, tree_checkoutReturn)
                            )
    btn_addCart.pack(side=tk.LEFT,fill=tk.X, expand=1, padx=10, pady=0)

    #button for removeing books from cart
    btn_removeCart = tk.Button( frm_addRemoveCart,
                                text="Remove from Cart", 
                                width=15, 
                                relief=tk.RIDGE, 
                                fg=colorPallet[0], 
                                font=('Arial', 11, "bold"), 
                                bg=colorPallet[1], 
                                #lambda function for removing selected items from cart
                                command= lambda: 
                                    #function takes the cart treeview widget
                                    Remove_from_Cart(tree_checkoutReturn)
                                )
    btn_removeCart.pack(side=tk.LEFT,fill=tk.X, expand=1, padx=(0,10), pady=0)

    ################## Label frame containing error label, treeview (cart) and checkout/return buttons

    lblfrm_checkoutReturn = tk.LabelFrame(frm_dashboard, text="Checkout and Returns", relief=tk.RIDGE, fg="white", bg=colorPallet[3], bd=3, font=('Arial', 13))
    lblfrm_checkoutReturn.pack(side=tk.TOP, fill=tk.BOTH, expand=1, padx=0, pady=0)

    #frame containing input field for memberID and an option menu for rating
    frm_checkoutReturn0 = Frame(lblfrm_checkoutReturn, style="body.TFrame")
    frm_checkoutReturn0.pack(side=tk.TOP, fill=tk.X, padx=0, pady=0)

    #memberID label and entry field
    lbl_memberID= Label(frm_checkoutReturn0, text="MemberID:", style="body.TLabel")
    lbl_memberID.pack(side=tk.LEFT, padx=(20,0), pady=0)
    ent_memberID = Entry(frm_checkoutReturn0, width=5, font=('Arial', 12))
    ent_memberID.pack(side=tk.LEFT, fill=tk.X, padx=10, pady=0)

    #string tkinter variable to store rating value
    rating = tk.StringVar()
    rating.set(1)
    #option menu and label for option menu
    opt_rating = OptionMenu(frm_checkoutReturn0, rating, *[1,1,2,3,4,5], style="rating.TMenubutton")
    opt_rating.pack(side=tk.RIGHT, padx=(0,20), pady=0)
    opt_rating.config(width=3)
    lbl_rating= Label(frm_checkoutReturn0, text="Rating:", style="body.TLabel")
    lbl_rating.pack(side=tk.RIGHT, padx=10, pady=10)

    #error label for returning and checking out books
    lbl_errCheckoutReturn= Label(lblfrm_checkoutReturn, text="", style="body.TLabel")
    lbl_errCheckoutReturn.pack(side=tk.TOP, fill=tk.X, padx=10, pady=0)

    #treeview for cart 
    tree_checkoutReturn = Treeview(lblfrm_checkoutReturn, style="search.Treeview")
    tree_checkoutReturn.pack(side=tk.TOP, fill=tk.BOTH, expand=1, padx=0, pady=10)

    tree_checkoutReturn["columns"]=("one","two","three")
    tree_checkoutReturn.column("#0", width=80, minwidth=80, stretch=tk.NO, anchor=tk.CENTER)
    tree_checkoutReturn.column("one", width=110, minwidth=110)
    tree_checkoutReturn.column("two", width=110, minwidth=110)
    tree_checkoutReturn.column("three", width=70, minwidth=70, stretch=tk.NO)

    tree_checkoutReturn.heading("#0", text="BookID", anchor=tk.CENTER)
    tree_checkoutReturn.heading("one", text="BookTitle",anchor=tk.W)
    tree_checkoutReturn.heading("two", text="ISBN",anchor=tk.W)
    tree_checkoutReturn.heading("three", text="Status",anchor=tk.W)

    #frame to horizontally display return and checkout buttons
    frm_checkoutReturn1 = Frame(lblfrm_checkoutReturn, style="body.TFrame")
    frm_checkoutReturn1.pack(side=tk.TOP, fill=tk.X, padx=0, pady=(0,10))

    #buttons for checking out books
    btn_checkout = tk.Button(   frm_checkoutReturn1, 
                                text="Checkout Books", 
                                width=15, 
                                relief=tk.RIDGE, 
                                fg=colorPallet[0], 
                                font=('Arial', 11, "bold"), 
                                bg=colorPallet[1], 
                                #lambda function taking a list of two functions
                                command= lambda: [
                                    #first function runs book checkout function 
                                    #this takes the cart treeview, error label and memberID entry input
                                    bookcheckout.Cart_Checkout( tree_checkoutReturn,
                                                                lbl_errCheckoutReturn,
                                                                ent_memberID.get()) ,
                                    #this function updates the database treeview to the current search
                                    #query found in the search entry
                                    booksearch.Treeview_Update( ent_searchBar.get(), 
                                                                tree_search, 
                                                                lbl_errSearch)
                                                ]
                            )
    btn_checkout.pack(side=tk.LEFT,fill=tk.X, expand=1,  padx=10, pady=0)

    #button to return books fromt the cart
    btn_return = tk.Button( frm_checkoutReturn1, 
                            text="Return Books", 
                            width=15, 
                            relief=tk.RIDGE, 
                            fg=colorPallet[0], 
                            font=('Arial', 11, "bold"), 
                            bg=colorPallet[1], 
                            #lambda function takes a list of two functions
                            command= lambda: [
                                #cart return function takes the cart treeview, error label and rating value
                                #from the option menu
                                bookreturn.Cart_Return( tree_checkoutReturn,
                                                        lbl_errCheckoutReturn, 
                                                        rating.get()), 
                                #runs treeview update function based on the current value of the search input
                                booksearch.Treeview_Update( ent_searchBar.get(), 
                                                            tree_search, 
                                                            lbl_errSearch)
                                            ]
                            )
    btn_return.pack(side=tk.LEFT,fill=tk.X, expand=1,  padx=(0,10), pady=0)

    ################## tree search treeview, displays the whole database in a treeview

    tree_search = Treeview(frm_body, style="search.Treeview")
    tree_search.pack(side=tk.RIGHT, fill=tk.BOTH, expand=1, padx=20, pady=20)

    tree_search["columns"]=("one","two","three","four","five")
    tree_search.column("#0", width=80, minwidth=80, stretch=tk.NO, anchor=tk.CENTER)
    tree_search.column("one", width=110, minwidth=110)
    tree_search.column("two", width=110, minwidth=110)
    tree_search.column("three", width=110, minwidth=110)
    tree_search.column("four", width=110, minwidth=110, stretch=tk.NO)
    tree_search.column("five", width=70, minwidth=70, stretch=tk.NO)

    tree_search.heading("#0", text="BookID", anchor=tk.CENTER)
    tree_search.heading("one", text="BookTitle",anchor=tk.W)
    tree_search.heading("two", text="ISBN",anchor=tk.W)
    tree_search.heading("three", text="Author",anchor=tk.W)
    tree_search.heading("four", text="PurchaseDate",anchor=tk.W)
    tree_search.heading("five", text="Status",anchor=tk.W)

    #runs treeview update function with an arument of " ", database treeview widget and error label
    #this will searching for a space returns all the values from the database - to be displayed
    booksearch.Treeview_Update(" ", tree_search, lbl_errSearch)

#add to cart function updates the cart treeview by adding the selected items
def Add_to_Cart(tree_search, cart):
    #loops through the slected items in the database treeview
    for row in tree_search.selection():
        #retrieving book ID and the book data
        bookID = tree_search.item(row)["text"]
        values = tree_search.item(row)["values"]
        record = [bookID]

        #concatinating the book id with the values into a list
        for i in values:
            record.append(i) 

        #inserting the new row into the cart treeview
        cart.insert(parent="", index="end", text=record[0], values=(record[1], record[2], record[5]))

#Remove_from_Cart for removing items from the cart
def Remove_from_Cart(cart):
    #loops through selected items in the cart and deletes them
    for row in cart.selection():
        cart.delete(row)

#weed (function) for plotting and showing weeding recommendations
def Weed():
    #preparing weeding page for widgets
    global selected
    selected = "Book Weed"
    frm_body = Page_Innit()

    ################## label frame for the polar plot of each book

    lblfrm_plot = tk.LabelFrame(frm_body, text="Plot", width=315, relief=tk.RIDGE, fg="white", bg=colorPallet[3], bd=3, font=('Arial', 13))
    lblfrm_plot.pack(side=tk.LEFT, fill=tk.BOTH, expand=1, padx=(10,5), pady=10)

    ################## canvas for the scrollable frame 

    canvas=tk.Canvas(frm_body, bg=colorPallet[3], width=575, highlightthickness=0)
    canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=1, padx=(5,10), pady=10)

    #creating a scrollbar to scroll through the canvas's y axis
    vbar=Scrollbar(frm_body,orient=tk.VERTICAL, style="TScrollbar", command=canvas.yview)
    vbar.pack(side=tk.RIGHT,fill=tk.Y)

    #setting the scroll bar as the event for the yscroll command of the canvas
    canvas.configure(yscrollcommand=vbar.set)

    #scrollable frame to contain a list of weeding recommendations

    frame = tk.Frame(canvas, bg=colorPallet[3])
    framWindow = canvas.create_window(0,0, anchor='nw', window=frame)

    #binding the event of 'Configure' to update the canvas width and the scroll region of the scroll bar
    canvas.bind("<Configure>", 
                lambda e: [
                    canvas.itemconfig(framWindow, width=canvas.winfo_width()), 
                    canvas.configure(scrollregion=canvas.bbox("all"))
                        ]
                )
    
    #binding the scroll wheel movement to the scroll bar
    canvas.bind_all("<MouseWheel>", lambda e: canvas.yview_scroll(int(-1*(e.delta/120)), "units"))

    ################## label frames for displaying book weeding data 

    #retrieving nessasary data to plot the book information
    x , weedingData = bookweed.Book_Weed()

    headings = ["Weed Recommendations  (in all three weeding catagories)", "Lowest Rated (average rating of less than 2)", "Least Checked-out (checked-out less than 5 times in the past 5 years)", "Oldest Checkouts (last checked-out over 8 years ago)"]

    #J variuable used to count the number of books displayed
    j = 0

    #looping through the catagories of weeding data - i.e. worst books, lowest rated, least checked-out and oldest checkouts
    for index, catagory in enumerate(weedingData): 
        #label frame fro storing each catagory
        lblfrm_weed = tk.LabelFrame(frame, text=headings[index], relief=tk.RIDGE, fg="white", bg=colorPallet[3], bd=3, font=('Arial', 13))
        lblfrm_weed.pack(side=tk.TOP, fill=tk.BOTH, expand=1, pady=10)

        #if there is no books in the catagory then display the message:
        if len(catagory) == 0:
            lbl_noBooks = Label(lblfrm_weed, text="No books in this catagory", style="body.TLabel")
            lbl_noBooks.pack(side=tk.TOP, padx=10, pady=(10,20))
        #if there are books in the catagory
        else:
            for book in catagory:
                #frame for displaying each book's data
                frm_bookData = Frame(lblfrm_weed, style="body.TFrame")
                frm_bookData.pack(side=tk.TOP, fill=tk.BOTH, expand=1, padx=10, pady=5)

                #frame for displaying the book title, isbn and author
                frm_bookDetails = Frame(frm_bookData, style="one.TFrame")
                frm_bookDetails.pack(side=tk.LEFT, fill=tk.BOTH,expand=1)

                #frame for displaying raing, number of checkouts and last checkout
                frm_bookStats = Frame(frm_bookData, style="sNav.TFrame")
                frm_bookStats.pack(side=tk.LEFT, fill=tk.BOTH,expand=1)

                #frame for a button to plot the data of the corrisponding book
                frm_bookPlot = Frame(frm_bookData, style="sNav.TFrame")
                frm_bookPlot.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)

                #lists containing the titles and dictionary keys required for displaying the labels
                details = [["Title: ", "ISBN: ", "Author: "], ["BookTitle", "ISBN", "Author"]]
                stats = [["Rating: ", "Num of checkouts (past 5 years): ", "Last checked-out: "], ["Rating", "numOfcheckouts", "lastCheckout"]]

                for x in range(3):
                    #concatinates the label for the data with the data for each book
                    #i.e.          Title:                Dune
                    detailsText = details[0][x] + book[details[1][x]]

                    #label to display items from details list
                    lbl_bookDetails = Label(frm_bookDetails, width=24, text= detailsText, style="details.TLabel")
                    lbl_bookDetails.pack(side=tk.TOP, fill=tk.Y, anchor=tk.W, padx=5, pady=5)

                    #i.e.          Rating:           3.5
                    statsText = stats[0][x] + str(book[stats[1][x]])

                    #label for displaying items from stats list
                    lbl_bookStats = Label(frm_bookStats, width=30, text=statsText, style="book.TLabel")
                    lbl_bookStats.pack(side=tk.TOP, fill=tk.Y,anchor=tk.W, padx=5, pady=5)

                #button for plotting the data for each book
                btn_plot= tk.Button(frm_bookPlot, 
                                    text="Plot", 
                                    width=15, 
                                    relief=tk.RIDGE, 
                                    fg=colorPallet[0], 
                                    font=('Arial', 11), 
                                    bg=colorPallet[1], 
                                    #lambda function takes a list with two functions
                                    command= lambda i=j: [
                                        #refresh function removes the current plot
                                        Refresh(lblfrm_plot), 
                                        #plor plot plots the new plot into the lblfrm_plot for the book index i
                                        #i will be unique for each button as it increments
                                        bookweed.Polar_Plot(lblfrm_plot, i)
                                                        ]
                )
                btn_plot.pack(side=tk.LEFT,fill=tk.BOTH, expand=1,  padx=5, pady=5)

                #incrementing j for each new book displayed
                j += 1 

    bookweed.Polar_Plot(lblfrm_plot, 0)

#login page, runs recursively untill username and password is correct
def Login_Page(username, password):
    headerText.set("Login")
    Refresh(window)

    #row and column config
    window.columnconfigure(0, weight=3)
    window.columnconfigure(1, weight=1)
    window.rowconfigure(0, weight=1)
    window.rowconfigure(1, weight=0)

    ### main divisions for right and left frames ###
    frm_leftBox = Frame(window, style="left.TFrame")
    frm_leftBox.grid(row=0,column=0, sticky="nesw")

    frm_loginForm = Frame(window, style="one.TFrame")
    frm_loginForm.grid(row=0,column=1, sticky="nesw")

    frm_image = Frame(window, style="body.TFrame")
    frm_image.grid(row=0, column=0, sticky="nesw")
    # loginPic = tk.PhotoImage(file="loginPic.png")
    # image = Label(frm_image, image=loginPic)
    # image.image = loginPic
    # image.place(x=0, y=0)

    ### title ###
    lbl_loginTitle = Label(frm_loginForm, textvariable = headerText, style="ttl.TLabel")
    lbl_loginTitle.pack(side=tk.TOP, pady=120)

    ### inputs ###    
    #email frame
    frm_username = Frame(frm_loginForm, width=330, height=30, style="one.TFrame")
    frm_username.pack(side=tk.TOP)

    #email label
    lbl_username = Label(frm_username, text="Username:", style="inp.TLabel")
    lbl_username.place(x=0, y=5)

    #email error message label
    lbl_errEmail = Label(frm_username, style="err.TLabel")
    lbl_errEmail.place(x=225, y=5)
    validUser = False
    if username != "abc" and username != "":
        lbl_errEmail.config(text="Invalid Username!",)
    elif username != "":
        validUser = True

    #email input
    ent_enterUsername = Entry(frm_loginForm, style="ent.TEntry", width=14, font=('Arial', 12))
    ent_enterUsername.pack(side=tk.TOP, pady=5, ipadx=100, ipady=3)

    #password frame
    frm_pass= Frame(frm_loginForm,width=330, height=30, style="one.TFrame")
    frm_pass.pack(side=tk.TOP)

    #password label
    lbl_pass = Label(frm_pass, text="Password:", style="inp.TLabel")
    lbl_pass.place(x=0, y=5)

    #password error message label
    lbl_errPass = Label(frm_pass, style="err.TLabel")
    lbl_errPass.place(x=225, y=5)
    validPass = False
    if password != "abc" and password != "":
        lbl_errPass.config(text="Invalid Password!")
    elif password != "":
        validPass = True

    #password input
    ent_enterPass = Entry(frm_loginForm, show="*", width=14, font=('Arial', 12))
    ent_enterPass.pack(side=tk.TOP, pady=5, ipadx=100, ipady=3)
    
    ### submit button ###
    btn_submitBtn = tk.Button(frm_loginForm, text="Login", fg=colorPallet[0], bg=colorPallet[2], font=('Arial', 15, 'bold'), width= 15, height=1, bd=2, relief=tk.RIDGE)
    btn_submitBtn.config(command= lambda: Login_Page(ent_enterUsername.get(), ent_enterPass.get()))
    btn_submitBtn.pack(side=tk.TOP, pady=20)

    frm_colorMode = Frame(frm_loginForm, width=330, height=30, style="one.TFrame")
    frm_colorMode.pack(side=tk.BOTTOM)
    
    btn_darkMode = tk.Button(   frm_colorMode, 
                                text="Dark", 
                                width=5, 
                                relief=tk.RIDGE, 
                                fg=colorPallet[0], 
                                font=('Arial', 11, "bold"), 
                                bg=colorPallet[1], 
                                command= lambda: 
                                    Change_Colors("dark","login")
                            )
    btn_darkMode.pack(side=tk.RIGHT, pady=20)

    btn_lightMode = tk.Button(  frm_colorMode, 
                                text="Light", 
                                width=5, 
                                relief=tk.RIDGE, 
                                fg=colorPallet[0], 
                                font=('Arial', 11, "bold"), 
                                bg=colorPallet[1], 
                                command= lambda: Change_Colors("light","login")
                            )
    btn_lightMode.pack(side=tk.LEFT, pady=20)

    #chenge to dashbaord if correct credentials
    if validPass == True and validUser == True:
        Header()

# Define_Styles creates the styleing used for the whole window
def Define_Styles():
    global colorPallet
    #styles
    styles = Style()
    styles.theme_use("alt")

    #styles for frames
    styles.configure("one.TFrame", background=colorPallet[1])
    styles.configure("sNav.TFrame", background=colorPallet[2])
    styles.configure("body.TFrame", background=colorPallet[3])
    styles.configure("left.TFrame", background=colorPallet[4])

    #styles for labels
    styles.configure("ttl.TLabel", foreground=colorPallet[0], background=colorPallet[1], font=('Arial', 50, "bold"))
    styles.configure("inp.TLabel", foreground=colorPallet[0], background=colorPallet[1], font=('Arial', 13, "bold"))
    styles.configure("details.TLabel", foreground=colorPallet[0], background=colorPallet[1], font=('Arial', 11, "bold"))
    styles.configure("err.TLabel", foreground="yellow", background=colorPallet[1], font=('Arial', 8, "bold"))
    styles.configure("sHed.TLabel", foreground=colorPallet[0], background=colorPallet[2], font=('Arial', 20, "bold"))
    styles.configure("sItem.TLabel", foreground=colorPallet[0], background=colorPallet[2], font=('Arial', 16, "bold"))
    styles.configure("uHed.TLabel", foreground=colorPallet[0], background=colorPallet[1], font=('Arial', 20, "bold"))
    styles.configure("body.TLabel", foreground=colorPallet[0], background=colorPallet[3], font=('Arial', 12))
    styles.configure("book.TLabel", foreground=colorPallet[0], background=colorPallet[2], font=('Arial', 11))

    #style for treeiview
    styles.configure("search.Treeview", rowheight=20, foreground=colorPallet[0], background=colorPallet[3], fieldbackground=colorPallet[3], font=('Arial', 10))
    styles.map("search.Treeview", foreground=[("!selected",colorPallet[0])], background=[("!selected",colorPallet[3]), ("selected", colorPallet[1])])
    styles.configure("search.Treeview.Heading", foreground=colorPallet[0], background=colorPallet[2], fieldbackground=colorPallet[2], font=('Arial', 10))
    styles.map("search.Treeview.Heading", background=[("!selected",colorPallet[2])])

    #style for option menu
    styles.configure("rating.TMenubutton", foreground=colorPallet[0], background=colorPallet[3], fieldbackground=colorPallet[3], font=('Arial', 10))
    styles.map("rating.TMenubutton", background=[("!selected",colorPallet[2])])

    #style for scrollbar
    styles.configure("TScrollbar", background=colorPallet[0], troughcolor=colorPallet[2], )

    #test styles during development
    # t = Style()
    # t.configure("t1.TFrame", background="pink")
    # t.configure("t2.TFrame", background="orange")

################################################################################
##################################### Main #####################################
################################################################################

#defining tkinter window
window = tk.Tk()

#window name
window.title("Library Management Tool")

#window dimentions and resizability = false
window.geometry("1200x650")

#setting minimum size of window
window.minsize(height = 650, width=1200)

#making window un-resizable
# window.resizable(False, False)

#global vars
#selected  for storing the current page
selected = ""  
#                  WHITE        RED         BLUE      L-BLUE        BLACK
colorPallet = {0:"#e8e8e8",1:"#f05454",2:"#30475e",3:"#416180",4:"#416180"}

#styles
Define_Styles()

#tk var for heading text of each page
headerText = tk.StringVar()

#starting at the login page
Login_Page("","")

window.mainloop()
