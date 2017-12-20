#!/usr/bin/env python

import wx
from bemMainFrame import bemMainFrame

class bem(wx.App):
    
    def OnInit(self):
        frame = bemMainFrame("PyBEM")
        frame.Show()
        self.SetTopWindow(frame)
        return True

if __name__ == '__main__':
    app = bem(False)
    app.MainLoop()
