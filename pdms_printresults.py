import pandas as pd
import re
import os
import csv
import webbrowser

def write_data_table(pathoffile, seriesnumber,grouplist):
    #need to pass file name and path
    #need to pass week number

    eventlist = ['Barrels','StraightAway','Poles','Jackpot']
    filterstring = ''
    firstfilter = True
    for event in eventlist:
        if firstfilter:
            filterstring = 'df[(df[\'' + event + seriesnumber + '\'] == \'True\')]'
            firstfilter = False
        else:
            filterstring += ' | ' + 'df[(df[\'' + event + seriesnumber + '\'] == \'True\')]'
        
    df = pd.read_csv(str(pathoffile + "\\riderdata.csv"))
    with open('participant_list.html', 'w') as htmlout:
        htmlout.write('<html>\n')
    for group in grouplist:
        currentgroup = df[(df['Group'] == group)]
        groupframe = pd.DataFrame()
        eventgroup = currentgroup[(df[str('Barrels' + seriesnumber)] == True) |
                                  (df[str('StraightAway' + seriesnumber)] == True) |
                                  (df[str('Poles' + seriesnumber)] == True) |
                                  (df[str('Jackpot' + seriesnumber)] == True)]
        groupdict = []
        for index, row in eventgroup.iterrows():
            groupdict.append({'Rider':row['Rider'], 'Horse':row['Horse'], 'Barrels':row[str('Barrels' + seriesnumber)],
                              'StraightAway':row[str('StraightAway' + seriesnumber)], 'Poles':row[str('Poles' + seriesnumber)],
                              'Jackpot':row[str('Jackpot' + seriesnumber)]})
        groupframe = pd.DataFrame(groupdict)
        #print(groupframe.to_html(index=False,justify='left))
        with open('participant_list.html', 'a') as htmlout:
            htmlout.write('<header><h3>Riders for ' + group + '</h3>\n')
            htmlfile = groupframe.to_html(index=False,justify='left')
            for linein in htmlfile.split('\n'):
                if bool(re.search(r'\s+<td>True</td>', linein)):
                    htmlout.write('<td><input type="checkbox" checked="checked"></td>\n')
                elif bool(re.search(r'\s+<td>False</td>', linein)):
                    htmlout.write('<td><input type="checkbox"></td>\n')
                elif bool(re.search(r'<table border="1" class="dataframe">',linein)):
                    htmlout.write('<table border="1" class="dataframe" style="width:100%">\n')
                elif bool(re.search(r'\s+<th>\w+</th>', linein)):
                    htmlout.write(str(re.split('<th',linein)[0] + '<th style="width:16%"' + re.split('<th',linein)[1] + '\n'))
                else:
                    htmlout.write(linein + '\n')
    with open('participant_list.html', 'a') as htmlout:
        htmlout.write('</html>\n')
    #os.startfile(str(group + '.html'), 'print')
    webbrowser.open_new_tab('participant_list.html')

def WinnerReports(pathoffile, AgeGroup):
    serieslist = []
    EventString = ['Barrels','StraightAway','Poles']
    datafile = ''
    os.chdir(pathoffile)
    timelist = []
    seriesmax = 3
        
    riderlist = []
    with open('riderdata.csv', 'r') as riderinput:
        riderreader = csv.DictReader(riderinput)
        for row in riderreader:
            riderdict = {}
            riderappendstring = ''
            if row['Group'] == AgeGroup and row['ExtraHorse'] == "False" and row['Buckle'] == "True":
                #riderlist.append({"Rider":row['Rider'], "Horse":row['Horse']})
                riderappendstring = "Rider:" + row['Rider'] + ",Horse:" + row['Horse']
                for eventid in EventString:
                    if eventid == "Barrels":
                        datafile = "barreltimes.csv"
                    elif eventid == "StraightAway":
                        datafile = "straightawaytimes.csv"
                    elif eventid == "Poles":
                        datafile = "polestimes.csv"
                    with open(datafile, 'r') as timeinput:
                        timereader = csv.DictReader(timeinput)
                        foundit = False
                        for time in timereader:
                            if row['Rider'] == time['Rider'] and row['Horse'] == time['Horse']:
                                riderappendstring += "," + eventid + "1:" + time['Week1'] + "," + eventid + "2:" + time['Week2'] + "," + eventid + "3:" + time['Week3']
                                foundit = True
                        if foundit == False:
                            riderappendstring += "," + eventid + "1:," + eventid + "2:," + eventid + "3:"
                #riderappendstring += "}"
                riderdict = dict(e.split(':') for e in riderappendstring.split(','))
                riderlist.append(riderdict)
    print(riderlist)
    for rider in riderlist:
        if rider['Barrels1'] != '':
            rider['Barrels1'] = float(rider['Barrels1'])
        else:
            rider['Barrels1'] = 0
        if rider['Barrels2'] != '':
            rider['Barrels2'] = float(rider['Barrels2'])
        else:
            rider['Barrels2'] = 0
        if rider['Barrels3'] != '':
            rider['Barrels3'] = float(rider['Barrels3'])
        else:
            rider['Barrels3'] = 0
        if rider['StraightAway1'] != '':
            rider['StraightAway1'] = float(rider['StraightAway1'])
        else:
            rider['StraightAway1'] = 0
        if rider['StraightAway2'] != '':
            rider['StraightAway2'] = float(rider['StraightAway2'])
        else:
            rider['StraightAway2'] = 0
        if rider['StraightAway3'] != '':
            rider['StraightAway3'] = float(rider['StraightAway3'])
        else:
            rider['StraightAway3'] = 0
        if rider['Poles1'] != '':
            rider['Poles1'] = float(rider['Poles1'])
        else:
            rider['Poles1'] = 0
        if rider['Poles2'] != '':
            rider['Poles2'] = float(rider['Poles2'])
        else:
            rider['Poles2'] = 0
        if rider['Poles3'] != '':
            rider['Poles3'] = float(rider['Poles3'])
        else:
            rider['Poles3'] = 0
        
    if len(riderlist) == 0:
        riderappendstring = "Rider:No Riders,Horse:No Riders,Barrels1:0,Barrels2:0,Barrels3:0,StraightAway1:0,StraightAway2:0,StraightAway3:0,Poles1:0,Poles2:0,Poles3:0"
        riderdict = dict(e.split(':') for e in riderappendstring.split(','))
        riderlist.append(riderdict)
    for currentkey in list(riderlist[0].keys()):
        if currentkey == 'Rider':
            pass
        elif currentkey == 'Horse':
            pass                    
        else:
            riderlist.sort(key=lambda x: x[currentkey])
            recordcounter = 0
            for times in riderlist:
                if times[currentkey] == 999.999:
                    times[str(currentkey + "points")] = "0"
                elif times[currentkey] != 0:
                    eventpoints = 10 - recordcounter
                    if eventpoints < 0:
                        eventpoints = 0
                    if times[currentkey] == 0:
                        eventpoints = 0
                    times[str(currentkey + "points")] = str(eventpoints)
                    recordcounter += 1
                else:
                    times[str(currentkey + "points")] = "0"
    with open(str(AgeGroup + ' Standings.html'), 'w') as htmlout:
        htmlout.write('<html>\n')
    for event in EventString:
        templist = []
        for rider in riderlist:
            templiststring = "Rider:" + rider['Rider'] + ",Horse:" + rider['Horse']
            totalscore = 0
            for x in range(3):
                actualnumber = x + 1
                templiststring += ",Day " + str(actualnumber) + " Points:" + rider[str(event + str(actualnumber) + "points")]
                totalscore += int(rider[str(event + str(actualnumber) + "points")])
            templiststring += ",Total Score:" + str(totalscore)
            tempdict = dict(e.split(':') for e in templiststring.split(','))
            templist.append(tempdict)
        tempframe = pd.DataFrame(templist)
        #print(groupframe.to_html(index=False,justify='left))
        with open(str(AgeGroup + ' Standings.html'), 'a') as htmlout:
            if event == "Barrels":
                eventname = "Cloverleaf"
            else:
                eventname = event
            htmlout.write('<header><h3>Standings for ' + AgeGroup + " " + eventname + '</h3>\n')
            htmlfile = tempframe.to_html(index=False,justify='left')
            for linein in htmlfile.split('\n'):
                somethingtoprocess = False
                if somethingtoprocess:
                    pass
                else:
                    htmlout.write(linein + '\n')
    with open(str(AgeGroup + ' Standings.html'), 'a') as htmlout:
        htmlout.write('</html>\n')
    return(riderlist)
    
        
if __name__ == "__main__":
    pathoffile = "C:\\Users\\tony\\OneDrive\\Projects\\playday-files\\Fall 2023\\"
    weeknumber = "Week2"
    pattern = re.compile('\d+')
    seriesnumber = pattern.findall(weeknumber)
    grouplist = ['5-8','9-12','13-16','17-30','31+']
    AgeGroup = "13-16"
    WinnerReports(pathoffile,AgeGroup)
