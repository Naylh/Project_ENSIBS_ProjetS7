#-----------------------------------#
#                                   #
#              Import               #
#                                   #
# ----------------------------------#    


import json
import os
import xlsxwriter
from datetime import datetime


#-----------------------------------#
#                                   #
#          Global Variables         #
#                                   #
# ----------------------------------#


thresholdRed = 0.70 #can be modified by the site
thresholdYellow = 0.50 #can be modified by the site
selectedRooms = 50 #can be modified by the site

C1="C1_8h-9h30"
C2="C2_9h45-11h15"
C3="C3_11h30-13h"
C4="C4_13h00-14h30"
C5="C5_14h45-16h15"
C6="C6_16h30-18h00"
C7="C7_18h15-19h45"

dayLists=["01-lundi","02-mardi","03-mercredi","04-jeudi","05-vendredi","06-samedi","07-dimanche"]
crenLists=[C1,C2,C3,C4,C5,C6,C7]


#-----------------------------------#
#                                   #
#            Functions              #
#                                   #
# ----------------------------------#


'''
Description : From a date with the format DD-MM-YYYY, return the number of the week in the year
Parameters : date (string) : the date with the format DD-MM-YYYY
Return : int : the number of the week in the year
'''
def getWeekNumber(date):
    return datetime.strptime(date, "%d-%m-%Y").isocalendar()[1]


'''
Description : From the json files, make an excel file with the number rooms occupied for each week, day and slot
Parameters : startADE (string) : the date of the start of the ADE with the format DD-MM-YYYY
             stopADE (string) : the date of the end of the ADE with the format DD-MM-YYYY
             JSON_number (string) : the name of the json file with the number of rooms occupied for each week, day and slot
             thresholdRed (int) : the threshold for the number of rooms occupied (to color the cells)
             thesholdYellow (int) : the threshold for the number of rooms occupied (to color the cells)
             selectedRooms (int) : the number of rooms selected by the user
Return : None
'''
def makeExcel(startADE,stopADE,JSON_number,thresholdRed,thresholdYellow,selectedRooms):
    if not os.path.exists("../excel"):
        print("Making directory excel...")
        os.makedirs("../excel")
    weekStart = getWeekNumber(startADE)
    weekStop = getWeekNumber(stopADE)
    #if there is already an excel file with the same name, we delete it
    if os.path.exists("../excel/Excel_number_"+startADE+"_"+stopADE+".xlsx"):
        print("Deleting old excel file...")
        os.remove("../excel/Excel_number_"+startADE+"_"+stopADE+".xlsx")
    print("Making excel file...")
    workbook = xlsxwriter.Workbook("../excel/Excel_Occupation_" + str(startADE) + "_" + str(stopADE) + ".xlsx")
    worksheet = workbook.add_worksheet()

    worksheet.write(0,0,"Excel représentant l'occupation des salles de l'UBS du " + str(startADE) + " au "+str(stopADE))

    #write the slots in the day
    for i in range(len(crenLists)):
        worksheet.write(i+4,0,crenLists[i])
    
    #if the calendar is on 2 differents year
    if weekStop < weekStart:
        weekStop += 52
    
    #for each week of the ADE we write the day and the week
    for i in range(weekStart-1,weekStop):
        worksheet.write(2,((i-weekStart+1)%52)*7+2,"Semaine "+str(i%52 + 1))
        worksheet.write(3,((i-weekStart+1)%52)*7+2,"Lundi")
        worksheet.write(3,((i-weekStart+1)%52)*7+3,"Mardi")
        worksheet.write(3,((i-weekStart+1)%52)*7+4,"Mercredi")
        worksheet.write(3,((i-weekStart+1)%52)*7+5,"Jeudi")
        worksheet.write(3,((i-weekStart+1)%52)*7+6,"Vendredi")
        worksheet.write(3,((i-weekStart+1)%52)*7+7,"Samedi")
        worksheet.write(3,((i-weekStart+1)%52)*7+8,"Dimanche")

    #read the json file and for the number of weeks, write the number of rooms occupied in the excel file
    with open(JSON_number) as f:
        data = json.load(f)
        #with my import i have to do like this for color the cells
        cell_format_red = workbook.add_format()
        cell_format_red.set_bg_color('red')
        cell_format_yellow = workbook.add_format()
        cell_format_yellow.set_bg_color('yellow')
        cell_format_green = workbook.add_format()
        cell_format_green.set_bg_color('green')

        #write the number of rooms occupied for each week, day and slot with the right color
        for week in range(weekStart-1,weekStop):
            for day in dayLists:
                for cren in crenLists:
                    if data[str((week%52)+1)][day][cren] > thresholdRed*selectedRooms:
                        worksheet.write(crenLists.index(cren)+4, 2+dayLists.index(day)+(week+1-weekStart)*7, data[str((week%52)+1)][day][cren], cell_format_red)
                    elif data[str((week%52)+1)][day][cren] >= thresholdYellow*selectedRooms:
                        worksheet.write(crenLists.index(cren)+4, 2+dayLists.index(day)+(week+1-weekStart)*7, data[str((week%52)+1)][day][cren], cell_format_yellow)
                    else:
                        worksheet.write(crenLists.index(cren)+4, 2+dayLists.index(day)+(week+1-weekStart)*7, data[str((week%52)+1)][day][cren], cell_format_green)
    workbook.close()


'''
Description : the main function, it calls the function makeExcel
Parameters : thresholdRed (float) : the limit to color the cells in red (it's a percentage)
             thresholdYellow (float) : the limit to color the cells in yellow (it's a percentage)
             selectedRooms (int) : the number of rooms selected by the user
Return : None
'''
def mainExcel(startADE,stopADE,thresholdRed,thresholdYellow,selectedRooms):

    thresholdRed = float(thresholdRed)
    thresholdYellow = float(thresholdYellow)
    selectedRooms = int(selectedRooms)
    if thresholdRed < 0 or thresholdRed > 1 or thresholdYellow < 0 or thresholdYellow > 1 or selectedRooms < 0:
        print("Error : the threshold must be between 0 and 1 and the number of rooms must be a positif integer")
        return

    start_time = datetime.now()
    print("Starting the program...")
    makeExcel(startADE,stopADE,"json/JSON_number_excel_"+startADE+"_"+stopADE+".json",thresholdRed,thresholdYellow,selectedRooms)
    print("The whole program took : %s" % (datetime.now() - start_time))
