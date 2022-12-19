#-----------------------------------#
#                                   #
#              Import               #
#                                   #
# ----------------------------------#    


from datetime import datetime
from icalendar import Calendar
import json
import mysql.connector
import os
import requests


#-----------------------------------#
#                                   #
#          Global Variables         #
#                                   #
# ----------------------------------#


#update_rooms = True if you want to update the rooms
#update_occupancy = True if you want to update the occupancy
update_rooms = False
update_occupancy = False

#url for generate the ics file
url = "https://planning.univ-ubs.fr/jsp/custom/modules/plannings/anonymous_cal.jsp?data=d3be1fff3397511bf2829d59289190e54592592d3b282f749c9a606b710f264fdc5c094f7d1a811b903031bde802c7f597e5f20f622768ff000996ffaaa109f62d0bb596bf80452fd9b95e257006d2f8166c54e36382c1aa3eb0ff5cb8980cdb,1"

C1 = "C1_8h-9h30"
C2 = "C2_9h45-11h15"
C3 = "C3_11h30-13h"
C4 = "C4_13h00-14h30"
C5 = "C5_14h45-16h15"
C6 = "C6_16h30-18h00"
C7 = "C7_18h15-19h45"

dayLists = ["01-lundi","02-mardi","03-mercredi","04-jeudi","05-vendredi","06-samedi","07-dimanche"]
crenLists = [C1,C2,C3,C4,C5,C6,C7]


#-----------------------------------#
#                                   #
#            Functions              #
#                                   #
# ----------------------------------#
   

'''
Description : Analyze the ics file to get the first and the last day when an event appears 
Parameters : file (string) : the name of the file
Return : [string,string] with the format (DD-MM-YYYY) : the first and last day when an event appears
'''
def findDateADE(file):
    g = open(file,'r', encoding = 'utf-8')
    gcal = Calendar.from_ical(g.read())
    min = 99999999
    max = 10000000
    for event in gcal.walk():
        #for each event we get the start and the end date and we compare them to the min and max
        if event.name == "VEVENT":
            dtstart = event.get("DTSTART").to_ical().decode("utf-8")[:8]
            if int(dtstart) < min:
                min = int(dtstart) 
            dtend = event.get("DTEND").to_ical().decode("utf-8")[:8]
            if int(dtend) > max:
                max = int(dtend)
    g.close()
    #write min and max with the format DD-MM-YYYY
    min = str(min)[6:8] + "-" + str(min)[4:6] + "-" + str(min)[:4]
    max = str(max)[6:8] + "-" + str(max)[4:6] + "-" + str(max)[:4]
    return min,max


'''
Description : Download/update the ics file in the directory data with the url
Parameters : url (string) : the url of the ics file
Return : None
'''
def downloadIcsFile(url):
    start = datetime.now()
    if not os.path.exists("data"):
        print("Making directory data...")
        os.makedirs("data")
    #if the directory is not empty
    if len(os.listdir("data")) != 0:
        print("Deleting files in data...")
        for file in os.listdir("data"):
            os.remove("data/" + file)
    print("Downloading the ics file...")
    r = requests.get(url)
    with open("data/ADE_ToRename.ics", 'wb') as f:
        f.write(r.content)
    f.close()
    end = datetime.now()
    print("Downloading time: " + str(end - start))
    return
    

'''
Description : Convert the ics file to a json file
Parameters : file (string) : the name of the ics file
Return : None
'''
def convertIcalToJson(file):
    global startADE
    global stopADE
    print("Converting the ics file to a json file...")
    start = datetime.now()
    el2 = 'LOCATION'
    myTab = set()
    startADE = 99999999
    stopADE = 10000000
    g = open(file,'r', encoding='utf-8')
    gcal = Calendar.from_ical(g.read())
    for component in gcal.walk():
        if component.name == "VEVENT":
            dtstart = component.get("DTSTART").to_ical().decode("utf-8")[:8]
            if int(dtstart) < startADE:
                startADE = int(dtstart) 
            dtend = component.get("DTEND").to_ical().decode("utf-8")[:8]
            if int(dtend) > stopADE:
                stopADE = int(dtend)
            for r in component.get(el2).split(","):
                myTab.add(r.encode().decode("utf-8"))
    g.close()

    #write startADE and stopADE with the format DD-MM-YYYY
    startADE = str(startADE)[6:8] + "-" + str(startADE)[4:6] + "-" + str(startADE)[:4]
    stopADE = str(stopADE)[6:8] + "-" + str(stopADE)[4:6] + "-" + str(stopADE)[:4]

    end = datetime.now()
    print("Conversion time: " + str(end-start))
    return myTab

    
'''
Description : Create the json file with the rooms
Parameters : url (string) : the url of the ics file
Return : None
'''
def getRooms(url):
    if not os.path.exists("./json"):
        os.makedirs("./json")
    #if thre is already the file rooms.json in the directory json we delete it
    if os.path.exists("./json/rooms.json"):
        print("Deleting the file rooms.json...")
        os.remove("./json/rooms.json")
    downloadIcsFile(url)
    result = convertIcalToJson("data/ADE_toRename.ics")
    os.rename("data/ADE_ToRename.ics", "data/ADE_" + str(startADE) + "_" + str(stopADE) + ".ics")
    print("Creating the json file with the rooms...")
    with open("./json/rooms.json", 'wb') as f:
        for i in sorted(list(result)):
            f.write((i + '\n').encode())
    f.close()
    conn = mysql.connector.connect(
        host = "localhost",
        user = "root", #os.getenv('UserMySQL'),
        password = "", #os.getenv('PasswordMySQL'),
        database = "bdplanning", #os.getenv('DatabaseName'),
        auth_plugin='mysql_native_password'
    )
    cursor = conn.cursor()
    cursor = conn.cursor(buffered=True)
    #for each rooms in the json file we search if it exists in the database and if not we add it
    with open("./json/rooms.json", 'r', encoding='utf-8') as f:
        for line in f:
            line = line.replace("\n","")
            cursor.execute("SELECT * FROM salle WHERE nom = %s", (line,))
            if cursor.rowcount == 0:
                cursor.execute("INSERT INTO salle (nom) VALUES (%s)", (line,))
                conn.commit()   
    print("Rooms successfully saved in ./json/rooms")
    return


'''
Description : From a date with the format DD-MM-YYYY, return the number of the week in the year
Parameters : date (string) : the date with the format DD-MM-YYYY
Return : int : the number of the week in the year
'''
def getWeekNumber(date):
    return datetime.strptime(date, "%d-%m-%Y").isocalendar()[1]


'''
Description : Get the slots occupied by the events in the ics file
Parameters : timeStart (string) : the start time of the event with the format HHMMSS
             timeEnd (string) : the end time of the event with the format HHMMSS
Return : [string] : a list with the slots occupied by the event
'''
def analyze(timeStart,timeEnd):
    cren = []
    if timeStart < "094500": 
        cren = [C1]
        if timeEnd < "094500":
            return cren
        elif timeEnd < "113000":
            cren.extend([C2])
        elif timeEnd < "130000":
            cren.extend([C2,C3])
        elif timeEnd < "144500":
            cren.extend([C2,C3,C4])
        elif timeEnd < "163000":
            cren.extend([C2,C3,C4,C5])
        elif timeEnd < "181500":
            cren.extend([C2,C3,C4,C5,C6])
        else:
            cren.extend([C2,C3,C4,C5,C6,C7])
    elif timeStart < "113000":
        cren = [C2]
        if timeEnd < "113000":
            return cren
        elif timeEnd < "130000":
            cren.extend([C3])
        elif timeEnd < "144500":
            cren.extend([C3,C4])
        elif timeEnd < "163000":
            cren.extend([C3,C4,C5])
        elif timeEnd < "181500":
            cren.extend([C3,C4,C5,C6])
        else:
            cren.extend([C3,C4,C5,C6,C7])
    elif timeStart < "130000":
        cren = [C3]
        if timeEnd < "130000":
            return cren
        elif timeEnd < "144500":
            cren.extend([C4])
        elif timeEnd < "163000":
            cren.extend([C4,C5])
        elif timeEnd < "181500":
            cren.extend([C4,C5,C6])
        else:
            cren.extend([C4,C5,C6,C7])
    elif timeStart < "144500":
        cren = [C4]
        if timeEnd < "144500":
            return cren
        elif timeEnd < "163000":
            cren.extend([C5])
        elif timeEnd < "181500":
            cren.extend([C5,C6])
        else:
            cren.extend([C5,C6,C7])
    elif timeStart < "163000":
        cren = [C5]
        if timeEnd < "163000":
            return cren
        elif timeEnd < "181500":
            cren.extend([C6])
        else:
            cren.extend([C6,C7])
    elif timeStart < "181500":
        cren = [C6]
        if timeEnd < "181500":
            return cren
        elif timeEnd < "194500":
            cren.extend([C7])
    elif timeStart < "194500":
        cren = [C7]
    return cren


'''
Description : Write json files with the events and number of rooms occupied
Parameters : file (string) : the name of the ics file
             startAde (string) : the start date of the ics file with the format DD-MM-YYYY
             stopAde (string) : the stop date of the ics file with the format DD-MM-YYYY
Return : None
'''
def busyRoom(file,startADE,stopADE):
    start_time = datetime.now()

    if not os.path.exists("./json"):
        os.makedirs("./json")
    if os.path.exists("./json/JSON_name.json"):
        print("Deleting the file JSON_name.json...")
        os.remove("./json/JSON_name.json")
    if os.path.exists("./json/JSON_number.json"):
        print("Deleting the file JSON_number.json...")
        os.remove("./json/JSON_number.json")

    weekStart = getWeekNumber(startADE)
    weekStop = getWeekNumber(stopADE)

    #if the calendar is on 2 differents year
    if weekStop < weekStart :
        weekStop += 52

    #we create a dictionnary with the template of the json file (with all the slots occupied)
    dict = {}
    for week in range(weekStart-1,weekStop):
        dict[week%52+1] = {}
        for day in dayLists:
            dict[week%52+1][day] = {}
            for cren in crenLists:
                dict[week%52+1][day][cren] = []
                
    #we create a dictionnary with the template of the json file (with the number of rooms occupied)
    dict2 = {}
    for week in range(weekStart-1,weekStop):
        dict2[week%52+1] = {}
        for day in dayLists:
            dict2[week%52+1][day] = {}
            for cren in crenLists:
                dict2[week%52+1][day][cren] = 0
    
    print("Starting to read the file ics and get the busy rooms and write them in a json file...")
    g = open(file,'r', encoding = 'utf-8')
    gcal = Calendar.from_ical(g.read())
    for event in gcal.walk():
        if event.name == "VEVENT":
            room = event.get("LOCATION").split(",")
            dtstart = event.get("DTSTART").to_ical().decode("utf-8")
            dtend = event.get("DTEND").to_ical().decode("utf-8")
            #make a regex to get the date and the time in the string
            date = dtstart[0:8]
            #convert date in the format dd-mm-yyyy
            date = date[6:8] + "-" + date[4:6] + "-" + date[0:4]
            timeStart = dtstart[9:15]
            timeEnd = dtend[9:15]
            #get the week number
            week = getWeekNumber(date)
            #get the day like in dayLists
            day = dayLists[datetime.strptime(date,"%d-%m-%Y").weekday()]
            #with the start and end time, we look in which slot we are with several possible slots for example: 8:30 a.m. to 10:00 a.m. in the slot C1 and C2
            cren = analyze(timeStart,timeEnd)
            for c in cren:
                #we add the room in the list of the slot only if it is not already in the list
                if room[0] not in dict[week][day][c]:
                    dict[week][day][c].append(room[0])
                    cpt = dict2[week][day][c]
                    dict2[week][day][c] = cpt+1
    g.close()   

    print("Writing the json file with the occupied rooms...")
    with open("./json/JSON_name.json", "w") as write_file:
        json.dump(dict, write_file, indent = 4)
    write_file.close()

    print("Writing the json file with the number of occupied rooms...")
    with open("./json//JSON_number.json", "w") as write_file:
        json.dump(dict2, write_file, indent = 4)
    write_file.close()

    print("Reading and writing took : %s" % (datetime.now() - start_time))
    

#-----------------------------------#
#                                   #
#              Main                 #
#                                   #
# ----------------------------------#


'''
Description : the main function, it calls the functions getRooms and busyRoom
Parameters : update_rooms (boolean) : if True, we update the rooms.json file
             update_occupancy (boolean) : if True, we update the JSON_name.json and JSON_number.json files
Return : None
'''
def mainParser(update_rooms, update_occupancy):
    if update_rooms == "-r":
        update_rooms = True
    if update_occupancy == "-r":
        update_rooms = True
   
    start_time = datetime.now()
    print("Starting the program...")
    if update_rooms:
        getRooms(url)
    if update_occupancy:
        busyRoom("data/ADE_"+str(startADE)+"_"+str(stopADE)+".ics",startADE,stopADE)
    print("The whole program took : %s" % (datetime.now() - start_time))
