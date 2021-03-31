#A Python module which contains functions used to ask librarian for borrower’s member-ID and the ID of the book(s) they wish to withdraw. Then, after performing the validity checks and functionality described in the previous section, should return a message letting the librarian know whether they have withdrawn the book successfully.

import random
import Modules.Database.database as db
from datetime import date as dt


#function to change the a specified (with bookID) book's status to a memberID
def Checkout(bookID, memberID):
    #checking if the memberID field is empty
    if memberID == "":
        return "Please Enter member ID"

    #checking if the memberID is a 4 digit integer
    elif len(str(memberID)) != 4 or str(memberID).isdecimal() != True: 
        return "Invalid member ID"
    else:
        #stores a list of dictionaries of the books in the database
        database_read = db.Read_File("database")

        #a list to store the updated database
        editedFile = []

        #checking if the bookID supplied is in database
        exists = False
        for record in database_read:
            #if the bookID is found
            if record["BookID"] == bookID:
                #if the status shows the book has not been checked-out
                if record["Status"] == "0":
                    #checkout the book by replacing the memberID
                    record["Status"] = memberID

                    #stores the isbn of the checked-out book
                    isbn = record["ISBN"]

                    #showing that the book exists in the database
                    exists = True
                else:
                    #book is already checkedout if the status is not 0
                    return "Book already checked-out"

            #adding all records from database into the list
            editedFile.append(record)
        
        #after looping through database, if exists still = false
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

        #retreiveing todays date 
        today = dt.today()
        date = today.strftime("%d/%m/%Y")

        #creating a random date
        # date = str(random.randint(1,30)) + "/" + str(random.randint(1,12)) + "/" + str(random.randint(2010,2020))
        
        #creating the dictionary to append to logfile
        log = {"Operation":"Checkout", "BookID":bookID, "ISBN":isbn, "Date":date, "MemberID":memberID, "Rating":"Null"}

        #using database function to append the log to logfile.txt
        appendTologfile = db.Append_to_File("logfile", log, logFieldNames)

        #if the operation is unseccessful then return the error message
        if appendTologfile != "Appended to file successfully":
            return appendTologfile

        #upon completion, return true
        return True

#a function for updating the treeview cart display
#this function takes the treeview cart widget, feedback label and the member id value
def Cart_Checkout(cart, feedbackLabel, memberID):
    #loops through all the books in the cart
    for row in cart.get_children():
        #retrieves the ID of each book
        bookID = cart.item(row)["text"]

        #runs checkout function on each book
        checkoutResults = Checkout(bookID, memberID)

        #if the checkout is successfull
        if checkoutResults == True:
            #update the feedback label to show success
            feedbackLabel.config(foreground="white", text="Successfully Checked-out")
            
            #remove the book from the cart
            cart.delete(row)
        else:
            #otherwise return the error in red and prevent abort this function
            feedbackLabel.config(foreground="red", text=f"BookID {bookID}: {checkoutResults}")
            break

#test inputs prints the results of checking out the books with the params - bookID and memberID
def Test_Inputs(bookID, memeberID):
    for x in range(3):
        #returning the book and printing the result
        print(f"BookID: {bookID[x]}  |  MemberID: {memeberID[x]}")
        result = Checkout(str(bookID[x]), str(memeberID[x]))
        print(result,"\n")
        
    print(50*"#"+"\n")


#testing the checkout process
if __name__ == "__main__":
    print(50*"#"+"\n")

    print("Testing valid Book ID and valid member ID")
    print("Results should be either True or a book related error \n")
    bookID = [1,100,149]
    memeberID = [1000, 5000, 9999]
    Test_Inputs(bookID, memeberID)

    print("Testing valid Book ID and invalid member ID")
    print("Results should be - Invalid memberID \n")
    bookID = [1,100,149]
    memeberID = [0, "xyz", True]
    Test_Inputs(bookID, memeberID)

    print("Testing invalid Book ID and valid member ID")
    print("Results should be - Book not in Database \n")
    bookID = [1000, False, "*/£"]
    memeberID = [1000, 5000, 9999]
    Test_Inputs(bookID, memeberID)

    print("Testing invalid Book ID and invalid member ID")
    print("Results should be - Invalid memeberID \n")
    bookID = [1000, False, "*/£"]
    memeberID = [0, "xyz", True]
    Test_Inputs(bookID, memeberID)
