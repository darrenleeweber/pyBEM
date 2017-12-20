import vtk
from Properties import *
from PropertySet import PropertySet

class ParametricSurface:
  def __init__(self, domain, curve0, curve1):
    self.curve = [ curve0, curve1 ]
    self.domain = domain
    self.stripCnt = 1
    self.Properties = PropertySet()
    
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
    
  def BuildPolyData(self, curve):
    points = vtk.vtkPoints()
    domain = self.domain
    for stripIdx in range(self.stripCnt):
      t = domain[0]
      ptCnt = 0
      while t < domain[1]:
        sidePts = self.EndPointsInsideLine( curve[0](t), curve[1](t),
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
    return polyData

  def ChangeCurve(self, curve):
    self.curve = curve
    polyData = self.BuildPolyData(curve)
    self.map.SetInput(polyData)
    
  def BuildStrip(self):
    polyData = self.BuildPolyData(self.curve)
    self.map = vtk.vtkPolyDataMapper()
    self.map.SetInput(polyData)
    
    self.stripActor = vtk.vtkActor()
    self.stripActor.SetMapper(self.map)
    self.stripActor.GetProperty().SetColor(0.3800, 0.7000, 0.1600)
    self.stripActor.GetProperty().SetOpacity(0.5)

    self.Properties.append(ColorProperty("color",
        self.stripActor.GetProperty().SetColor,
        self.stripActor.GetProperty().GetColor))
    self.Properties.append(FloatProperty("opacity",
        self.stripActor.GetProperty().SetOpacity,
        self.stripActor.GetProperty().GetOpacity))
    
  def GetActor(self):
    return self.stripActor

    