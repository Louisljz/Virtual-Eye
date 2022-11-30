from pywinauto import Desktop
import uiautomation as auto


class Screen_Monitor():

    def __init__(self):
        self.browser_names=[['MozillaWindowClass', 'Firefox'], ['Chrome_WidgetWin_1', 'Edge'], ['Chrome_WidgetWin_1', 'Google Chrome']]
        self.Browserdetails = []
        self.SUS_Apps = []
        self.all_processes = []
        self.getprocess()
        self.browser_details()
        self.screen_monitor()


    def getprocess(self):
        windows = Desktop(backend="uia").windows()
        for w in windows:
            if w.window_text() !="Taskbar" and w.window_text() !="Program Manager" and w.window_text() !="Task Switcher":
                self.SUS_Apps.append(w.window_text())

    def browser_details(self):
        for i in self.SUS_Apps:
            for a in range(len(self.browser_names)):
                if self.browser_names[a][1] in i:
                    self.SUS_Apps[self.SUS_Apps.index(i)]=self.browser_names[a][1]
                    detailed_window = auto.Control(searchDepth=1, ClassName=self.browser_names[a][0], SubName=self.browser_names[a][1])
                    self.Browserdetails.append(detailed_window)
        for i in self.SUS_Apps:
            self.all_processes.append(i)

    def screen_monitor(self):
        Active_Tabs=[]
        for i in range(len(self.Browserdetails)):
            try:
                for control, depth in auto.WalkControl(self.Browserdetails[i]):
                    if isinstance(control, auto.TabItemControl):
                        if control.ClassName== "" or control.ClassName== "Tab":
                            Active_Tabs.append(control.Name)
            except:
                pass
        if Active_Tabs:
            self.all_processes.append({"Browser Tabs: " : Active_Tabs})
