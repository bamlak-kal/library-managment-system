#A Python module which contains functions used to ask the librarian for the ID of the book(s) they wish to return and provide either an appropriate error message, or a message letting them know they have returned the book(s) successfully.
import random
import Modules.Database.database as db
from datetime import datetime as dt

#a function for returning books to the library, and also recoring the rating
def Return(bookID, rating):
    #a list containing dictionaries of every book
    database_read = db.Read_File("database")

    #a list to contain the updated database
    editedFile = []

    #used to check if the book id is within the database
    exists = False
    for record in database_read:
        #if the book id is found
        if record["BookID"] == bookID:
            #if the book has been checked-out
            if record["Status"] != "0":
                #edit the status to be 0
                record["Status"] = "0"

                #record the isbn to store in the logs
                isbn = record["ISBN"]

                #signify that the book exists
                exists = True
            else:
                return "Book was never checked-out"

        #add evey book from the database into editedFile list
        editedFile.append(record)
    
    if exists == False:
        return "Book not in Database"

    #creating list of field names for dict writer of database.txt
    dbFieldNames = ["BookID", "BookTitle", "ISBN", "Author", "PurchaseDate", "Status"]

    #using database function to overwrite database.txt with edited list
    writeTodatabase = db.Over_Write_File("database", editedFile, dbFieldNames)

    #if the operation is not successful, then output the error message
    if writeTodatabase != "Over-written file successfully":
        return writeTodatabase 

    #creating a list of field names for dict writer of logfile.txt
    logFieldNames = ["Operation", "BookID", "ISBN", "Date","MemberID", "Rating"]

    #retrieving todays date 
    today = dt.today()
    date = today.strftime("%d/%m/%Y")

    #creating a random dates
    # date = str(random.randint(1,30)) + "/" + str(random.randint(1,12)) + "/" + str(random.randint(2010,2020))

    #creating the dictionary to append to logfile
    log = {"Operation":"Return", "BookID":bookID, "ISBN":isbn, "Date":date, "MemberID":"Null", "Rating":rating}
    
    #using database function to append the log to logfile.txt
    appendTologfile = db.Append_to_File("logfile", log, logFieldNames)

    #if the operation is unseccessful then return the error message
    if appendTologfile != "Appended to file successfully":
        return appendTologfile
    
    #return true once successfull return
    return True

def Cart_Return(cart, feedbackLabel, rating):
    #looping through all items in the cart treeview
    for row in cart.get_children():
        #retrieving book id for each book
        bookID = cart.item(row)["text"]
        
        #returning book alongside its rating
        returnResults = Return(bookID, rating)

        #if the operation is successful, return a success message
        if returnResults == True:
            feedbackLabel.config(foreground="white", text="Successfully Returned")
            cart.delete(row)
        else:
            #otherwise return the error message in red and stop this function
            feedbackLabel.config(foreground="red", text=f"BookID {bookID}: {returnResults}")
            break

#test inputs prints the results of returning a book with the params - bookID and rating
def Test_Inputs(bookID):
    for x in range(3):
        # rating is being generated randomly 1-5 as it is selected from a drop down menu
        rating = random.randint(1,5)
        print(f"BookID: {bookID[x]}  |  Rating: {rating}")
        
        #returning the book and printing the resultl
        result = Return(str(bookID[x]), str(rating))
        print(result,"\n")
        
    print(50*"#"+"\n")

#testing the return process, 
if __name__ == "__main__":
    print(50*"#"+"\n")

    print("Testing valid Book ID and a rating 1-5")
    print("Results should be either True or a book related error \n")
    bookID = [1,100,149]
    Test_Inputs(bookID)


    print("Testing invalid Book ID and a rating 1-5")
    print("Result should be - Book not in Database \n")
    bookID = [1000, False, "*/£"]
    Test_Inputs(bookID)
