import vtk
import Properties
from PropertySet import PropertySet


class LineTube:
  def __init__(self, curve, domain):
    self.curve = curve
    self.domain = domain
    self.lineActor = None
    self.Properties = PropertySet()
    self.BuildCurve(self.curve)
    self.BuildTube()
  
  def GetActor(self):
    if not self.lineActor:
      self.BuildTube()
      
    return self.lineActor

  def ChangeCurve(self, curve):
    self.BuildCurve(curve)
    self.AttachTubeToCurve()
    
  def BuildCurve(self, curve):
    points = vtk.vtkPoints()
    domain = self.domain
    t = domain[0]
    while t < domain[1]:
      apply(points.InsertNextPoint, curve(t))
      t = t + domain[2]

    ptCnt = points.GetNumberOfPoints()
    lines = vtk.vtkCellArray()
    lines.InsertNextCell(ptCnt)
    for insertIdx in xrange(0, ptCnt):
      lines.InsertCellPoint(insertIdx)
    
    polyData = vtk.vtkPolyData()
    polyData.SetPoints(points)
    polyData.SetLines(lines)
    self.polyData = polyData

  def AttachTubeToCurve(self):
    self.tubeFilter.SetInput(self.polyData)
    self.tubeFilter.Modified()
    
  def BuildTube(self):    
    self.tubeFilter = vtk.vtkTubeFilter()
    self.tubeFilter.SetInput(self.polyData)
    self.tubeFilter.SetRadius(0.1)
    self.Properties.append(Properties.FloatProperty("tube radius",
                           self.tubeFilter.SetRadius, self.tubeFilter.GetRadius))
    self.tubeFilter.SetNumberOfSides(12)
    self.tubeFilter.CappingOn()
    
    map = vtk.vtkPolyDataMapper()
    map.SetInput(self.tubeFilter.GetOutput())
    
    self.lineActor = vtk.vtkActor()
    self.lineActor.SetMapper(map)
    self.lineActor.GetProperty().SetColor(1,.2,.2)
    self.Properties.append(Properties.ColorProperty("tube color",
                           self.lineActor.GetProperty().SetColor,
                           self.lineActor.GetProperty().GetColor))
  