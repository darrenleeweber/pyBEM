#!/usr/bin/env python

import wx
import emse

from wxVTKRenderWindow import wxVTKRenderWindow
import vtk

class bemMainFrame(wx.Frame):
    
    def __init__(self, title, pos=wx.DefaultPosition, size=wx.DefaultSize):
        wx.Frame.__init__(self, None, -1, title, pos, size)
        menuFile = wx.Menu()
        menuFile.Append(1, "&About...")
        menuFile.AppendSeparator()
        menuFile.Append(2, "E&xit")
        menuBar = wx.MenuBar()
        menuBar.Append(menuFile, "&File")
        self.SetMenuBar(menuBar)
        self.CreateStatusBar()
        self.SetStatusText("Welcome to PyBEM!")
        self.Bind(wx.EVT_MENU, self.OnAbout, id=1)
        self.Bind(wx.EVT_MENU, self.OnQuit, id=2)
        
        #s=wx.Size(size[0],size[1])
        vtkWindow = wxVTKRenderWindow(self, wx.NewId(), stereo=1)
        
        wfr = emse.wfr()
        wfr.read('mesh_emse_mrev4_scalp.wfr')
        #wfr.view()
        
        
        # map data into a vtk actor
        wfrMapper = vtk.vtkPolyDataMapper()
        wfrMapper.SetInput(wfr.vtkSurf())
        #wfrMapper.SetInput(wfrNormals.GetOutput())
        
        wfrActor = vtk.vtkActor()
        wfrActor.SetMapper(wfrMapper)
        
        # create rendering
        ren = vtk.vtkRenderer()
        ren.SetViewport(0.0, 0.0, 1.0, 1.0)
        ren.SetBackground(0.0, 0.0, 0.0)
        ren.AddViewProp(wfrActor)
        
        vtkWindow.GetRenderWindow().AddRenderer(ren)
        ren.ResetCamera()
        
    def OnQuit(self, event):
        self.Close()
    
    def OnAbout(self, event):
        wx.MessageBox("This is a Python Program for Neuroimaging",
            "About PyBEM", wx.OK | wx.ICON_INFORMATION, self)
