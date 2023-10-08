import wx
import os
import configparser
from os.path import exists
import csv
#Other application imports
import pdms_showresults
import pdms_timeentry
import pdms_entrygrid
import pdms_riderentry

class PlayDayApp(wx.App):
    def __init__(self):
        super().__init__(clearSigInt=True)

        # init frame
        self.InitFrame()

    def InitFrame(self):
        frame = MainFrame(parent=None, title="PlayDay Program", pos=(100,100))
        frame.Show(True)

class FileMenu (wx.Menu):
    def __init__(self, parentFrame):
        super().__init__()
        self.OnInit()
        self.parentFrame = parentFrame

    def OnInit(self):
        newSeries = wx.MenuItem(parentMenu=self, id=wx.ID_ANY, text="&New\tCtrl+N", kind=wx.ITEM_NORMAL)
        self.Append(newSeries)
        self.Bind(wx.EVT_MENU, handler=MainPanel.onNew, source=newSeries)

        openSeries = wx.MenuItem(parentMenu=self, id=wx.ID_ANY, text='&Open\tCtrl+O', kind=wx.ITEM_NORMAL)
        self.Append(openSeries)
        self.Bind(wx.EVT_MENU, handler=MainPanel.onExisting, source=openSeries)

        self.AppendSeparator() 
        
        settingsItem = wx.MenuItem(parentMenu=self, id=wx.ID_ANY, text='Settings', kind=wx.ITEM_NORMAL)
        self.Append(settingsItem)
        self.Bind(wx.EVT_MENU, handler=self.onSettings, source=settingsItem)

        self.AppendSeparator() 

        quitItem = wx.MenuItem(parentMenu=self, id=wx.ID_EXIT, text='&Quit\tCtrl+Q') 
        self.Append(quitItem)
        self.Bind(event=wx.EVT_MENU, handler=self.onQuit, source=quitItem)

    def onQuit(self, event):
        self.parentFrame.Close()

    def onSettings(self, event):
        pass
   
class MainFrame(wx.Frame):
    #start window
    def __init__(self, parent, title, pos):
        super().__init__(parent=parent, title=title, pos=pos, size=(450,300))
        self.OnInit()
        
    def OnInit(self):
        panel = MainPanel(parent=self)
        menuBar = wx.MenuBar()

        fileMenu = FileMenu(parentFrame=self)
        menuBar.Append(fileMenu, '&File')

        self.SetMenuBar(menuBar)
        
class MainPanel(wx.Panel):
    def __init__(self,parent):
        #Improvement opp, define what events are in a playday
        #reward structure as well, overall series champions, event champions
        super().__init__(parent=parent)
        self.frame_number = 1

        # Start Message of Panel
        starttext = "Welcome to the Play Day Scoring System"
        self.welcomeText = wx.StaticText(self, id=wx.ID_ANY, label=starttext, pos=(20,20))

        #The two buttons shown first until a Series is defined
        self.buttonNew = wx.Button(parent=self, label="New Series", pos=(20,80))
        self.buttonNew.Bind(event=wx.EVT_BUTTON, handler=self.onNew)
        self.buttonExisting = wx.Button(parent=self, label="Existing Series", pos=(120,80))
        self.buttonExisting.Bind(event=wx.EVT_BUTTON, handler=self.onExisting)

        #buttons shown after selecting or creating series
        self.buttonRiderEntry = wx.Button(parent=self, label="Rider Entry", pos=(20,80))
        self.buttonRiderEntry.Bind(event=wx.EVT_BUTTON, handler=self.onRiderEntry)
        self.buttonRiderEntry.Hide()
        self.buttonEntryGrid = wx.Button(parent=self, label="Participants", pos=(120,80))
        self.buttonEntryGrid.Bind(event=wx.EVT_BUTTON, handler=self.onEntryGrid)
        self.buttonEntryGrid.Hide()
        self.buttonTimeKeeper = wx.Button(parent=self, label="Time Keeper", pos=(220,80))
        self.buttonTimeKeeper.Bind(event=wx.EVT_BUTTON, handler=self.onTimeKeeper)
        self.buttonTimeKeeper.Hide()
        self.buttonShowResults = wx.Button(parent=self, label="Show Results", pos=(320,80))
        self.buttonShowResults.Bind(event=wx.EVT_BUTTON, handler=self.onShowResults)
        self.buttonShowResults.Hide()        

    def onNew(self, event):
        dlg = wx.TextEntryDialog(None, "Enter the Season and Year (example, Fall 2023)", "Create New Season")
        if dlg.ShowModal() == wx.ID_OK:
            seriesname = dlg.GetValue()
            #Candidate for INI file
            newfiledirectory = str(os.getcwd()) + "\\playday-files\\" + dlg.GetValue()
        try:
            os.makedirs(newfiledirectory)
        except:
            print("Invalid Directory, may already exist")
        dlg.Destroy()
        # Create data files
        # update panel with Label for Series Name
        os.chdir(newfiledirectory)
        with open('riderdata.csv', 'w') as outcsv:
            writer = csv.writer(outcsv)
            writer.writerow(["Number", "Rider", "Horse", "Group", "Buckle", "ExtraHorse", "Barrels1", "Barrels2", "Barrels3", "StraightAway1",
                             "StraightAway2", "StraightAway3", "Poles1", "Poles2", "Poles3", "Jackpot1", "Jackpot2", "Jackpot3"])
        with open('barreltimes.csv', 'w') as outcsv:
            writer = csv.writer(outcsv)
            writer.writerow(["Rider", "Horse", "Week1", "Week2", "Week3"])
        with open('straightawaytimes.csv', 'w') as outcsv:
            writer = csv.writer(outcsv)
            writer.writerow(["Rider", "Horse", "Week1", "Week2", "Week3"])
        with open('polestimes.csv', 'w') as outcsv:
            writer = csv.writer(outcsv)
            writer.writerow(["Rider", "Horse", "Week1", "Week2", "Week3"])
        with open('jackpottimes.csv', 'w') as outcsv:
            writer = csv.writer(outcsv)
            writer.writerow(["Rider", "Horse", "Week1", "Week2", "Week3"])
        self.PlayDayPicked(seriesname)

    def onExisting(self, event):
        #Candidate for INI file. Create menu for picking other series or new
        CurrentPath = str(os.getcwd()) + "\playday-files"
        dlg = wx.DirDialog(None, "Choose Series Folder", defaultPath=CurrentPath, style=wx.DD_DEFAULT_STYLE | wx.DD_DIR_MUST_EXIST)
        if dlg.ShowModal() == wx.ID_OK:
            #dlg.SetPath(self,CurrentPath)
            WorkingPath = dlg.GetPath()
            seriesname = WorkingPath.split("\\")[-1]
            if exists(str(WorkingPath + "\\riderdata.csv")) and exists(str(WorkingPath + "\\barreltimes.csv")) and exists(str(WorkingPath + "\\straightawaytimes.csv")) and exists(str(WorkingPath + "\\polestimes.csv")) and exists(str(WorkingPath + "\\jackpottimes.csv")):
                os.chdir(WorkingPath)
            else:
                wx.MessageBox('Data Files Not Found.  Directory may be corrupted', 'Error', wx.OK | wx.ICON_ERROR)
        dlg.Destroy()
        self.PlayDayPicked(seriesname)

    def PlayDayPicked(self, seriesname):
        #After series set, change the window.
        self.buttonNew.Destroy()
        self.buttonExisting.Destroy()
        updatedbanner = "You are working with the " + seriesname + " Play Day"
        self.welcomeText.Destroy()
        textbanner = wx.StaticText(self, id=wx.ID_ANY, label=updatedbanner, pos=(20,20))
        self.buttonRiderEntry.Show()
        self.buttonEntryGrid.Show()
        self.buttonTimeKeeper.Show()
        self.buttonShowResults.Show()
    #improvement opp, need better way to switch/update windows, I think this frame_number needs to be decremented on_close
    def onRiderEntry(self, event):
        RiderEntry = pdms_riderentry.PDMSRiderEntry()
        RiderEntry.MainLoop()
        
    def onEntryGrid(self, event):
        EntryGrid = pdms_entrygrid.PDMSEntryGrid()
        EntryGrid.MainLoop()

    def onTimeKeeper(self, event):
        TimeEntry = pdms_timeentry.PDMSTimeEntry()
        TimeEntry.MainLoop()

    def onShowResults(self, event):
        ShowResults = pdms_showresults.PDMSShowResults()
        ShowResults.MainLoop()

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
    app = PlayDayApp()
    app.MainLoop()
