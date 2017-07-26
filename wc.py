from datetime import datetime, timedelta
from pytz import timezone
import pytz
import wx

def SelectTimeZone(tz='Australia/Brisbane'):
    return timezone(tz)
        
       
class MainDisplay(wx.Frame):
    def __init__(self, parent):
        wx.Frame.__init__(self, parent, title='Time')
        self.tz = SelectTimeZone()
        self.box = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(self.box)
        self.layoutSelPanel()
        self.Bind(wx.EVT_CLOSE, self.stop)
        self.Show()
        
    def layoutSelPanel(self):
        self.selPanel = wx.Panel(self, size=(-1,self.GetSize().width))
        self.timer = wx.Timer(self)
        self.timer.Start(100)
        self.Bind(wx.EVT_TIMER, self.update, self.timer)
        self.test = wx.ListBox(self.selPanel, choices=pytz.common_timezones)
        self.txtSelTime = wx.TextCtrl(self.selPanel, style=wx.TE_PROCESS_ENTER)
        self.lblCurrentTime = wx.StaticText(self.selPanel, label=datetime.now(SelectTimeZone()).strftime(fmt))
        self.txtSelTime.Bind(wx.EVT_TEXT_ENTER, self.confirmed, self.txtSelTime)
        self.gb = wx.GridBagSizer(5,5)
        self.gb.Add(self.txtSelTime, pos=(0,1))
        self.gb.Add(self.lblCurrentTime, pos=(1,1))
        self.gb.Add(self.test, pos=(0,2))
        self.selPanel.SetSizer(self.gb)
        self.box.Add(self.selPanel, 2, wx.EXPAND)
        
    def stop(self, e):
        if self.timer.IsRunning():
            self.timer.Stop()
            print('timer stopped')
            e.Skip()
        
    def confirmed(self, e):
        if self.txtSelTime.GetValue() in pytz.all_timezones_set:
            self.tz = SelectTimeZone(self.txtSelTime.GetValue())
        else:
            self.Info(self, "For a list of timezones visit - https://en.wikipedia.org/wiki/List_of_tz_database_time_zones", "Timezones")
        
    def Info(self, parent, message, caption = 'Insert program title'):
        dlg = wx.MessageDialog(parent, message, caption, wx.OK | wx.ICON_INFORMATION)
        dlg.ShowModal()
        dlg.Destroy()
    
    def update(self, e):
        self.lblCurrentTime.SetLabel(datetime.now(self.tz).strftime(fmt))


if __name__ == '__main__':
    root = wx.App(False)
    fmt = '%H:%M:%S %Z%z'
    frame = MainDisplay(None)
    root.MainLoop()