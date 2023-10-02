import wx
import os
import csv
import serial
import time
import re
import configparser
from threading import Thread

class PDMSTimeEntry(wx.App):
    def __init__(self):
        super().__init__(clearSigInt=True)

        # init frame
        self.InitFrame()

    def InitFrame(self):
        frame = TimeEntry(parent=None, title="PDMS Time Entry", pos=(100,100))
        frame.Show(True)

class TimeEntry(wx.Frame):
    #Time entry frame and panel
    def __init__(self, parent, title, pos):
        wx.Frame.__init__(self, parent=parent, title=title, size=(450,350), pos=pos)
        panel = TimeEntryPanel(self)
        self.Show()
        
class TimeEntryPanel(wx.Panel):
    #Time system
    #Candidate for INI, serial information for time keeper
    def __init__(self,parent):
        wx.Panel.__init__(self,parent)
        lbEventDay = wx.StaticText(self, label="Day:", pos=(5,7))
        self.cbEventDay = wx.ComboBox(self, pos=(80,5), choices=['1','2','3'])
        lbAgeGroup = wx.StaticText(self, label="Age Group:", pos=(5,37))
        self.cbAgeGroup = wx.ComboBox(self, pos=(80,35), choices=["5-8", "9-12", "13-16", "17-30", "31+"])
        lbEvent = wx.StaticText(self, label="Event:", pos=(5,67))
        self.cbEvent = wx.ComboBox(self, pos=(80,65), choices=["Barrels", "Straight Away", "Poles", "Jackpot"])
        lbTimer = wx.StaticText(self, label="Time:", pos=(5,100))
        self.inTimer = wx.TextCtrl(self, id=wx.ID_ANY, pos=(65,100))
        buttonLoad = wx.Button(parent=self, label="Load", pos=(5,150))
        buttonLoad.Bind(event=wx.EVT_BUTTON, handler=self.onLoad)
        self.buttonPrevious = wx.Button(parent=self, label="Previous", pos=(105,150))
        self.buttonPrevious.Bind(event=wx.EVT_BUTTON, handler=self.onPrevious)
        self.buttonNext = wx.Button(parent=self, label="Next", pos=(205,150))
        self.buttonNext.Bind(event=wx.EVT_BUTTON, handler=self.onNext)
        buttonDrag = wx.Button(parent=self, label="Drag", pos=(305,150))
        buttonDrag.Bind(event=wx.EVT_BUTTON, handler=self.onDrag)
        self.lbRiderName = wx.StaticText(self, label="", pos=(350,5))
        self.lbHorseName = wx.StaticText(self, label="", pos=(350,35))
        self.lbRiderRemain = wx.StaticText(self, label="", pos=(350,65))
        self.chNoTime = wx.CheckBox(self, label="No Time", pos=(280,95))
        self.AutoEntry = wx.Button(self, label="Auto Entry", pos=(105,200))
        self.AutoEntry.Bind(event=wx.EVT_BUTTON, handler=self.TimerEvent)
        self.Cancel = wx.Button(self, label="Cancel", pos=(205,200))
        self.Cancel.Bind(event=wx.EVT_BUTTON, handler=self.onCancel)
        self.Cancel.Hide()
        self.lbRecordTime = wx.StaticText(self, label="Waiting for Timer...", pos=(5,180))
        self.lbRecordTime.Hide()

        #Variables used in Panel
        self.RiderList = []
        self.barrelstring = ""
        self.straightawaystring = ""
        self.polesstring = ""
        self.jackpotstring = ""
        self.weekstring = ""
        self.conditioncheck = ""
        self.csvfilename = ""
        self.currentplace = 0
        self.recordfilter = []
        self.recordcounter = 0
        self.tdata = ""

    def onLoad(self, event):
        self.chNoTime.SetValue(0)
        self.RiderList = []
        self.currentplace = 0
        self.inTimer.SetValue("")
        self.recordfilter = []
        with open('riderdata.csv', 'r') as csvinput:
            reader = csv.DictReader(csvinput)
            for row in reader:
                self.RiderList.append({'Number':row['Number'],'Rider':row['Rider'],'Horse':row['Horse'],'Group':row['Group'],'Buckle':row['Buckle'],
                                       'ExtraHorse':row['ExtraHorse'],'Barrels1':row['Barrels1'],'Barrels2':row['Barrels2'],'Barrels3':row['Barrels3'],
                                       'StraightAway1':row['StraightAway1'],'StraightAway2':row['StraightAway2'],'StraightAway3':row['StraightAway3'],
                                       'Poles1':row['Poles1'],'Poles2':row['Poles2'],'Poles3':row['Poles3'],'Jackpot1':row['Jackpot1'],'Jackpot2':row['Jackpot2'],
                                       'Jackpot3':row['Jackpot3']})
        lbRider = wx.StaticText(self, label="Rider:", pos=(280,5))
        lbHorse = wx.StaticText(self, label="Horse:", pos=(280,35))
        lbRemaining = wx.StaticText(self, label="Remaining:", pos=(280,65))
        if self.cbEventDay.GetValue() == "" or self.cbAgeGroup.GetValue() == "" or self.cbEvent.GetValue() == "":
            wx.MessageBox('Day, Age Group, and Event need to be selected.  Please Try Again', 'Error', wx.OK | wx.ICON_ERROR)
        else:
            firsttime = True
            self.daynumber = self.cbEventDay.GetValue()
            self.barrelstring = "Barrels" + str(self.daynumber)
            self.straightawaystring = "StraightAway" + str(self.daynumber)
            self.polesstring = "Poles" + str(self.daynumber)
            self.jackpotstring = "Jackpot" + str(self.daynumber)
            self.weekstring = "Week" + str(self.daynumber)
            if self.cbEvent.GetValue() == "Barrels":
                self.conditioncheck = self.barrelstring
                self.csvfilename = "barreltimes.csv"
            elif self.cbEvent.GetValue() == "Straight Away":
                self.conditioncheck = self.straightawaystring
                self.csvfilename = "straightawaytimes.csv"
            elif self.cbEvent.GetValue() == "Poles":
                self.conditioncheck = self.polesstring
                self.csvfilename = "polestimes.csv"
            elif self.cbEvent.GetValue() == "Jackpot":
                self.conditioncheck = self.jackpotstring
                self.csvfilename = "jackpottimes.csv"
            self.recordcounter = 0
            for rider in self.RiderList:
                if rider[self.conditioncheck] == "True" and self.cbAgeGroup.GetValue() == rider['Group']:
                    if firsttime:
                        firsttime = False
                        self.recordfilter.append(self.recordcounter)
                        self.lbRiderName.Destroy()
                        self.lbHorseName.Destroy()
                        self.lbRiderName = wx.StaticText(self, label=rider['Rider'], pos=(350,5))
                        self.lbHorseName = wx.StaticText(self, label=rider['Horse'], pos=(350,35))
                        with open(self.csvfilename, 'r') as csvinput:
                            reader = csv.DictReader(csvinput)
                            for row in reader:
                                if rider['Rider'] == row['Rider'] and rider['Horse'] == row['Horse']:
                                    self.inTimer.SetValue(row[self.weekstring])
                                    if self.inTimer.GetValue() == "999.999":
                                        self.chNoTime.SetValue(1)
                    else:
                        self.recordfilter.append(self.recordcounter)
                self.recordcounter += 1
                self.lbRiderRemain.Destroy()
                self.lbRiderRemain = wx.StaticText(self, label=str(int(len(self.recordfilter)-1)), pos=(350,65))
                self.buttonNext.Enable()
                self.buttonPrevious.Disable()

    def onPrevious(self, event):
        self.chNoTime.SetValue(0)
        if self.currentplace == 0:
            wx.MessageBox('Already at the beginning.', 'Error', wx.OK | wx.ICON_ERROR)
        else:
            self.currentplace -= 1
            self.lbRiderName.Destroy()
            self.lbHorseName.Destroy()
            self.lbRiderName = wx.StaticText(self, label=self.RiderList[self.recordfilter[self.currentplace]]['Rider'], pos=(350,5))
            self.lbHorseName = wx.StaticText(self, label=self.RiderList[self.recordfilter[self.currentplace]]['Horse'], pos=(350,35))
            existingtime = ""
            with open(self.csvfilename, 'r') as csvinput:
                reader = csv.DictReader(csvinput)
                for row in reader:
                    if row['Rider'] == self.RiderList[self.recordfilter[self.currentplace]]['Rider'] and row['Horse'] == self.RiderList[self.recordfilter[self.currentplace]]['Horse']:
                        existingtime = row[self.weekstring]
                        if existingtime == "999.999":
                            self.chNoTime.SetValue(1)
                        break
            self.inTimer.SetValue(existingtime)
            self.lbRiderRemain.Destroy()
            self.lbRiderRemain = wx.StaticText(self, label=str(int(len(self.recordfilter)-self.currentplace-1)), pos=(350,65))
            self.buttonNext.Enable()

    def onNext(self, event):
        newrider = False
        addtime = False
        oldrider = False
        self.buttonPrevious.Enable()

        try:
            timecheck = float(self.inTimer.GetValue())
        except:
            wx.MessageBox(str('Invalid time entered.'), 'Error', wx.OK | wx.ICON_ERROR)
            return
         
        with open(self.csvfilename, 'r') as csvinput:
            reader = csv.DictReader(csvinput)
            readercounter = 0
            for row in reader:
                readercounter += 1
                if row['Rider'] == self.RiderList[self.recordfilter[self.currentplace]]['Rider'] and row['Horse'] == self.RiderList[self.recordfilter[self.currentplace]]['Horse']:
                    addtime = True
                    newrider = False
                    break
                else:
                    newrider = True
                    addtime = False
        if readercounter == 0:
            newrider = True
        if newrider:
            if self.weekstring == "Week1":
                if self.chNoTime.GetValue():
                    week1value = "999.999"
                else:
                    week1value = self.inTimer.GetValue()
                week2value = ""
                week3value = ""
            elif self.weekstring == "Week2":
                week1value = ""
                if self.chNoTime.GetValue():
                    week2value = "999.999"
                else:
                    week2value = self.inTimer.GetValue()
                week3value = ""
            elif self.weekstring == "Week3":
                week1value = ""
                week2value = ""
                if self.chNoTime.GetValue():
                    week3value = "999.999"
                else:
                    week3value = self.inTimer.GetValue()
            with open(self.csvfilename, 'a') as csvappend:
                writer = csv.writer(csvappend)
                writer.writerow([self.RiderList[self.recordfilter[self.currentplace]]['Rider'],self.RiderList[self.recordfilter[self.currentplace]]['Horse'],
                                 week1value, week2value, week3value])
            newrider = False
        if addtime:
            templist = []
            with open(self.csvfilename, 'r') as csvinput:
                reader = csv.DictReader(csvinput)
                for row in reader:
                    if row['Rider'] == self.RiderList[self.recordfilter[self.currentplace]]['Rider'] and row['Horse'] == self.RiderList[self.recordfilter[self.currentplace]]['Horse']:
                        ridername = row['Rider']
                        horsename = row['Horse']
                        if self.weekstring == "Week1":
                            if self.chNoTime.GetValue():
                                week1value = "999.999"
                            else:
                                week1value = self.inTimer.GetValue()
                            week2value = row['Week2']
                            week3value = row['Week3']
                        elif self.weekstring == "Week2":
                            week1value = row['Week1']
                            if self.chNoTime.GetValue():
                                week2value = "999.999"
                            else:
                                week2value = self.inTimer.GetValue()
                            week3value = row['Week3']
                        elif self.weekstring == "Week3":
                            week1value = row['Week1']
                            week2value = row['Week2']
                            if self.chNoTime.GetValue():
                                week3value = "999.999"
                            else:
                                week3value = self.inTimer.GetValue()
                        templist.append({'Rider':ridername,'Horse':horsename,'Week1':week1value,'Week2':week2value,'Week3':week3value})
                    else:
                        templist.append({'Rider':row['Rider'],'Horse':row['Horse'],'Week1':row['Week1'],'Week2':row['Week2'],'Week3':row['Week3']})
            with open('temporary.csv', 'w') as csvoutput:
                writer = csv.writer(csvoutput)
                #This has crashed here a few times now, destroys timesheet (appears resolved in V2)
                writer.writerow(["Rider", "Horse", "Week1", "Week2", "Week3"])
                for item in templist:
                    writer.writerow([item['Rider'],item['Horse'],item['Week1'],item['Week2'],item['Week3']])
            addtime = False
            os.remove(self.csvfilename)
            os.rename('temporary.csv', self.csvfilename)
        self.currentplace += 1
        self.chNoTime.SetValue(0)        
        lasttime = self.inTimer.GetValue()
        if str(len(self.recordfilter)-self.currentplace) == "0":
            wx.MessageBox("Last rider was updated.  Move to next Group or Event", "No More", wx.OK | wx.ICON_INFORMATION)
            self.buttonNext.Disable()
        else:
            try:
                self.lbRiderName.Destroy()
                self.lbHorseName.Destroy()
                self.lbRiderRemain.Destroy()
                self.lbRiderName = wx.StaticText(self, label=self.RiderList[self.recordfilter[self.currentplace]]['Rider'], pos=(350,5))
                self.lbHorseName = wx.StaticText(self, label=self.RiderList[self.recordfilter[self.currentplace]]['Horse'], pos=(350,35))
                self.lbRiderRemain = wx.StaticText(self, label=str(int(len(self.recordfilter)-self.currentplace-1)), pos=(350,65))
                with open(self.csvfilename, 'r') as csvinput:
                    reader = csv.DictReader(csvinput)
                    for row in reader:
                        if row['Rider'] == self.RiderList[self.recordfilter[self.currentplace]]['Rider'] and row['Horse'] == self.RiderList[self.recordfilter[self.currentplace]]['Horse']:
                            oldrider = True
                            existingtime = row[self.weekstring]
                            if existingtime == "999.999":
                                self.chNoTime.SetValue(1)
            except:
                wx.MessageBox('That was the last rider. Go to the next Age Group or Event', 'Error', wx.OK | wx.ICON_ERROR)
                self.currentplace -= 1
                self.inTimer.SetValue(lasttime)
            if oldrider:
                self.inTimer.SetValue(existingtime)
            else:
                self.inTimer.SetValue("")

    def TimerEvent(self, event):
        notifythread = Thread(target = self.NotifyTimer)
        workthread = Thread(target = self.SerialTimer)
        notifythread.start()
        workthread.start()

    def NotifyTimer(self):
        self.Cancel.Show()
        self.lbRecordTime.Show()

    def onCancel(self, event):
        self.tdata = "Cancel"
        
    def onDrag(self, event):
        #important when threading issue resolved and timer can run in background
        wx.MessageBox('Stay here while the Arena is dragged.', 'Arena Drag', wx.OK | wx.ICON_INFORMATION)
        #self.inTimer.SetFocus()

    def SerialTimer(self):
        #not able to thread currently
        #Move settings to INI file
        #guessed from http://www.arenamanagementsoftware.com/Arena%20Management%20FarmTek%20Timers.pdf
        #self.lbRecordTime.Show()
        serialin = serial.Serial('COM3',1200,timeout=0,bytesize=8,parity='N',stopbits=1)
        #serialin.open()
        self.tdata = ""
        #self.chManualEntry.SetValue(False)
        #self.donevariable = False
        waitcounter = 0
        while self.tdata == "":
            #serial data is byte encoded, also contains non-important info
            self.tdata += str(serialin.read(20),'utf-8')
            time.sleep(1)
            waitcounter += 1
            print(waitcounter)
        self.tdata += str(serialin.read(20),'utf-8')
        #Need to parse this and only grab time
        print("tdata is " + self.tdata)
        pattern = re.compile('\d+\.\d+')
        searchstring = re.findall(pattern, self.tdata) or ["Error"]
        for match in searchstring:
            if match == "Error":
                wx.MessageBox(str('Timer not sending valid time.  Received ' + self.tdata), 'Error', wx.OK | wx.ICON_ERROR)
                self.Cancel.Hide()
            else:
                print(match)
        self.inTimer.SetValue(match)
        self.lbRecordTime.Hide()
        
if __name__ == "__main__":
    try:
        os.makedirs("playday-files")
    except FileExistsError:
        #directory exists so skip it
        pass
    if os.path.isfile(str(str(os.getcwd()) + "\\playday-files\\configuration.ini")):
        #Read INI file for settings
        pass
    else:
        inifile = open(str(str(os.getcwd()) + "\\playday-files\\configuration.ini"), 'w')
        inifile.close()
    try:
        configurationini = configparser.ConfigParser()
        fileini = open(str(str(os.getcwd()) + "\\playday-files\\configuration.ini"), 'r')
        configurationini.read_file(fileini)
        inidict = dict()
        sections = configurationini.sections()
        for section in sections:
            items = configurationini.items(section)
            inidict[section]=dict(items)
        print("Read the following from ini file:")
        print(inidict)
        fileini.close()
    except Exception as e:
        if hasattr(e, 'message'):
            print(e.message)
        else:
            print(e)
    #when running in standalone mode, check test data exists and move to directory
    try:
        os.chdir(str(os.getcwd()) + "\\playday-files\\TestData")
    except FileExistsError:
        pass
    
    app = PDMSTimeEntry()
    app.MainLoop()
