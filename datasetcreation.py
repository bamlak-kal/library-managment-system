#this file will create the required dataset
import random
import csv

def Createlist():
    #creates a list from a text file with a list of items on each line
    temp = []
    with open("add.txt", "r") as addThis:
        for line in addThis:
            temp.append(line)
    createdList = [x.rstrip() for x in temp]
    return createdList

def Create_Database(numberOfbooks, numOfcopies):
    bookTitlewords = ['Ficciones', 'Ulysses', 'Splat', 'Cloudstreet', 'Blackout', 'Eunoia', 'Bluets', 'Dogsbody', 'Nox', 'Echo', 'Heidi', 'Blameless', 'Changeless', 'Affinity', 'PrairyErth', 'Shane', 'Emma', 'Synergetics', 'Walden', 'PenseÃ©s', 'Utopia', 'Bibelot', 'Jingo', 'Hogfather', 'Maskerade', 'Pyramids', 'Sourcery', 'Mort', 'Memorare', 'Wintersmith', 'Thud!', 'Bibliomen', 'Castleview', 'Peace', 'Beauty', 'Flipped', 'Splendid', 'Labyrinth', 'Jewel', 'Paradise', 'Night', 'Wicked', 'Atonement', 'Eclipse', 'Twilight', 'Push', 'Birdsong', 'Freedom', 'Persuasion', 'Room', 'Speak', 'Diary', 'Neverwhere', 'Choke', 'Imperium', 'Fingersmith', 'Possession', 'Thunderstruck', 'She', 'Sunshine', 'Weight', 'Rebecca', 'Running', 'Piano', 'Witness', 'Atticus', 'Jumper', 'Quentins', 'Soulless', 'Siddhartha', 'Scaramouche', 'Prague', 'Fatherland', 'Eragon', 'Elynia', 
    'Elsewhere', 'Clapton', 'Biblioholism', 'Angelica', 'Ice', 'Shipwrecks', 'Coraline', 'Harbor', 'Identity', 'Beaufort', 'Kitchen', 'Feed', 'Desertion', 'Lolita', 'Disgrace', 'Libra', 'Mysterium', 'Birdman', 'Dupe', 'Firewall', 'Afterimage', 'Unstuck', 'Payback', 'Nudge', 'Sway', 'Free', 'Outliers', 'Winning', 'Leadership', 'Godless', 'Giving', 'Jazz', 'Bliss', 'Lita', 'Lucy', 'Beloved', 'Cubicles', 'Joy', 'Passing', 'Temptation', 'Logic', 'Always', 'Eden', 'Dune', 'Until', 'Love', 'Emotions', 'Crave', 'Cane', 'Rising', 'Banjo', 'Sugar', 'Roots', 'Freakonomics', 'Blink']

    # caps = [x[0].upper()+x[1:] for x in bookTitlewords]
    # print(caps)
        

    authorNames = ['Steve Farabaugh', 'Viola Concannon', 'Fredia Hurston', 'Jenniffer Higgenbotham', 'Shirly Annunziata', 'Lady Bullen', 'Arlie Sand', 'Argentina Narciso', 'Thresa Hosford', 'Robby Luedtke', 'Talitha Jang', 'Holly Gaudreau', 'Miranda Mclellan', 'Arnold Rehn', 'Enda Marmon', 'Johna Darosa', 'Blanca Hartig', 'Dian Huard', 'Sherita Thaxton', 'Sabra Cookson', 'Steve Farabaugh', 'Viola Concannon', 'Fredia Hurston', 'Jenniffer Higgenbotham', 'Shirly Annunziata', 'Lady Bullen', 'Arlie Sand', 'Argentina Narciso', 'Thresa Hosford', 'Robby Luedtke', 'Talitha Jang', 'Holly Gaudreau', 'Miranda Mclellan', 'Arnold Rehn', 'Enda Marmon', 'Johna Darosa', 'Blanca Hartig', 'Dian Huard', 'Sherita Thaxton', 'Sabra Cookson']

    fieldNames = ["BookID", "BookTitle", "ISBN", "Author", "PurchaseDate", "Status"]

    with open("database.txt", "w") as database:
        database_write = csv.DictWriter(database, fieldnames=fieldNames, delimiter="\t")

        database_write.writeheader()

        for x in range(0,numOfbooks,numOfcopies):

            bookID = x

            bookTitle = random.choice(bookTitlewords) if random.randint(1,2)==1 else random.choice(bookTitlewords) + " " + random.choice(bookTitlewords)

            isbn = random.randint(1000000000000,9999999999999)

            author = random.choice(authorNames)

            purchaseDate = str(random.randint(1,30)) + "/" + str(random.randint(1,12)) + "/" + str(random.randint(1980,2020))

            status = random.choice([0,random.randint(1000,9999)])

            for x in range(numOfcopies):
                status = random.choice([0,random.randint(1000,9999)])

                newRow = {"BookID":(bookID+x), "BookTitle":bookTitle, "ISBN":isbn, "Author":author, "PurchaseDate":purchaseDate, "Status":status}

                database_write.writerow(newRow)


def Read_Database(p):
    with open("database.txt", "r") as database:
        database_read = csv.DictReader(database, delimiter="\t")

        for x in range(p):
            print(next(database_read))

def Create_UniqueBooks():
    fieldNames = ["BookTitle","ISBN", "Rating"]


    with open("database.txt", "r") as database:
        database_read = csv.DictReader(database, delimiter="\t")

        uniqueISBN = []
        uniqueDictList = []
        for record in database_read:
            if record["ISBN"] not in uniqueISBN:
                uniqueISBN.append(record["ISBN"])
                uniqueDictList.append(record)

    # use this for ordering new books

        # for item in uniqueDictList:
        #     rate = random.randint(0,5)
        #     newRow = {"BookTitle":item["BookTitle"],"ISBN":item["ISBN"], "Rating":rate}
        #     uniqueBooks_write.writerow(newRow)

try: 
    numOfbooks = int(input('How many books? '))
    numOfcopies = int(input('How many copies of each book? '))
except:
    print('Enter only numbers. ')


Create_Database(numOfbooks,numOfcopies)

# numOfrows = 5
# Read_Database(numOfrows)

# Create_UniqueBooks()
