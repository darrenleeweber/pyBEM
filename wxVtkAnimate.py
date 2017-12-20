#!/usr/bin/env python

import wx
import vtk

#from vtk.wx.wxVTKRenderWindow import *
from wxVTKRenderWindow import *


class MyApp(wx.App):
  """
  Main application class.
  """
  def OnInit(self):
    frame = MyFrame(None, "Test app ...")
    frame.Show(True)
    return True

class MyCue(vtk.vtkAnimationCue):
  def __init__(self, sphere):
    self._sphere = sphere
    self.AddObserver("AnimationCueTickEvent", self.Tick)

  def Tick(self, ct, dt):
    print "Tick (%s)" % dt
    print "  ct: %s" % ct
    print "  self: %s" % self


class MyFrame(wx.Frame):
  def __init__(self, parent, title):
    wx.Frame.__init__(self, parent, -1, title)
    self.InitGui()
    self.CreatePipeline()
    self.DefineAnimation()

  def InitGui(self):
    self._renWin = wxVTKRenderWindow(self, -1)

  def CreatePipeline(self):
    self._sphere = vtk.vtkSphereSource()
    self._sphere.SetThetaResolution(100)
    self._sphere.SetPhiResolution(100)
    self._sphere.SetStartTheta(10)

    self._mapper = vtk.vtkPolyDataMapper()
    self._actor = vtk.vtkActor()
    self._renderer = vtk.vtkRenderer()

    self._mapper.SetInput(self._sphere.GetOutput())
    self._actor.SetMapper(self._mapper)

    self._renderer.AddActor(self._actor)

    self._renWin.GetRenderWindow().AddRenderer(self._renderer)

  def DefineAnimation(self):
    cue = MyCue(self._sphere)
    cue.SetStartTime(0.0)
    cue.SetEndTime(2.0)

    scn = vtk.vtkAnimationScene()
    scn.AddCue(cue)
    scn.SetStartTime(0.0)
    scn.SetEndTime(2.0)
    scn.SetModeToRealTime()


    print "animation start ..."

    scn.Play()
    scn.Stop()

    print "animation end ..."
    scn.SetAnimationTime(0.3)


if __name__ == '__main__':
    app = MyApp(redirect=False)
    app.MainLoop()
