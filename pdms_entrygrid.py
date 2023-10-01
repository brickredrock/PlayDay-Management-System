import wx
import wx.grid as grid
import os
import csv
import wx.lib.scrolledpanel
import configparser
from pdms_printresults import write_data_table

class PDMSEntryGrid(wx.App):
    def __init__(self):
        super().__init__(clearSigInt=True)

        # init frame
        self.InitFrame()

    def InitFrame(self):
        frame = EntryGrid(parent=None, title="PDMS Participants", pos=(100,100))
        frame.Show(True)

class EntryGrid(wx.Frame):
    #frame with panel detailing participants using the riderdata.csv file
    def __init__(self, parent, title, pos):
        wx.Frame.__init__(self, parent=parent, title=title, size=(450,350))
        panel = EntryGridPanel(self)
        self.Show()

class EntryGridPanel(wx.Panel):
    #Improvement opp, allow data to be writting or additional riders to be added?  Correct Name spelling?
    def __init__(self,parent):
        wx.Panel.__init__(self,parent)
        self.recordcounter = 0
        self.filtercounter = 0
        with open('riderdata.csv', 'r') as csvinput:
            reader = csv.DictReader(csvinput)
            for row in reader:
                self.recordcounter +=1

        panel2 = wx.lib.scrolledpanel.ScrolledPanel(self,-1, size=(1200,800), pos=(0,50), style=wx.SIMPLE_BORDER)
        panel2.SetupScrolling()
        panel2.SetBackgroundColour('#FFFFFF')

        self.entrygrid = grid.Grid(panel2)
        self.entrygrid.CreateGrid(self.recordcounter,9)
        self.entrygrid.SetColLabelValue(0, "Number")
        self.entrygrid.SetColLabelValue(1, "Rider")
        self.entrygrid.SetColLabelValue(2, "Horse")
        self.entrygrid.SetColLabelValue(3, "Buckle")
        self.entrygrid.SetColLabelValue(4, "Extra Horse")
        self.entrygrid.SetColLabelValue(5, "Barrels")
        self.entrygrid.SetColLabelValue(6, "Straight Aways")
        self.entrygrid.SetColLabelValue(7, "Poles")
        self.entrygrid.SetColLabelValue(8, "Jackpot")

        #sets fields to display checkboxes
        attr = grid.GridCellAttr()
        attr.SetEditor(grid.GridCellBoolEditor())
        attr.SetRenderer(grid.GridCellBoolRenderer())
        self.entrygrid.SetColAttr(3,attr)
        self.entrygrid.SetColAttr(4,attr.Clone())
        self.entrygrid.SetColAttr(5,attr.Clone())
        self.entrygrid.SetColAttr(6,attr.Clone())
        self.entrygrid.SetColAttr(7,attr.Clone())
        self.entrygrid.SetColAttr(8,attr.Clone())

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.entrygrid, 1, wx.EXPAND)
        panel2.SetSizer(sizer)

        buttonSave = wx.Button(parent=self, label="Save", pos=(20,5))
        buttonSave.Bind(event=wx.EVT_BUTTON, handler=self.onSave)
        buttonRefresh = wx.Button(parent=self, label="Refresh", pos=(100,5))
        buttonRefresh.Bind(event=wx.EVT_BUTTON, handler=self.onRefresh)
        buttonMove = wx.Button(parent=self,label="Move", pos=(180,5))
        buttonMove.Bind(event=wx.EVT_BUTTON, handler=self.onMove)
        lbEventDay = wx.StaticText(self, label="Day:", pos=(370,7))
        self.cbEventDay = wx.ComboBox(self, pos=(400,5), choices=['1','2','3'])
        self.cbEventDay.Bind(event=wx.EVT_COMBOBOX, handler=self.onRefresh)
        AgeGroupLabel = wx.StaticText(self, id=wx.ID_ANY, label="Age Group:", pos=(450,7))
        self.AgeGroupDDown = wx.ComboBox(self, id=wx.ID_ANY, pos=(515,5), choices=["5-8", "9-12", "13-16", "17-30", "31+"])
        self.AgeGroupDDown.Bind(event=wx.EVT_COMBOBOX, handler=self.onRefresh)
        buttonPrint = wx.Button(parent=self,label="Print", pos=(260,5))
        buttonPrint.Bind(event=wx.EVT_BUTTON, handler=self.onPrint)
                
        self.RiderList = []
        self.FilterList = []

    def onPrint(self,event):
        AgeGroupList = ["5-8", "9-12", "13-16", "17-30", "31+"]
        print(os.getcwd())
        write_data_table(str(os.getcwd()), str(self.cbEventDay.GetValue()), AgeGroupList)
        #EventList = ["Barrels", "StraightAway", "Poles", "Jackpot"]

        #switch this to groups with list of events inside
        #Grid style with checkboxes?
        #for Event in EventList:
            #fileopen = open(str(Event + ".txt"), "w")
            #fileopen.close()
            #for AgeGroup in AgeGroupList:
                #with open(str(Event + ".txt"), "a") as text_file:
                    #text_file.write("\n\nAge Group " + AgeGroup + "\n")
                #for rider in self.RiderList:
                    #if rider[str(Event + self.cbEventDay.GetValue())] == "True" and rider['Group'] == AgeGroup:
                        #with open(str(Event + ".txt"), "a") as text_file:
                            #text_file.write(str(rider['Rider'] + " riding " + rider['Horse'] + "\n"))
        
    def onMove(self,event):
        #currently just moves to the end of the group.  Allow moving to specific spot?  Good use for number field?
        templist = []
        mover =()
        if self.FilterList == []:
            wx.MessageBox('Age Group is Not Selected', 'Error', wx.OK | wx.ICON_ERROR)
        else:
            dlg = wx.TextEntryDialog(None, "Enter the number you want to move to the end", "Move Rider to End")
            if dlg.ShowModal() == wx.ID_OK:
                ridernumber = dlg.GetValue()
            dlg.Destroy()
        if int(ridernumber):
            for row in self.RiderList:
                if self.entrygrid.GetCellValue(int(int(ridernumber)-1),1) == row['Rider'] and self.entrygrid.GetCellValue(int(int(ridernumber)-1),2) == row['Horse']:
                    mover = row
                    continue
                else:
                    templist.append({'Number':row['Number'],'Rider':row['Rider'],'Horse':row['Horse'],'Group':row['Group'],'Buckle':row['Buckle'],
                                     'ExtraHorse':row['ExtraHorse'],'Barrels1':row['Barrels1'],'Barrels2':row['Barrels2'],'Barrels3':row['Barrels3'],
                                     'StraightAway1':row['StraightAway1'],'StraightAway2':row['StraightAway2'],'StraightAway3':row['StraightAway3'],
                                     'Poles1':row['Poles1'],'Poles2':row['Poles2'],'Poles3':row['Poles3'],'Jackpot1':row['Jackpot1'],'Jackpot2':row['Jackpot2'],
                                     'Jackpot3':row['Jackpot3']})
            templist.append(mover)
            self.RiderList = templist
            os.remove("riderdata.csv")
            with open('riderdata.csv', 'w') as csvoutput:
                writer = csv.writer(csvoutput)
                writer.writerow(["Number", "Rider", "Horse", "Group", "Buckle", "ExtraHorse", "Barrels1", "Barrels2", "Barrels3", "StraightAway1",
                                 "StraightAway2", "StraightAway3", "Poles1", "Poles2", "Poles3", "Jackpot1", "Jackpot2", "Jackpot3"])
                for rider in self.RiderList:
                    writer.writerow([rider["Number"], rider["Rider"], rider["Horse"], rider["Group"], rider["Buckle"], rider["ExtraHorse"], rider["Barrels1"],
                                     rider["Barrels2"], rider["Barrels3"], rider["StraightAway1"], rider["StraightAway2"], rider["StraightAway3"],
                                     rider["Poles1"], rider["Poles2"], rider["Poles3"], rider["Jackpot1"], rider["Jackpot2"], rider["Jackpot3"]])

        else:
            wx.MessageBox('You must enter a number', 'Error', wx.OK | wx.ICON_ERROR)
        self.onRefresh(wx.EVT_BUTTON)
            
    def onSave(self, event):
        #Warn if changes not saved?
        self.entrygrid.GoToCell(0,0)
        daynumber = self.cbEventDay.GetValue()
        barrelstring = "Barrels" + str(daynumber)
        straightawaystring = "StraightAway" + str(daynumber)
        polesstring = "Poles" + str(daynumber)
        jackpotstring = "Jackpot" + str(daynumber)
        savecounter = 0
        if self.AgeGroupDDown.GetValue() == "":
            savecounter = self.recordcounter
        else:
            savecounter = self.filtercounter
        for x in range(savecounter):
            for rider in self.RiderList:
                if self.entrygrid.GetCellValue(x,1) == rider['Rider'] and self.entrygrid.GetCellValue(x,2) == rider['Horse']:
                    if self.entrygrid.GetCellValue(x,3) == "1":
                        rider['Buckle'] = "True"
                    else:
                        rider['Buckle'] = "False"
                    if self.entrygrid.GetCellValue(x,4) == "1":
                        rider['ExtraHorse'] = "True"
                    else:
                        rider['ExtraHorse'] = "False"
                    if self.entrygrid.GetCellValue(x,5) == "1":
                        rider[barrelstring] = "True"
                    else:
                        rider[barrelstring] = "False"
                    if self.entrygrid.GetCellValue(x,6) == "1":
                        rider[straightawaystring] = "True"
                    else:
                        rider[straightawaystring] = "False"
                    if self.entrygrid.GetCellValue(x,7) == "1":
                        rider[polesstring] = "True"
                    else:
                        rider[polesstring] = "False"
                    if self.entrygrid.GetCellValue(x,8) == "1":
                        rider[jackpotstring] = "True"
                    else:
                        rider[jackpotstring] = "False"
        os.remove("riderdata.csv")
        with open('riderdata.csv', 'w') as csvoutput:
            writer = csv.writer(csvoutput)
            writer.writerow(["Number", "Rider", "Horse", "Group", "Buckle", "ExtraHorse", "Barrels1", "Barrels2", "Barrels3", "StraightAway1",
                             "StraightAway2", "StraightAway3", "Poles1", "Poles2", "Poles3", "Jackpot1", "Jackpot2", "Jackpot3"])
            for rider in self.RiderList:
                writer.writerow([rider["Number"], rider["Rider"], rider["Horse"], rider["Group"], rider["Buckle"], rider["ExtraHorse"], rider["Barrels1"],
                                 rider["Barrels2"], rider["Barrels3"], rider["StraightAway1"], rider["StraightAway2"], rider["StraightAway3"],
                                 rider["Poles1"], rider["Poles2"], rider["Poles3"], rider["Jackpot1"], rider["Jackpot2"], rider["Jackpot3"]])
            
            
            

    def onRefresh(self, event):
        #called by picking group and series.
        self.RiderList = []
        self.FilterList = []
        recordcounter = 0
        self.filtercounter = 0
        self.entrygrid.ClearGrid()
        daynumber = self.cbEventDay.GetValue()
        barrelstring = "Barrels" + str(daynumber)
        straightawaystring = "StraightAway" + str(daynumber)
        polesstring = "Poles" + str(daynumber)
        jackpotstring = "Jackpot" + str(daynumber)
        with open('riderdata.csv', 'r') as csvinput:
            reader = csv.DictReader(csvinput)
            for row in reader:
                self.RiderList.append({'Number':row['Number'],'Rider':row['Rider'],'Horse':row['Horse'],'Group':row['Group'],'Buckle':row['Buckle'],
                                       'ExtraHorse':row['ExtraHorse'],'Barrels1':row['Barrels1'],'Barrels2':row['Barrels2'],'Barrels3':row['Barrels3'],
                                       'StraightAway1':row['StraightAway1'],'StraightAway2':row['StraightAway2'],'StraightAway3':row['StraightAway3'],
                                       'Poles1':row['Poles1'],'Poles2':row['Poles2'],'Poles3':row['Poles3'],'Jackpot1':row['Jackpot1'],'Jackpot2':row['Jackpot2'],
                                       'Jackpot3':row['Jackpot3']})
        for record in self.RiderList:
            if self.AgeGroupDDown.GetValue() == "":
                #if not filtering, pass through and grab all.
                pass
            else:
                if record['Group'] == self.AgeGroupDDown.GetValue():
                    #pass to collect what is filtered for
                    self.filtercounter += 1
                    self.FilterList.append({'Number':record['Number'],'Rider':record['Rider'],'Horse':record['Horse'],'Group':record['Group'],'Buckle':record['Buckle'],
                                            'ExtraHorse':record['ExtraHorse'],'Barrels1':record['Barrels1'],'Barrels2':record['Barrels2'],'Barrels3':record['Barrels3'],
                                            'StraightAway1':record['StraightAway1'],'StraightAway2':record['StraightAway2'],'StraightAway3':record['StraightAway3'],
                                            'Poles1':record['Poles1'],'Poles2':record['Poles2'],'Poles3':record['Poles3'],'Jackpot1':record['Jackpot1'],
                                            'Jackpot2':record['Jackpot2'],'Jackpot3':record['Jackpot3']})
                    pass
                else:
                    #skip this one and continue to next
                    continue
            self.entrygrid.SetCellValue(recordcounter,0,record['Number'])
            self.entrygrid.SetCellValue(recordcounter,1,record['Rider'])
            self.entrygrid.SetCellValue(recordcounter,2,record['Horse'])
            #WX uses 1 for True
            if record['Buckle'] == "True":
                buckleentry = "1"
            else:
                buckleentry = ""
            self.entrygrid.SetCellValue(recordcounter,3,buckleentry)
            if record['ExtraHorse'] == "True":
                extrahorseentry = "1"
            else:
                extrahorseentry = ""
            self.entrygrid.SetCellValue(recordcounter,4,extrahorseentry)
            if record[barrelstring] == "True":
                barrelentry = "1"
            else:
                barrelentry = ""
            self.entrygrid.SetCellValue(recordcounter,5,barrelentry)
            if record[straightawaystring] == "True":
                straightawayentry = "1"
            else:
                straightawayentry = ""
            self.entrygrid.SetCellValue(recordcounter,6,straightawayentry)
            if record[polesstring] == "True":
                polesentry = "1"
            else:
                polesentry = ""
            self.entrygrid.SetCellValue(recordcounter,7,polesentry)
            if record[jackpotstring] == "True":
                jackpotentry = "1"
            else:
                jackpotentry = ""
            self.entrygrid.SetCellValue(recordcounter,8,jackpotentry)
            recordcounter += 1
        
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
    
    app = PDMSEntryGrid()
    app.MainLoop()
