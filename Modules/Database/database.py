#A Python module which contains common functions that the book search, checkout, return and weeding modules use to interact with the database and log files.
import csv
from os import remove
from os.path import getsize

#takes filename (string) to return a list of dictionaries of a file
#used to read the database.txt and logfile.txt
def Read_File(filename):
    #using exception incase of an environmental error
    try:
        #opens the file to read
        with open(f"{filename}.txt", "r") as textFile:
            #using cvs dict reader to format the data
            file_read = csv.DictReader(textFile, delimiter="\t")

            #list to contain all the data from the file
            result = []

            for record in file_read:
                #adding record into the the list
                result.append(record)
            return result
    except EnvironmentError: 
        return "Error while reading file"

#overwrites the database with updated data
#takes the file (string) to overwrite and the data (list of dicts) along with the field names (list of strings)
def Over_Write_File(filename, data, fieldNames):
    #using exception incase of an environmental error
    try:
        #opens the file to write
        with open(f"{filename}.txt", "w") as textFile:
            #using csv dict writer for correct formatting
            file_write = csv.DictWriter(textFile, fieldnames=fieldNames, delimiter="\t")

            #writing the headings for each column with field names
            file_write.writeheader()

            #looping through each value in data
            for record in data:
                #overwirting each line with the new data
                file_write.writerow(record)
            return "Over-written file successfully"
    except EnvironmentError:
        return "Error while writing to File"

#adds new logs to the logfile
# takes filename (string), data (dict) and filenames (list of strings)
def Append_to_File(filename, data, fieldNames):
    #using exception incase of an environmental error
    try:
        txtFile = f"{filename}.txt"
        #opens the file to append
        with open(txtFile, "a") as textFile:
            #using csv dict writer for correct format
            file_append = csv.DictWriter(textFile, fieldnames=fieldNames, delimiter="\t")

            #if the file is empty
            if getsize(txtFile) == 0:
                #write the headings for each column
                file_append.writeheader()
            
            #add the new data into the file
            file_append.writerow(data)

            return "Appended to file successfully"
    except EnvironmentError:
        return "Error while appending to File"

# testing read, overwrite and append file fuctions
if __name__ == "__main__":
    print("\n" + 50*"#"+"\n")

    # creating a new file test.txt
    filename = "test"

    # creating the file with the fields DataID, DataName and Data 
    fieldNames = ["DataID", "DataName", "Data"]

    # testing valid data
    data = [{"DataID":"1", "DataName":"MyData", "Data":"Data"}]

    # creating the file and writing the data above
    feedback = Over_Write_File(filename, data, fieldNames)

    print(f'''Testing Over_Write_File function:
    Filename: {filename}.txt  |  fieldnames: {fieldNames}  |  data: {data}
    The result should output - Over-written file successfully
    Result: {feedback} ''')

    print("\n" + 50*"#"+"\n")

    # creating the file with the fields DataID, DataName and Data 
    fieldNames = ["DataID", "DataName", "Data"]

    # testing valid data
    data = {"DataID":"2", "DataName":"YourData", "Data":"Data2"}

    # creating the file and writing the data above
    feedback = Append_to_File(filename, data, fieldNames)

    print(f'''Testing Append_to_File function:
    Filename: {filename}.txt  |  fieldnames: {fieldNames}  |  data: {data}
    The result should output - Appended to file successfully
    Result: {feedback} ''')

    print("\n" + 50*"#"+"\n")

    # reading the file test.txt
    feedback = Read_File(filename)

    # formatting the result into a list called results
    results = []
    for row in feedback:
        record = {"DataID":row["DataID"], "DataName":row["DataName"], "Data":row["Data"]}
        results.append(record)

    # record1 and record2 represent expected outputs
    record1 = {"DataID":"1", "DataName":"MyData", "Data":"Data"}
    record2 = {"DataID":"2", "DataName":"YourData", "Data":"Data2"}

    print(f'''Testing Read_File function:
    Filename: {filename}.txt
    The result should output: {[record1, record2]}
    
    Result: {results} ''')

    # deleting the text file to ensure the test data isnt saved
    remove("test.txt")
