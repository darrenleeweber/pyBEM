# python planes8.py -c camera.pickle
# Hit "b" to save a camera position into a file called camera.pickle
# Hit "t" to save an image.

import vtk
import wx
import cmath
import pickle
import os
import math
import sys
import getopt

from Backdrop import Backdrop
from ParametricSurface import ParametricSurface
from LineTube import LineTube

from VTKFrame import VTKFrame
from PropertyWxMediator import PropertyWxMediator
from DynamicDialog import DynamicDialog
from Properties import *

def ParametricUp(t):
  return [t, cmath.asinh(t).real, 2]

def ParametricDown(t):
  return [t, cmath.asinh(-t).real, -2]

class AppMenu:
  def __init__(self, frame, app, pipeline):
    self.frame = frame
    self.app = app
    menuFile = wx.Menu()
    saveId = wx.NewId()
    menuFile.Append( saveId, "&Save settings")
    frame.Bind(wx.EVT_MENU, self.OnSave, id=saveId)
    imageId = wx.NewId()
    menuFile.Append( imageId, "&Save image")
    frame.Bind(wx.EVT_MENU, self.OnImage, id=imageId)
    aboutId = wx.NewId()
    menuFile.Append( aboutId, "&About...")
    frame.Bind(wx.EVT_MENU, self.OnAbout, id=aboutId)
    exitId = wx.NewId()
    menuFile.Append( exitId, "E&xit")
    frame.Bind(wx.EVT_MENU, self.OnExit, id=exitId)
    
    menuBar = wx.MenuBar()
    menuBar.Append(menuFile, "&File")
    
    menuDynamic = wx.Menu()
    self.idToActor = {}
    for pipe in pipeline:
      twistId = wx.NewId()
      menuDynamic.Append( twistId, pipe.Name)
      frame.Bind(wx.EVT_MENU, self.OnDynamicMenu, id=twistId)
      self.idToActor[twistId] = pipe

    menuBar.Append(menuDynamic, "Actors")
    
    frame.SetMenuBar(menuBar)

  def OnSave(self, evt):
    self.app.SaveProperties()
    
  def OnImage(self, evt):
    self.app.SaveImage()
    
  def OnAbout(self, evt):
    wx.MessageBox("VTK Application using wxWindows.")
  
  def OnExit(self, evt):
    self.frame.Destroy()

  def OnDynamicMenu(self, evt):
    if self.idToActor.has_key(evt.GetId()):
      actor = self.idToActor[evt.GetId()]
      props = actor.Properties
      dialog = DynamicDialog(PropertyWxMediator(props), self.frame, -1,
                             "%s properties" % (actor.Name))
      dialog.Show()
    else:
      print "Dialog box not found"

    
class App(wx.App):

  def OnInit(self):
    'Create the main window and insert the custom frame'
    domain = [ -5, 5, .1 ]
    backdrop = Backdrop(((-6, -4, -2), (6, 4, 2)))
    self.twist = ParametricSurface(domain, ParametricUp, ParametricDown)
    upTube = LineTube(ParametricUp, domain)
    downTube = LineTube(ParametricDown, domain)
    self.twist.Name = "twist surface"
    upTube.Name = "up tube"
    downTube.Name = "down tube"
    self.pipelines = [self.twist, upTube, downTube]
    self.LoadProperties()
    window = VTKFrame()
    appMenu = AppMenu(window, self, self.pipelines)
    window.AddActor(self.twist.GetActor())
    window.AddActor(upTube.GetActor())
    window.AddActor(downTube.GetActor())
    backActors = backdrop.GetActor()
    self.window = window
    #window.AddActor(backActors[0])
    #window.AddActor(backActors[1])
    #frame.Show(True)
    return True

    
  def SaveImage(self):
    tiffSelector = "TIFF files (*.tiff)|*.tiff|"
    dlg = wx.FileDialog(self.window, message="Save image as ...", defaultDir=os.getcwd(), 
            defaultFile="", wildcard=tiffSelector, style=wx.SAVE)
    if dlg.ShowModal() == wx.ID_OK:
      path = dlg.GetPath()
      self.window.SaveFile(path)
    dlg.Destroy()
    
  def SaveProperties(self):
    saveFile = open("props.pickle", "w")
    pickler = pickle.Pickler(saveFile)
    for pipe in self.pipelines:
      pickler.dump(self.PropValues(pipe.Properties))
    saveFile.close()

    
  def PropValues(self, props):
    vals = []
    for prop in props:
      vals.append(prop.GetValue())
    return vals
  
  
  def LoadProperties(self):
    loadFile = open("props.pickle", "r")
    unpickler = pickle.Unpickler(loadFile)
    for pipe in self.pipelines:
      vals = unpickler.load()
      self.SetPropValues(pipe.Properties, vals)
    loadFile.close


    
  def SetPropValues(self, props, vals):
    for setIdx in range(len(vals)):
      props[setIdx].SetValue(vals[setIdx])
      
# HERE is MAIN()		
if __name__ == "__main__":
  
  app = App(0)
  app.MainLoop()

	