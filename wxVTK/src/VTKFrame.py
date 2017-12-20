
import wx
import vtk.wx
from vtk.wx.wxVTKRenderWindow import wxVTKRenderWindow
import math, os, sys
from wxPython.wx import *
#from vtkpython import *
from vtk import *


background_color = (0.3, 0.3, 0.3)
imageMagnification = 4
imageFocalDepthFrames = 1
imageAAFrames = 1

class VTKFrame(wxFrame):
  def __init__(self):
    wxFrame.__init__(self, None, -1, "VTK Window", size=wxSize(400,400))

    # create the widget
    self.widget = wxVTKRenderWindow(self,-1)
    self.ren = vtkRenderer()
    self.ren.SetBackground(background_color)
    self.widget.GetRenderWindow().AddRenderer(self.ren)
    
  def OnAbout(self, evt):
    wxMessageBox("VTK Application using wxWindows.")
  
  def OnExit(self, evt):
    self.Destroy()

  def OnActorEvent(self, sender, eventString):
    pass #print "actorEvent", eventString

  def AddActor(self,actor):
    actor.AddObserver("AnyEvent", self.OnActorEvent)
    self.ren.AddActor(actor)
    self.widget.Update()
    self.widget.Refresh()

  def SaveImage(self):
    tiffSelector = "TIFF files (*.tiff)|*.tiff|"
    dlg = wx.FileDialog(self, message="Save file as ...", defaultDir=os.getcwd(), 
            defaultFile="", wildcard=tiffSelector, style=wx.SAVE)
    if dlg.ShowModal() == wx.ID_OK:
      path = dlg.GetPath()
      self.SaveFile(path)
    dlg.Destroy()

  def SaveFile(self, filename):
    renWin = self.ren.GetRenderWindow()
    windowToImage = vtk.vtkWindowToImageFilter()
    windowToImage.SetInput(renWin)
    windowToImage.SetMagnification(imageMagnification)
    writer = vtk.vtkTIFFWriter()
    writer.SetInput(windowToImage.GetOutput())
    writer.SetFileName(filename)
    aaFrames = renWin.GetAAFrames()
    renWin.SetAAFrames(imageAAFrames)
    writer.Write()
    renWin.SetAAFrames(aaFrames)
    renWin.Render()
  
  
  def PrintCallback(self, irenStyle, event):
    iren = irenStyle.GetInteractor()
    if 't' is iren.GetKeySym():
      renWin = iren.GetRenderWindow()
      windowToImage = vtk.vtkWindowToImageFilter()
      windowToImage.SetInput(renWin)
      windowToImage.SetMagnification(imageMagnification)
      writer = vtk.vtkTIFFWriter()
      writer.SetInput(windowToImage.GetOutput())
      writer.SetFileName("image.tiff")
      aaFrames = renWin.GetAAFrames()
      renWin.SetAAFrames(imageAAFrames)
      writer.Write()
      renWin.SetAAFrames(aaFrames)
      renWin.Render()
  
    
if __name__ == "__main__":
  
  atomWindow = VTKFrame()
  
  atomWindow.Run()
  
