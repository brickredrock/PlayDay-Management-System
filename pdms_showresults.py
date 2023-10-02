import wx
import wx.grid as grid
import os
import csv
import wx.lib.scrolledpanel
import configparser
from pdms_printresults import WinnerReports

class PDMSShowResults(wx.App):
    def __init__(self):
        super().__init__(clearSigInt=True)

        # init frame
        self.InitFrame()

    def InitFrame(self):
        frame = ShowResults(parent=None, title="PDMS Show Results", pos=(100,100))
        frame.Show(True)

class ShowResults(wx.Frame):
    #frame with panel for outputing results
    def __init__(self, parent, title, pos):
        wx.Frame.__init__(self, parent=parent, title=title, size=(1040,500), pos=pos)
        panel = ShowResultsPanel(self)
        self.Show()

class ShowResultsPanel(wx.Panel):
    def __init__(self,parent):
        wx.Panel.__init__(self,parent)
        lbAgeGroup = wx.StaticText(self, label="Age Group:", pos=(5,37))
        self.cbAgeGroup = wx.ComboBox(self, pos=(68,35), choices=["5-8", "9-12", "13-16", "17-30", "31+"])
        lbSeries = wx.StaticText(self, label="Series:", pos=(175,37))
        self.Series = wx.ComboBox(self, pos=(210,35), choices=["Week1", "Week2", "Week3"])
        buttonLoad = wx.Button(parent=self, label="Results", pos=(300,35))
        buttonLoad.Bind(event=wx.EVT_BUTTON, handler=self.DisplayWinner)
        self.SeriesBox =  wx.StaticBox(self, pos=(770,5), label="Series Standing", size=(250,105))
        self.SeriesBox.Hide()
        self.SeriesFirstPlace = wx.TextCtrl(self.SeriesBox, id=wx.ID_ANY, pos=(135,15))
        self.lbSeriesFirstPlace = wx.StaticText(self.SeriesBox, id=wx.ID_ANY, label="First Place:", pos=(5,15))
        self.SeriesSecondPlace = wx.TextCtrl(self.SeriesBox, id=wx.ID_ANY, pos=(135,45))
        self.lbSeriesSecondPlace = wx.StaticText(self.SeriesBox, id=wx.ID_ANY, label="Second Place:", pos=(5,45))
        self.SeriesThirdPlace = wx.TextCtrl(self.SeriesBox, id=wx.ID_ANY, pos=(135,75))
        self.lbSeriesThirdPlace = wx.StaticText(self.SeriesBox, id=wx.ID_ANY, label="Third Place:", pos=(5,75))
        self.SeriesBox.Hide()
        self.BarrelsBox = wx.StaticBox(self, pos=(5,270), label="Barrels", size=(250,105))
        self.BarrelsBox.Hide()
        self.StraightAwayBox = wx.StaticBox(self, pos=(260,270), label="Straight Away", size=(250,105))
        self.StraightAwayBox.Hide()
        self.PolesBox = wx.StaticBox(self, pos=(515,270), label="Poles", size=(250,105))
        self.PolesBox.Hide()
        self.JackpotBox = wx.StaticBox(self, pos=(770,270), label="Jackpot", size=(250,105))
        self.JackpotBox.Hide()
        lbBanner = wx.StaticText(self, label="Select Age Group to view results", pos=(5,5))
        self.BFirstPlace = wx.TextCtrl(self.BarrelsBox, id=wx.ID_ANY, pos=(135,15))
        lbBFirstPlace = wx.StaticText(self.BarrelsBox, id=wx.ID_ANY, label="First Place:", pos=(5,15))
        self.SFirstPlace = wx.TextCtrl(self.StraightAwayBox, id=wx.ID_ANY, pos=(135,15))
        lbSFirstPlace = wx.StaticText(self.StraightAwayBox, id=wx.ID_ANY, label="First Place:", pos=(5,15))
        self.PFirstPlace = wx.TextCtrl(self.PolesBox, id=wx.ID_ANY, pos=(135,15))
        lbPFirstPlace = wx.StaticText(self.PolesBox, id=wx.ID_ANY, label="First Place:", pos=(5,15))
        self.JFirstPlace = wx.TextCtrl(self.JackpotBox, id=wx.ID_ANY, pos=(135,15))
        lbJFirstPlace = wx.StaticText(self.JackpotBox, id=wx.ID_ANY, label="First Place:", pos=(5,15))
        self.BSecondPlace = wx.TextCtrl(self.BarrelsBox, id=wx.ID_ANY, pos=(135,45))
        lbBSecondPlace = wx.StaticText(self.BarrelsBox, id=wx.ID_ANY, label="Second Place:", pos=(5,45))
        self.SSecondPlace = wx.TextCtrl(self.StraightAwayBox, id=wx.ID_ANY, pos=(135,45))
        lbSSecondPlace = wx.StaticText(self.StraightAwayBox, id=wx.ID_ANY, label="Second Place:", pos=(5,45))
        self.PSecondPlace = wx.TextCtrl(self.PolesBox, id=wx.ID_ANY, pos=(135,45))
        lbPSecondPlace = wx.StaticText(self.PolesBox, id=wx.ID_ANY, label="Second Place:", pos=(5,45))
        #Not needed in our format
        #self.JSecondPlace = wx.TextCtrl(self.JackpotBox, id=wx.ID_ANY, pos=(135,45))
        #lbJSecondPlace = wx.StaticText(self.JackpotBox, id=wx.ID_ANY, label="Second Place:", pos=(5,45))
        self.BThirdPlace = wx.TextCtrl(self.BarrelsBox, id=wx.ID_ANY, pos=(135,75))
        lbBThirdPlace = wx.StaticText(self.BarrelsBox, id=wx.ID_ANY, label="Third Place:", pos=(5,75))
        self.SThirdPlace = wx.TextCtrl(self.StraightAwayBox, id=wx.ID_ANY, pos=(135,75))
        lbSThirdPlace = wx.StaticText(self.StraightAwayBox, id=wx.ID_ANY, label="Third Place:", pos=(5,75))
        self.PThirdPlace = wx.TextCtrl(self.PolesBox, id=wx.ID_ANY, pos=(135,75))
        lbPThirdPlace = wx.StaticText(self.PolesBox, id=wx.ID_ANY, label="Third Place:", pos=(5,75))
        #not needed in our format
        #self.JThirdPlace = wx.TextCtrl(self.JackpotBox, id=wx.ID_ANY, pos=(135,75))
        #lbJThirdPlace = wx.StaticText(self.JackpotBox, id=wx.ID_ANY, label="Third Place:", pos=(5,75))

    def DisplayWinner(self, event):
        #using Panels for each group, improvement size based on screen size
        barrelpanel = wx.lib.scrolledpanel.ScrolledPanel(self,-1, size=(250,400), pos=(5,390), style=wx.SIMPLE_BORDER)
        barrelpanel.SetupScrolling()
        barrelpanel.SetBackgroundColour('#FFFFFF')
        straightawaypanel = wx.lib.scrolledpanel.ScrolledPanel(self,-1, size=(250,400), pos=(260,390), style=wx.SIMPLE_BORDER)
        straightawaypanel.SetupScrolling()
        straightawaypanel.SetBackgroundColour('#FFFFFF')
        polespanel = wx.lib.scrolledpanel.ScrolledPanel(self,-1, size=(250,400), pos=(515,390), style=wx.SIMPLE_BORDER)
        polespanel.SetupScrolling()
        polespanel.SetBackgroundColour('#FFFFFF')
        jackpotpanel = wx.lib.scrolledpanel.ScrolledPanel(self,-1, size=(250,400), pos=(770,390), style=wx.SIMPLE_BORDER)
        jackpotpanel.SetupScrolling()
        jackpotpanel.SetBackgroundColour('#FFFFFF')
        seriespanel = wx.lib.scrolledpanel.ScrolledPanel(self,-1, size=(1000,150), pos=(5,110), style=wx.SIMPLE_BORDER)
        seriespanel.SetupScrolling()
        seriespanel.SetBackgroundColour('#FFFFFF')

        barrelscalc = self.PlaceCalculation("Barrels", self.Series.GetValue(), self.cbAgeGroup.GetValue())
        straightawaycalc = self.PlaceCalculation("StraightAway", self.Series.GetValue(), self.cbAgeGroup.GetValue())
        polescalc = self.PlaceCalculation("Poles", self.Series.GetValue(), self.cbAgeGroup.GetValue())
        jackpotcalc = self.PlaceCalculation("Jackpot", self.Series.GetValue(), self.cbAgeGroup.GetValue())
        barrelsgrid = grid.Grid(barrelpanel)
        barrelsgrid.CreateGrid(len(barrelscalc),2)
        barrelsgrid.SetColLabelValue(0, "Rider")
        barrelsgrid.SetColLabelValue(1, "Time")
        straightawaygrid = grid.Grid(straightawaypanel)
        straightawaygrid.CreateGrid(len(straightawaycalc),2)
        straightawaygrid.SetColLabelValue(0, "Rider")
        straightawaygrid.SetColLabelValue(1, "Time")
        polesgrid = grid.Grid(polespanel)
        polesgrid.CreateGrid(len(polescalc),2)
        polesgrid.SetColLabelValue(0, "Rider")
        polesgrid.SetColLabelValue(1, "Time")
        jackpotgrid = grid.Grid(jackpotpanel)
        jackpotgrid.CreateGrid(len(jackpotcalc),2)
        jackpotgrid.SetColLabelValue(0, "Rider")
        jackpotgrid.SetColLabelValue(1, "Time")

        barrelsizer = wx.BoxSizer(wx.VERTICAL)
        barrelsizer.Add(barrelsgrid, 1, wx.EXPAND)
        barrelpanel.SetSizer(barrelsizer)
        straightawaysizer = wx.BoxSizer(wx.VERTICAL)
        straightawaysizer.Add(straightawaygrid, 1, wx.EXPAND)
        straightawaypanel.SetSizer(straightawaysizer)
        polessizer = wx.BoxSizer(wx.VERTICAL)
        polessizer.Add(polesgrid, 1, wx.EXPAND)
        polespanel.SetSizer(polessizer)
        jackpotsizer = wx.BoxSizer(wx.VERTICAL)
        jackpotsizer.Add(jackpotgrid, 1, wx.EXPAND)
        jackpotpanel.SetSizer(jackpotsizer)

        self.BFirstPlace.SetValue("")
        self.BSecondPlace.SetValue("")
        self.BThirdPlace.SetValue("")
        self.SFirstPlace.SetValue("")
        self.SSecondPlace.SetValue("")
        self.SThirdPlace.SetValue("")
        self.PFirstPlace.SetValue("")
        self.PSecondPlace.SetValue("")
        self.PThirdPlace.SetValue("")
        self.JFirstPlace.SetValue("")
        seriesdict = []
        tempdict = []
        recordcounter = 0
        barrelscalc.sort(key=lambda x: x['Time'])
        for times in barrelscalc:
            barrelsgrid.SetCellValue(recordcounter,0,times['Rider'])
            barrelsgrid.SetCellValue(recordcounter,1,str(times['Time']))
            if recordcounter == 0 and times['Time'] != '999.999':
                self.BFirstPlace.SetValue(times['Rider'])
            elif recordcounter == 1 and times['Time'] != '999.999':
                self.BSecondPlace.SetValue(times['Rider'])
            elif recordcounter == 2 and times['Time'] != '999.999':
                self.BThirdPlace.SetValue(times['Rider'])
            recordcounter += 1

        recordcounter = 0
        straightawaycalc.sort(key=lambda x: x['Time'])
        for times in straightawaycalc:
            straightawaygrid.SetCellValue(recordcounter,0,times['Rider'])
            straightawaygrid.SetCellValue(recordcounter,1,str(times['Time']))
            if recordcounter == 0 and times['Time'] != '999.999':
                self.SFirstPlace.SetValue(times['Rider'])
            elif recordcounter == 1 and times['Time'] != '999.999':
                self.SSecondPlace.SetValue(times['Rider'])
            elif recordcounter == 2 and times['Time'] != '999.999':
                self.SThirdPlace.SetValue(times['Rider'])
            recordcounter += 1

        recordcounter = 0
        polescalc.sort(key=lambda x: x['Time'])
        for times in polescalc:
            polesgrid.SetCellValue(recordcounter,0,times['Rider'])
            polesgrid.SetCellValue(recordcounter,1,str(times['Time']))
            if recordcounter == 0 and times['Time'] != '999.999':
                self.PFirstPlace.SetValue(times['Rider'])
            elif recordcounter == 1 and times['Time'] != '999.999':
                self.PSecondPlace.SetValue(times['Rider'])
            elif recordcounter == 2 and times['Time'] != '999.999':
                self.PThirdPlace.SetValue(times['Rider'])
            recordcounter += 1
        recordcounter = 0

        jackpotcalc.sort(key=lambda x: x['Time'])
        for times in jackpotcalc:
            jackpotgrid.SetCellValue(recordcounter,0,times['Rider'])
            jackpotgrid.SetCellValue(recordcounter,1,str(times['Time']))
            if recordcounter == 0 and times['Time'] != '999.999':
                self.JFirstPlace.SetValue(times['Rider'])
            recordcounter += 1

        #Use this variable to define the series
        #Possible Items:
        #EventChampion - Champion for each event type
        #SingleEvent - Just a Single Play Day and no Series Winner defined
        #GrandChampion - Winner of entire series in all normal events
        seriesdefinition = "EventChampion"
        #print(seriesdict)
        #barrelseriescalc = self.SeriesCalculation("Barrels", self.cbAgeGroup.GetValue())
        #straightawayseriescalc = self.SeriesCalculation("StraightAway", self.cbAgeGroup.GetValue())
        #polesseriescalc = self.SeriesCalculation("Poles", self.cbAgeGroup.GetValue())

        if seriesdefinition == "GrandChampion":
            seriesgrid = grid.Grid(seriespanel)
            seriesgrid.CreateGrid(len(seriesdict),5)
            seriesgrid.SetColLabelValue(0, "Rider")
            seriesgrid.SetColLabelValue(1, "Barrels")
            seriesgrid.SetColLabelValue(2, "Poles")
            seriesgrid.SetColLabelValue(3, "StraightAway")
            seriesgrid.SetColLabelValue(4, "Total")
            seriessizer = wx.BoxSizer(wx.VERTICAL)
            seriessizer.Add(seriesgrid, 1, wx.EXPAND)
            seriespanel.SetSizer(seriessizer)

            seriesdict.sort(key=lambda x: x['Total'], reverse=True)

            recordcounter = 0
            for riders in seriesdict:
                seriesgrid.SetCellValue(recordcounter,0,riders['Rider'])
                seriesgrid.SetCellValue(recordcounter,1,riders['BPoints'])
                seriesgrid.SetCellValue(recordcounter,2,riders['SPoints'])
                seriesgrid.SetCellValue(recordcounter,3,riders['PPoints'])
                seriesgrid.SetCellValue(recordcounter,4,str(riders['Total']))
                if recordcounter == 0:
                    self.SeriesFirstPlace.SetValue(riders['Rider'])
                if recordcounter == 1:
                    self.SeriesSecondPlace.SetValue(riders['Rider'])
                if recordcounter == 2:
                    self.SeriesThirdPlace.SetValue(riders['Rider'])
                recordcounter += 1
            self.SeriesBox.Show()
        elif seriesdefinition == "EventChampion":
            riderlist = WinnerReports(str(os.getcwd()), self.cbAgeGroup.GetValue())
            self.SeriesBox =  wx.StaticBox(self, pos=(770,5), label="Event Reserve Champion", size=(250,105))
            SeriesBarrelsPlace = wx.TextCtrl(self.SeriesBox, id=wx.ID_ANY, pos=(135,15))
            lbSeriesBarrelsPlace = wx.StaticText(self.SeriesBox, id=wx.ID_ANY, label="Cloverleaf:", pos=(5,15))
            SeriesStraightAwayPlace = wx.TextCtrl(self.SeriesBox, id=wx.ID_ANY, pos=(135,45))
            lbSeriesStraightAwayPlace = wx.StaticText(self.SeriesBox, id=wx.ID_ANY, label="Straight Away:", pos=(5,45))
            SeriesPolesPlace = wx.TextCtrl(self.SeriesBox, id=wx.ID_ANY, pos=(135,75))
            lbSeriesPolesPlace = wx.StaticText(self.SeriesBox, id=wx.ID_ANY, label="Poles:", pos=(5,75))            
            EventSeriesBox =  wx.StaticBox(self, pos=(515,5), label="Event Grand Champion", size=(250,105))
            EventSeriesBarrelsPlace = wx.TextCtrl(EventSeriesBox, id=wx.ID_ANY, pos=(135,15))
            EventlbSeriesBarrelsPlace = wx.StaticText(EventSeriesBox, id=wx.ID_ANY, label="Cloverleaf:", pos=(5,15))
            EventSeriesStraightAwayPlace = wx.TextCtrl(EventSeriesBox, id=wx.ID_ANY, pos=(135,45))
            EventlbSeriesStraightAwayPlace = wx.StaticText(EventSeriesBox, id=wx.ID_ANY, label="Straight Away:", pos=(5,45))
            EventSeriesPolesPlace = wx.TextCtrl(EventSeriesBox, id=wx.ID_ANY, pos=(135,75))
            EventlbSeriesPolesPlace = wx.StaticText(EventSeriesBox, id=wx.ID_ANY, label="Poles:", pos=(5,75))            
            
            seriesgrid = grid.Grid(seriespanel)
            seriesgrid.CreateGrid(len(riderlist),4)
            seriesgrid.SetColLabelValue(0, "Rider")
            seriesgrid.SetColLabelValue(1, "Barrels")
            seriesgrid.SetColLabelValue(2, "StraightAway")
            seriesgrid.SetColLabelValue(3, "Poles")
            seriessizer = wx.BoxSizer(wx.VERTICAL)
            seriessizer.Add(seriesgrid, 1, wx.EXPAND)
            seriespanel.SetSizer(seriessizer)

            totalscorelist = []
            recordcounter = 0
            for riders in riderlist:
                totalscoredict = {}
                barrelstotal = int(int(riders['Barrels1points']) + int(riders['Barrels2points']) + int(riders['Barrels3points']))
                straightawaytotal = int(int(riders['StraightAway1points']) + int(riders['StraightAway2points']) + int(riders['StraightAway3points']))
                polestotal = int(int(riders['Poles1points']) + int(riders['Poles2points']) + int(riders['Poles3points']))
                seriesgrid.SetCellValue(recordcounter,0,riders['Rider'])
                seriesgrid.SetCellValue(recordcounter,1,str(barrelstotal))
                seriesgrid.SetCellValue(recordcounter,2,str(straightawaytotal))
                seriesgrid.SetCellValue(recordcounter,3,str(polestotal))
                totalscoredict = {'Rider':riders['Rider'],'BarrelsTotal':barrelstotal,'StraightAwayTotal':straightawaytotal,'PolesTotal':polestotal}
                totalscorelist.append(totalscoredict)
                recordcounter += 1

            eventlist = ['Barrels','StraightAway','Poles']
            recordcounter = 0
            for event in eventlist:
                totalscorelist.sort(key=lambda x: x[str(event + "Total")],reverse=True)
                recordcounter = 0
                for totals in totalscorelist:
                    if recordcounter == 0:
                        if event == "Barrels":
                            EventSeriesBarrelsPlace.SetValue(totals['Rider'])
                        if event == "StraightAway":
                            EventSeriesStraightAwayPlace.SetValue(totals['Rider'])
                        if event == "Poles":
                            EventSeriesPolesPlace.SetValue(totals['Rider'])
                    if recordcounter == 1:
                        #self.SeriesSecondPlace.SetValue(riders['Rider'])
                        if event == "Barrels":
                            SeriesBarrelsPlace.SetValue(totals['Rider'])
                        if event == "StraightAway":
                            SeriesStraightAwayPlace.SetValue(totals['Rider'])
                        if event == "Poles":
                            SeriesPolesPlace.SetValue(totals['Rider'])
                    #if recordcounter == 2:
                        #self.SeriesThirdPlace.SetValue(riders['Rider'])
                        #print("Third Place for " + event + " is " + totals['Rider'])
                    recordcounter += 1
            self.SeriesBox.Show()
            
        elif seriesdefinition == "SingleEvent":
            pass
        else:
            pass
        
        self.BarrelsBox.Show()
        self.StraightAwayBox.Show()
        self.PolesBox.Show()
        self.JackpotBox.Show()
        self.SeriesBox.Show()

    def SeriesCalculation(self, AgeGroup):
        serieslist = []
        EventString = ['Barrels','StraightAway','Poles']
        datafile = ''
        print(os.getcwd())
        
        for eventid in EventString:
            timelist = []
            riderlist = []
            if EventString == "Barrels":
                datafile = "barreltimes.csv"
            elif EventString == "StraightAway":
                datafile = "straightawaytimes.csv"
            elif EventString == "Poles":
                datafile = "polestimes.csv"

            with open(datafile, 'r') as timeinput:
                timereader = csv.DictReader(timeinput)
                for row in timereader:
                    timelist.append({"Rider":row['Rider'], "Horse":row['Horse'], "Week1":row['Week1'], "Week2":row['Week2'], "Week3":row['Week3']})
            with open('riderdata.csv', 'r') as riderinput:
                riderreader = csv.DictReader(riderinput)
                for row in riderreader:
                    if row['Group'] == AgeGroup:
                        if row['ExtraHorse'] == "False" and row['Buckle'] == "True":
                            riderlist.append({"Rider":row['Rider'], "Horse":row['Horse']})
            for ridertime in timelist:
                for riderdata in riderlist:
                    if riderdata['Rider'] == ridertime['Rider'] and riderdata['Horse'] == ridertime['Horse']:
                        serieslist.append({"Rider":riderdata['Rider'], "Week1":ridertime['Week1'], "Week2":ridertime['Week2'], "Week3":ridertime['Week3'],})

            serieslist.sort(key=lambda x: x['Week1'])
            recordcounter = 0
            for times in serieslist:
                eventpoints = 10 - recordcounter
                if eventpoints < 0:
                    eventpoints = 0
                times[str(eventid + "Week1")] = str(eventpoints)
                recordcounter += 1

            serieslist.sort(key=lambda x: x['Week2'])
            recordcounter = 0
            for times in serieslist:
                eventpoints = 10 - recordcounter
                if eventpoints < 0:
                    eventpoints = 0
                times[str(eventid + "Week2")] = str(eventpoints)
                recordcounter += 1

            serieslist.sort(key=lambda x: x['Week3'])
            recordcounter = 0
            for times in serieslist:
                eventpoints = 10 - recordcounter
                if eventpoints < 0:
                    eventpoints = 0
                times[str(eventid + "Week3")] = str(eventpoints)
                recordcounter += 1
            
        #return(serieslist)
        print(EventString)
        print(serieslist)
            

    def PlaceCalculation(self, EventString, SeriesString, AgeGroup):
        timelist = []
        riderlist = []
        serieslist = []
        
        if EventString == "Barrels":
            datafile = "barreltimes.csv"
        elif EventString == "StraightAway":
            datafile = "straightawaytimes.csv"
        elif EventString == "Poles":
            datafile = "polestimes.csv"
        elif EventString == "Jackpot":
            datafile = "jackpottimes.csv"

        if SeriesString == "Week1":
            seriesnumber = "1"
        elif SeriesString == "Week2":
            seriesnumber = "2"
        elif SeriesString == "Week3":
            seriesnumber = "3"

        with open(datafile, 'r') as timeinput:
            timereader = csv.DictReader(timeinput)
            for row in timereader:
                timelist.append({"Rider":row['Rider'], "Horse":row['Horse'], "Time":row[SeriesString]})
        with open('riderdata.csv', 'r') as riderinput:
            riderreader = csv.DictReader(riderinput)
            for row in riderreader:
                if row['Group'] == AgeGroup:
                    if row['ExtraHorse'] == "False":
                        riderlist.append({"Rider":row['Rider'], "Horse":row['Horse'], "Buckle":row['Buckle']})
        for ridertime in timelist:
            for riderdata in riderlist:
                if riderdata['Rider'] == ridertime['Rider'] and riderdata['Horse'] == ridertime['Horse']:
                    serieslist.append({"Rider":riderdata['Rider'], "Time":float(ridertime['Time']), "Buckle":riderdata['Buckle']})
        return(serieslist)

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
    
    app = PDMSShowResults()
    app.MainLoop()
