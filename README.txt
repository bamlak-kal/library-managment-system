-----------------------------------------------------------------------------------------------------
--------------------- Bamlak Terefe - submission for Library Management System ----------------------
-----------------------------------------------------------------------------------------------------
----------------------- LOGIN (case sensitive): username: abc, password: abc ------------------------
-----------------------------------------------------------------------------------------------------

------------------- SPECIAL HIGHLIGHTS 

- Ensured that only the body/necessary widgets were refreshed when switching pages. This
  is the frm_body for the majority of the code

- Using loops for creating navigation buttons along with a page access function to allow
  easy addition of new pages - all a new programmer would need to do is add the function
  into page access, update the for loop's count and create the new page function

- Using a color pallet dictionary for all the colors of the window, allows for easily
  switching between color pallets for light and dark mode

- Created three weeding categories (rating, number of checkouts, and last checkout year) to
  be plotted to allow the librarian to compare each book with the average book

- Implemented a host of user-friendly features such as:
   - ensuring the database treeview is showing the last search query after checking-out/returning a book
   - highlighting navigation buttons once selected or hovered
   - a cart system for group checkouts and returns
   - binding scroll bar wheel to the scroll bar
   - ability to resize the window
   - light and dark modes

-----------------------------------------------------------------------------------------------------

INSTRUCTIONS:

------------------- STARTUP -------------------

1: Run menu.py

2: Enter credentails for login - (username: abc, password: abc)

 - You will be taken to the dashboard page 

------------------- DASHBOARD PAGE -------------------

 - dashboard features booksearch, bookcheckout and book return

----- FOR SEARCHING 

1: Input query into search bar

2: Click on search button

 - Relevant results should be displayed in the table on the right
 - Error message will display if nothing is displayed in the table

----- FOR ADDING BOOKS INTO THE CART

1: Select books from the table on the right to checkout (can multi-select using Ctrl + MouseButton1)
   - Selected items should be highlighted orange

2: Click on 'Add to Cart' button

----- TO REMOVE FROM CART

1: Select books from the cart (table on the bottom left)
   - Selected items should be highlighted orange

2: Click on 'Remove from Cart' button

----- TO CHECKOUT BOOKS

1: Add the books to checkout into the cart

2: Enter a memberID into the input field

4: Click on 'Checkout Books' button

 - Books from the cart should be checked-out and their statuses will be changed to the memberID supplied
 - Books should be removed from cart
 - Error messages should appear for many cases

----- TO RETURN BOOKS

1: Add the books to checkout into the cart

2: Use option menu to select the rating of the book

4: Click on 'Return Books' button

 - Books from the cart should be returned and their statuses will be changed to 0
 - Books should be removed from cart
 - Error messages should appear for many cases

------------------- WEEDING PAGE -------------------

 - weeding page features a plot (left), a list of weeding recommendations (right)

----- TO PLOT BOOK DATA

1: Click on the plot button corresponding to the book you want plotted

-----------------------------------------------------------------------------------------------------





