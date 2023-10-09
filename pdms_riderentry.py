import wx
import os
import csv
import configparser

class PDMSRiderEntry(wx.App):
    def __init__(self):
        super().__init__(clearSigInt=True)

        # init frame
        self.InitFrame()

    def InitFrame(self):
        frame = RiderEntry(parent=None, title="PDMS Rider Entry", pos=(100,100))
        frame.Show(True)

class RiderEntry(wx.Frame):
    #Frame with panel for Entering Participant details
    def __init__(self, parent, title, pos):
        wx.Frame.__init__(self, parent=parent, title=title, size=(450,360))
        panel = RiderEntryPanel(self)
        self.Show()

class RiderEntryPanel(wx.Panel):
    #For entering Rider Details
    def __init__(self,parent):
        wx.Panel.__init__(self,parent)
            
        #RiderEntry and HorseEntry are required, need to note/validate/enforce
        RiderLabel = wx.StaticText(self, id=wx.ID_ANY, label="Rider Name:", pos=(20,20))
        self.RiderEntry = wx.TextCtrl(self, id=wx.ID_ANY, pos=(100,20))
        HorseLabel = wx.StaticText(self, id=wx.ID_ANY, label="Horse Name:", pos=(20,50))
        self.HorseEntry = wx.TextCtrl(self, id=wx.ID_ANY, pos=(100,50))
        AgeGroupLabel = wx.StaticText(self, id=wx.ID_ANY, label="Age Group:", pos=(20,80))
        self.AgeGroupDDown = wx.ComboBox(self, id=wx.ID_ANY, pos=(100,80), choices=["5-8", "9-12", "13-16", "17-30", "31+"])
        BuckleLabel = wx.StaticText(self, id=wx.ID_ANY, label="Series Member?", pos=(20,110))
        self.BuckleCheckbox = wx.CheckBox(self, id=wx.ID_ANY, pos=(120,110))
        ExtraHorseLabel = wx.StaticText(self, id=wx.ID_ANY, label="Extra Horse?", pos=(20,140))
        self.ExtraHorseCheckbox = wx.CheckBox(self, id=wx.ID_ANY, pos=(120,140))
        StartingWeekLabel = wx.StaticText(self, id=wx.ID_ANY, label="Starting Week", pos=(20,170))
        self.StartingWeekDDown = wx.ComboBox(self, id=wx.ID_ANY, pos=(100,170), choices=["1", "2", "3"])
        self.StartingWeekDDown.Bind(event=wx.EVT_COMBOBOX, handler=self.ShowMoreChoices)
        self.BarrelsLabel = wx.StaticText(self, id=wx.ID_ANY, label="Barrels", pos=(20,200))
        self.BarrelsLabel.Hide()
        self.StraightAwayLabel = wx.StaticText(self, id=wx.ID_ANY, label="Straight Away", pos=(90,200))
        self.StraightAwayLabel.Hide()
        self.PolesLabel = wx.StaticText(self, id=wx.ID_ANY, label="Poles", pos=(200,200))
        self.PolesLabel.Hide()
        self.BarrelsCheckbox = wx.CheckBox(self, id=wx.ID_ANY, pos=(30,230))
        self.BarrelsCheckbox.Hide()
        self.StraightAwayCheckbox = wx.CheckBox(self, id=wx.ID_ANY, pos=(125,230))
        self.StraightAwayCheckbox.Hide()
        self.PolesCheckbox = wx.CheckBox(self, id=wx.ID_ANY, pos=(210,230))
        self.PolesCheckbox.Hide()
        self.JackpotLabel = wx.StaticText(self, id=wx.ID_ANY, label="Jackpot", pos=(20,260))
        self.JackpotLabel.Hide()
        self.JackpotCheckbox = wx.CheckBox(self, id=wx.ID_ANY, pos=(30,290))
        self.JackpotCheckbox.Hide()
        buttonAddMore = wx.Button(parent=self, label="Add", pos=(320,290))
        buttonAddMore.Bind(event=wx.EVT_BUTTON, handler=self.onAddMore)

    def ShowMoreChoices(self, event):
        self.BarrelsLabel.Show()
        self.StraightAwayLabel.Show()
        self.PolesLabel.Show()
        self.BarrelsCheckbox.Show()
        self.StraightAwayCheckbox.Show()
        self.PolesCheckbox.Show()
        self.JackpotLabel.Show()
        self.JackpotCheckbox.Show()

    def onAddMore(self, event):
        #having this Number field in the data has proven unnecessary, need to remove.
        if self.RiderEntry.GetValue() == '':
            wx.MessageBox('No Rider Name Entered', 'Error', wx.OK | wx.ICON_ERROR)
            return
        if self.HorseEntry.GetValue() == '':
            wx.MessageBox('No Horse Entered', 'Error', wx.OK | wx.ICON_ERROR)
            return
        if self.AgeGroupDDown.GetValue() == '':
            wx.MessageBox('No Age Group Chosen', 'Error', wx.OK | wx.ICON_ERROR)
            return
        RiderNumber = 0
        with open('riderdata.csv', 'r') as incsv:
            reader = csv.DictReader(incsv)
            for row in reader:
                if row['Group'] == self.AgeGroupDDown.GetValue():
                    if int(row['Number']) > RiderNumber:
                        RiderNumber = int(row['Number'])
        RiderNumber += 1
        Barrels1 = "False"
        Barrels2 = "False"
        Barrels3 = "False"
        StraightAway1 = "False"
        StraightAway2 = "False"
        StraightAway3 = "False"
        Poles1 = "False"
        Poles2 = "False"
        Poles3 = "False"
        Jackpot1 = "False"
        Jackpot2 = "False"
        Jackpot3 = "False"
        if self.StartingWeekDDown.GetValue() == "1":
            Barrels1 = self.BarrelsCheckbox.GetValue()
            StraightAway1 = self.StraightAwayCheckbox.GetValue()
            Poles1 = self.PolesCheckbox.GetValue()
            Jackpot1 = self.JackpotCheckbox.GetValue()
        elif self.StartingWeekDDown.GetValue() == "2":
            Barrels2 = self.BarrelsCheckbox.GetValue()
            StraightAway2 = self.StraightAwayCheckbox.GetValue()
            Poles2 = self.PolesCheckbox.GetValue()
            Jackpot2 = self.JackpotCheckbox.GetValue()
        elif self.StartingWeekDDown.GetValue() == "3":
            Barrels3 = self.BarrelsCheckbox.GetValue()
            StraightAway3 = self.StraightAwayCheckbox.GetValue()
            Poles3 = self.PolesCheckbox.GetValue()
            Jackpot3 = self.JackpotCheckbox.GetValue()
        else:
            #Starting Week not picked so we need to alert and break
            wx.MessageBox('Starting Week is not picked', 'Error', wx.OK | wx.ICON_ERROR)
            return
        with open('riderdata.csv', 'a') as outcsv:
            writer = csv.writer(outcsv)
            writer.writerow([RiderNumber, self.RiderEntry.GetValue(), self.HorseEntry.GetValue(), self.AgeGroupDDown.GetValue(),
                             self.BuckleCheckbox.GetValue(),self.ExtraHorseCheckbox.GetValue(), Barrels1, Barrels2, Barrels3, StraightAway1,
                             StraightAway2, StraightAway3, Poles1, Poles2, Poles3, Jackpot1, Jackpot2, Jackpot3])
        #After submitting entry, clear form for the next
        #Improvement opp, validate if data exists on close indicating that data not submitted and warn
        self.BarrelsLabel.Hide()
        self.StraightAwayLabel.Hide()
        self.PolesLabel.Hide()
        self.BarrelsCheckbox.Hide()
        self.StraightAwayCheckbox.Hide()
        self.PolesCheckbox.Hide()
        self.JackpotLabel.Hide()
        self.JackpotCheckbox.Hide()
        self.RiderEntry.SetValue('')
        self.HorseEntry.SetValue('')
        self.AgeGroupDDown.SetSelection(-1)
        self.StartingWeekDDown.SetSelection(-1)
        self.BarrelsCheckbox.SetValue(False)
        self.StraightAwayCheckbox.SetValue(False)
        self.PolesCheckbox.SetValue(False)
        self.JackpotCheckbox.SetValue(False)
        self.BuckleCheckbox.SetValue(False)
        self.ExtraHorseCheckbox.SetValue(False)

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
    
    app = PDMSRiderEntry()
    app.MainLoop()
