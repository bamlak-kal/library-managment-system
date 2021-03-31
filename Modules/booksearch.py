# A Python module which contains functions used to allows librarian to input search terms as strings, and returns the output as described in the previous section. You can either: load the contents of database.txt into a list, and store this as a global variable for repeated use, or load the contents of database.txt each time a search is performed.
import Modules.Database.database as db

#function to return a list of relevant books
def Search(query):
    #list to contain dictionaries of relevant books
    searchResults =[]

    #using database funcion to get a list of all record in database.txt
    database_read = db.Read_File("database")

    #lowering the query to small case to prevent case sensitivity
    query = str(query).lower()
    
    #using to check if the book exists in the database
    exists = False

    #looping through all items in the database
    for record in database_read:
        #if the isbn is in either book title, author or isbn, it becomes a relevant book
        if query in record["BookTitle"].lower() or query in record["Author"].lower() or query in record["ISBN"]:
            searchResults.append(record)

            #signifies the book exists
            exists = True

    if exists == False:
        return "Book not in Database"
   
    return searchResults

#functiont o update the database treeivew in the dashboard
#takes the query from the entry widget, the database treeview and the error label
def Treeview_Update(query, treeviewObject, errorLabel):
    #loops through each item in the database and removes them
    for i in treeviewObject.get_children():
        treeviewObject.delete(i)

    #retrieves the relevant books from running book search on the query
    searchResults = Search(query)

    #returns an error if the book is not in database
    if searchResults == "Book not in Database":
        errorLabel.config(text=searchResults)
    else:
        #clear the text from the error label
        errorLabel.config(text="")
        
        #adding relevant books (from the search) into database treeview
        for record in searchResults:
            treeviewObject.insert(parent="", index="end", text=record["BookID"], values=(record["BookTitle"], record["ISBN"], record["Author"], record["PurchaseDate"], record["Status"]))


#testing the search process
if __name__ == "__main__":
    print(50*"#"+"\n")

    print("Testing valid queries")
    print("Results should contain the query in either BookTitle, ISBN or Author columns \n")
    query = ["echo","3773739648655","Talitha"]
    print(f"Query1: {query[0]}  |  Query2: {query[1]}  |  Query3: {query[2]}")

    #loops through each query and searches for the results
    for item in query:
        result = Search(item)
        print(f"\n Results for {item}: \n")

        # if the results arnt empty
        if result != "Book not in Database":
            #prints the results in a table format
            for x, book in enumerate(result):
                book = f'"BookID": {book["BookID"]}, "BookTitle": {book["BookTitle"]}, "ISBN": {book["ISBN"]}, "Author": {book["Author"]}, "PurchaseDate": {book["PurchaseDate"]}, "Status": {book["Status"]}'
                print(f"Book {x}: {book}")
        else:
            print(result)

    print("\n" + 50*"#"+"\n")

    print("Testing invalid queries")
    print("Results should output - Book not in Database \n")

    # note testing invalid queries with numbers as ISBN could contain them
    query = ["INVALIDBOOK","INVALIDISBN",True]
    print(f"Query1: {query[0]}  |  Query2: {query[1]}  |  Query3: {query[2]}")

    #loops through each query and searches for the results
    for item in query:
        result = Search(item)
        print(f"\n Results for {item}: \n")

        # if the results arnt empty
        if result != "Book not in Database":
            #prints the results in a table format
            for x, book in enumerate(result):
                book = f'"BookID": {book["BookID"]}, "BookTitle": {book["BookTitle"]}, "ISBN": {book["ISBN"]}, "Author": {book["Author"]}, "PurchaseDate": {book["PurchaseDate"]}, "Status": {book["Status"]}'
                print(f"Book {x}: {book}")
        else:
            print(result)

    print("\n" + 50*"#"+"\n")