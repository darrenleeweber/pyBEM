#!/usr/bin/env python

# python planes8.py -c camera.pickle
# Hit "b" to save a camera position into a file called camera.pickle
# Hit "t" to save an image.

import sys
import os
import getopt

import vtk
import wx
import cmath
import math
import pickle

from Backdrop import Backdrop
from ParametricSurface import ParametricSurface
from LineTube import LineTube

from VTKFrame import VTKFrame
from PropertyWxMediator import PropertyWxMediator
from DynamicDialog import DynamicDialog
from Properties import *
from PropertySet import PropertySet


def LeftUp(t):
  s = t-5
  return [0, cmath.asinh(2*s).real, t]

def LeftDown(t):
  s = t-5
  return [0, cmath.asinh(-2*s).real, t]

def RightUp(t):
  s = t-5
  return [t, cmath.asinh(2*s).real, 0]

def RightDown(t):
  s = t-5
  return [t, cmath.asinh(-2*s).real, 0]

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
    
    menuDynamic = wx.Menu()
    self.idToActor = {}
    for pipe in pipeline:
      twistId = wx.NewId()
      menuDynamic.Append( twistId, pipe.Name)
      frame.Bind(wx.EVT_MENU, self.OnDynamicMenu, id=twistId)
      self.idToActor[twistId] = pipe
    
    menuBar = wx.MenuBar()
    menuBar.Append(menuFile, "&File")
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
    self.SettingsFile = "props.pickle"
    self.Properties = PropertySet()
    self.Name = "app choices"
    self.leftUp = True
    self.rightUp = False
    self.Properties.append(ChoiceProperty("left tube up",
             self.SetLeftTube, self.GetLeftTube))
    self.Properties.append(ChoiceProperty("right tube up",
             self.SetRightTube, self.GetRightTube))
    'Create the main window and insert the custom frame'
    domain = [ -0, 10, .1 ]
    backdrop = Backdrop(((0, cmath.asinh(-10).real, 0), (10, 4, 10)))
    self.twist = ParametricSurface(domain, LeftUp, RightDown)
    if self.leftUp:
      upTube = LineTube(LeftUp, domain)
    else:
      upTube = LineTube(LeftDown, domain)
    if self.rightUp:
      downTube = LineTube(RightUp, domain)
    else:
      downTube = LineTube(RightDown, domain)
    
    self.twist.Name = "twist surface"
    upTube.Name = "left tube"
    downTube.Name = "right tube"
    backdrop.Name = "backdrop"
    self.pipelines = [self.twist, upTube, downTube, backdrop, self]
    window = VTKFrame()
    appMenu = AppMenu(window, self, self.pipelines)
    window.AddActor(self.twist.GetActor())
    window.AddActor(upTube.GetActor())
    window.AddActor(downTube.GetActor())
    backActors = backdrop.GetActor()
    self.window = window
    window.AddActor(backActors[0])
    window.AddActor(backActors[1])
    self.LoadProperties()
    #frame.Show(True)
    return True
  
  def SetTwist(self, upLeft, upRight):
    curve = []
    if upLeft:
      curve.append(LeftUp)
    else:
      curve.append(LeftDown)
    if upRight:
      curve.append(RightUp)
    else:
      curve.append(RightDown)
    self.twist.ChangeCurve(curve)
    
  def SetLeftTube(self, updown):
    self.leftUp = updown
    if updown:
      self.pipelines[1].ChangeCurve(LeftUp)
    else:
      self.pipelines[1].ChangeCurve(LeftDown)
    self.SetTwist(self.leftUp, self.rightUp)
  
  def GetLeftTube(self):
    if self.leftUp:
      return 1
    return 0
  
  def SetRightTube(self, updown):
    self.rightUp = updown
    if updown:
      self.pipelines[2].ChangeCurve(RightUp)
    else:
      self.pipelines[2].ChangeCurve(RightDown)
    self.SetTwist(self.leftUp, self.rightUp)
  
  def GetRightTube(self):
    if self.rightUp:
      return 1
    return 0
  
  def SaveImage(self):
    tiffSelector = "TIFF files (*.tiff)|*.tiff|"
    dlg = wx.FileDialog(self.window, message="Save image as ...", defaultDir=os.getcwd(), 
            defaultFile="", wildcard=tiffSelector, style=wx.SAVE)
    if dlg.ShowModal() == wx.ID_OK:
      path = dlg.GetPath()
      self.window.SaveFile(path)
    dlg.Destroy()
  
  def SaveProperties(self):
    saveFile = open(self.SettingsFile, "w")
    pickler = pickle.Pickler(saveFile)
    for pipe in self.pipelines:
      pickler.dump(pipe.Properties.WriteToDict())
    saveFile.close()
  
  def LoadProperties(self):
    if os.path.exists(self.SettingsFile):
      try:
        loadFile = open(self.SettingsFile, "r")
        unpickler = pickle.Unpickler(loadFile)
        for pipe in self.pipelines:
          vals = unpickler.load()
          pipe.Properties.ReadFromDict(vals)
        loadFile.close
      except:
        pass


if __name__ == "__main__":
  app = App()
  app.MainLoop()
