# python planes8.py -c camera.pickle
# Hit "b" to save a camera position into a file called camera.pickle
# Hit "t" to save an image.

import vtk
import cmath
import pickle
import os
import math
import sys
import getopt

from DisplayWindow import DisplayWindow
from Backdrop import Backdrop


def ParametricUp(t):
  return [t, cmath.asinh(t).real, 2]

def ParametricDown(t):
  return [t, cmath.asinh(-t).real, -2]

  
class Twist:
  def __init__(self, domain):
    self.curve = [ ParametricUp, ParametricDown ]
    self.domain = domain
    self.stripCnt = 1
  
    self.BuildStrip()
    
  def EndPointsInsideLine(self, pt0, pt1, segmentIdx, segmentCnt):
    v = []
    for slopeIdx in range(3):
      v.append(pt1[slopeIdx] - pt0[slopeIdx])
    endRatio = [ float(segmentIdx)/segmentCnt, float(segmentIdx+1)/segmentCnt ]
    endPoint = []
    for endIdx in range(2):
      pt = []
      for dimIdx in range(3):
        pt.append( endRatio[endIdx]*v[dimIdx] + pt0[dimIdx] )
      endPoint.append(pt)
    return endPoint
    
    
  def BuildStrip(self):
    points = vtk.vtkPoints()
    domain = self.domain
    for stripIdx in range(self.stripCnt):
      t = domain[0]
      ptCnt = 0
      while t < domain[1]:
        sidePts = self.EndPointsInsideLine( self.curve[0](t), self.curve[1](t),
                                       stripIdx, self.stripCnt)
        apply(points.InsertNextPoint, sidePts[0])
        apply(points.InsertNextPoint, sidePts[1])
        ptCnt = ptCnt + 2
        t = t + domain[2]

    strips = vtk.vtkCellArray()
    cellPointIdx = 0
    for insertStripIdx in range(self.stripCnt):
      strips.InsertNextCell(ptCnt)
      for insertPointIdx in xrange(0, ptCnt):
        strips.InsertCellPoint(cellPointIdx)
        cellPointIdx = cellPointIdx + 1
    
    polyData = vtk.vtkPolyData()
    polyData.SetPoints(points)
    polyData.SetStrips(strips)
    
    map = vtk.vtkPolyDataMapper()
    map.SetInput(polyData)
    
    self.stripActor = vtk.vtkActor()
    self.stripActor.SetMapper(map)
    self.stripActor.GetProperty().SetColor(0.3800, 0.7000, 0.1600)
    self.stripActor.GetProperty().SetOpacity(0.5)

    
  def GetActor(self):
    return self.stripActor

    
    
class LineTube:
  def __init__(self, curve, domain):
    self.curve = curve
    self.domain = domain
    self.lineActor = None
  
  def GetActor(self):
    if not self.lineActor:
      self.BuildTube()
      
    return self.lineActor
    
  def BuildTube(self):
    points = vtk.vtkPoints()
    domain = self.domain
    t = domain[0]
    while t < domain[1]:
      apply(points.InsertNextPoint, self.curve(t))
      t = t + domain[2]

    ptCnt = points.GetNumberOfPoints()
    lines = vtk.vtkCellArray()
    lines.InsertNextCell(ptCnt)
    for insertIdx in xrange(0, ptCnt):
      lines.InsertCellPoint(insertIdx)
    
    polyData = vtk.vtkPolyData()
    polyData.SetPoints(points)
    polyData.SetLines(lines)
    
    tubeFilter = vtk.vtkTubeFilter()
    tubeFilter.SetInput(polyData)
    tubeFilter.SetRadius(0.1)
    tubeFilter.SetNumberOfSides(12)
    tubeFilter.CappingOn()
    
    map = vtk.vtkPolyDataMapper()
    map.SetInput(tubeFilter.GetOutput())
    
    self.lineActor = vtk.vtkActor()
    self.lineActor.SetMapper(map)
    self.lineActor.GetProperty().SetColor(1,.2,.2)
  
# HERE is MAIN()		
if __name__ == "__main__":
  domain = [ -5, 5, .1 ]
  backdrop = Backdrop(((-6, -4, -2), (6, 4, 2)))
  twist = Twist(domain)
  upTube = LineTube(ParametricUp, domain)
  downTube = LineTube(ParametricDown, domain)
  window = DisplayWindow()
  window.AddActor(twist.GetActor())
  window.AddActor(upTube.GetActor())
  window.AddActor(downTube.GetActor())
  backActors = backdrop.GetActor()
  #window.AddActor(backActors[0])
  #window.AddActor(backActors[1])
  
  window.Start()

	