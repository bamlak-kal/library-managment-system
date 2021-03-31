#A Python module should suggest which book titles (not book copies) need to be removed from the library database. You might use the Matplotlib Python module to visualize unpopular book tittles to aid the weeding process. You should come up with the details of your own weeding criteria.

import Modules.Database.database as db

from datetime import date
import tkinter as tk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

#supressing matplotlib warnings 
import warnings
warnings.filterwarnings("ignore")

#function for fetching nessasary data for the weeding function
def Get_Data():
    #using database.py funciton to read database and logfile
    database = db.Read_File("database")
    logfile = db.Read_File("logfile")

    #creating a list of unique ISBN's to as it is the foreign key between database and logfile for UNIQUE books
    #i.e. books with the same ISBN but different BookID
    uniqueISBN = []
    bookData = []
    for record in database:
        if record["ISBN"] not in uniqueISBN:
            uniqueISBN.append(record["ISBN"])
            book = {"BookTitle":record["BookTitle"], "ISBN":record["ISBN"], "Author":record["Author"]}
            bookData.append(book)
    
    return uniqueISBN, bookData, logfile

#function for creating a list of weeding recommendations
def Book_Weed():
    #using get data to get the following data
    uniqueISBN, bookData, logfile = Get_Data()

    #toadys date for recording a log
    todaysYear = date.today().year

    #### three weeding catagories
    #preparing to calculate rating average for each unique ISBN
    ratingAverages = []

    #preparing to retrieve dates of last checkout for each unique ISBN
    lastCheckout = []

    #preparing to retrieve frequency of checkouts of each unique ISBN
    frequency = []

    #looping through the list of unique ISBNs to retrieve data to base the weeding on
    #this data will be rating, last time book was checked-out and frequency of checkouts
    for isbn in uniqueISBN:
        #list of ratings linked to a unique ISBN
        ratings = []

        #list of dates linked to a unique ISBN
        dates = []

        #looping through entire logfile
        for record in logfile:

            #if there is a log of a return operation, and the ISBN matches the current ISBN, 
            if record["Operation"] == "Return" and record["ISBN"] == isbn:
                    #add the rating of the record  to the ratings list
                    ratings.append(int(record["Rating"]))

            #if there is a log of a checkout operation, and the ISBN matches the current ISBN.
            if record["Operation"] == "Checkout" and record["ISBN"] == isbn:
                #since date format is dd/mm/yyyy, using split to create a list
                dateSplit = record["Date"].split("/")
                year = int(dateSplit[2])

                #add the date of the record to the list of dates
                dates.append(year)

        #adding number of checkouts (in the past 5 years) to the frequency list
        fiveYearcheckouts = [x for x in dates if x-todaysYear < 5]
        frequency.append(len(fiveYearcheckouts))

        #calculating the average from ratings list for each ISBN
        if len(ratings) == 0:
            #add a 0 if there is no rating for the ISBN
            #this signifies that this book should be weeded out
            ratingAverages.append(0)
        else:
            #calculate the average if there are ratings for the ISBN
            average = sum(ratings) / len(ratings)
            ratingAverages.append(average)

        #calculating the last time each ISBN was checked-out
        if len(dates) == 0:
            #if the book was never checked-out append a 10
            #this signifies that this book should be weeded out
            lastCheckout.append(10)
        else:
            #find the last time the book with an isbn as been checked-out
            mostRecent = dates[-1]
            #the difference between today and last time the ISBN was checked-out
            diff = todaysYear - mostRecent
            lastCheckout.append(diff)

    #average rating, last checkout date and average number of checkouts of all ISBNs
    avgRating = sum(ratingAverages) / len(ratingAverages)
    avgCheckout = sum(lastCheckout) / len(lastCheckout)
    avgFreq = sum(frequency) / len(frequency)
    
    #creating a list of the average results for plotting the data later on
    averageResults = [avgRating, avgCheckout, avgFreq, avgRating]

    #worst rated list to contain all books with an average rating of less than 2
    lowestRated = []
    for index, ratingValue in enumerate(ratingAverages):
        if ratingValue < 2:
            book = {"BookTitle":bookData[index]["BookTitle"], "ISBN":uniqueISBN[index], "Author":bookData[index]["Author"], "Rating":round(ratingAverages[index],1), "numOfcheckouts":frequency[index], "lastCheckout":lastCheckout[index]}
            lowestRated.append(book)

    #least checkouts list to contain books that have been checked-out less than 5 times
    leastCheckouts = []
    for index, frequencyValue in enumerate(frequency):
        if frequencyValue < 5:
            book = {"BookTitle":bookData[index]["BookTitle"], "ISBN":uniqueISBN[index], "Author":bookData[index]["Author"], "Rating":round(ratingAverages[index],1), "numOfcheckouts":frequency[index], "lastCheckout":lastCheckout[index]}
            leastCheckouts.append(book)

    #oldest checkout list to contain all books that were clast hecked-out over 8 years ago
    oldestCheckedout = []
    for index, difference in enumerate(lastCheckout):
        if  difference > 8:
            book = {"BookTitle":bookData[index]["BookTitle"], "ISBN":uniqueISBN[index], "Author":bookData[index]["Author"], "Rating":round(ratingAverages[index],1), "numOfcheckouts":frequency[index], "lastCheckout":lastCheckout[index]}
            oldestCheckedout.append(book)

    #worst books list to contain ISBN that appear in all three weeding catagories
    worstBooks = []
    
    #creating lists of ISBNs for each of the weeding catagories
    lowestISBN = [record["ISBN"] for record in lowestRated]
    oldestISBN = [record["ISBN"] for record in oldestCheckedout]
    leastISBN = [record["ISBN"] for record in leastCheckouts]

    #looping through the lowest rated ISBN list 
    for index, isbn in enumerate(lowestISBN):
        #checking if this ISBN is common in all three ISBN lists
        if isbn in  oldestISBN and isbn in leastISBN:
            bookRecord = {"BookTitle":bookData[index]["BookTitle"], "ISBN":uniqueISBN[index], "Author":bookData[index]["Author"], "Rating":round(ratingAverages[index],1), "numOfcheckouts":frequency[index], "lastCheckout":lastCheckout[index]}
            worstBooks.append(bookRecord) 

    #combining all the catagories into a list 
    weedingData= [worstBooks, lowestRated, leastCheckouts, oldestCheckedout]

    return averageResults, weedingData

#function for creating the polar plot into plotting frame
#this takes frm - the frame to display the plot in, pos - the index of the book the unpacked weeding data
def Polar_Plot(frm, pos):
    #getting the average results and weedingdata from the weeding function
    averageResults, weedingData = Book_Weed()

    #unpacks the weeding data into a single list containing all the books
    unpack = []
    for catagory in weedingData:
        for item in catagory:
            unpack.append(item)

    #the book to be plotted based on the index - pos
    book = unpack[pos]

    #plotting catagories
    radarCatagories = ["Rating", "Num of Checkouts", "Last Checked-out"]

    #the plotting data of the book i.e. rating, frequency of checkouts and last checkout
    plotData = [book["Rating"], book["numOfcheckouts"], book["lastCheckout"], book["Rating"]]

    #angles to place the plots, degrees for the labels of the plot
    plotPlacementDegrees = [0, 120, 240, 0]

    #angles in radians for the data plot
    plotPlacement = [x*3.14159/180 for x in plotPlacementDegrees]

    #creating a figure of size 5x7
    fig = plt.Figure(figsize=(5,7), dpi=80)
    
    #figure defined as a subplot for the polar plot
    plt.subplot(polar=True)

    #creating the subplot for the book as a polar plot
    ax = fig.add_subplot(111, polar=True)

    #creating the labels to replace the angle labels
    ax.set_xticks(plotPlacement[:-1], minor=False)
    ax.set_xticklabels(radarCatagories, size=12, fontdict=None, minor=False)

    #plotting the book data and filling the area with blue
    ax.plot(plotPlacement, plotData)
    ax.fill(plotPlacement, plotData, 'b', alpha=0.1)

    #creating subplot for averages plot as a polar plot
    ay = fig.add_subplot(111, polar=True)

    #plotting the average data and filling the area orange
    ay.plot(plotPlacement, averageResults)
    ay.fill(plotPlacement, averageResults, 'r', alpha=0.1)

    #concatinating the book title with 'Comparison
    heading = book["BookTitle"] + " Comparison"
    
    #setting the title for the plot to be heading
    fig.suptitle(heading, fontdict={"fontsize":20})

    #adding a legend to differentiate the book plot and average plot
    fig.legend(labels = [book["BookTitle"], "Average"], loc=(0.1,0.8))

    #adjusting the position of the figure
    fig.subplots_adjust(left = 0.045, bottom=-0.1)

    #creating a widget to display the figure in the frame frm
    chart = FigureCanvasTkAgg(fig, frm)
    chart.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1, padx=10, pady=(5,10))


# these functions are untestable without extensive control over the database (outside of coursework spec)