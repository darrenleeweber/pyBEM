
import vtk
from Properties import *
from PropertySet import PropertySet

class Backdrop:
  def __init__(self, box):
    """Box is [ lower-left point, lower-right point ].
    """
    self.box = box
    self.Properties = PropertySet()
  
  def SetResolution(self, pieces):
    for planeSource in self.planeSources:
      planeSource.SetXResolution(pieces)
      planeSource.SetYResolution(pieces)
  def GetResolution(self):
    return self.planeSources[0].GetXResolution()
  
  def SetTubeThickness(self, thickness):
    for filter in self.tubeFilter:
      filter.SetRadius(thickness)
      
  def GetTubeThickness(self):
    return self.tubeFilter[0].GetRadius()
    
  def GetActor(self):
    planeCnt = 3
    planeSources = []
    for createSources in range(planeCnt):
      planeSources.append(vtk.vtkPlaneSource())
      
    self.planeSources = planeSources
    
    endPts = (
      (0,0,0), (1, 0, 0), (0,0,1),
      (0,1,0), (1,1,0), (0,0,0),
      (0,1,0), (0,0,0), (0,1,1)
      )
    
    box = self.box
    
    planeSources[0].SetOrigin(box[0][0], box[0][1], box[0][2])
    planeSources[0].SetPoint1(box[1][0], box[0][1], box[0][2])
    planeSources[0].SetPoint2(box[0][0], box[0][1], box[1][2])
    planeSources[1].SetOrigin(box[0][0], box[1][1], box[0][2])
    planeSources[1].SetPoint1(box[1][0], box[1][1], box[0][2])
    planeSources[1].SetPoint2(box[0][0], box[0][1], box[0][2])
    planeSources[2].SetOrigin(box[0][0], box[1][1], box[0][2])
    planeSources[2].SetPoint1(box[0][0], box[0][1], box[0][2])
    planeSources[2].SetPoint2(box[0][0], box[1][1], box[1][2])

    planeSources[0].SetXResolution(5)
    planeSources[0].SetYResolution(5)
    planeSources[1].SetXResolution(5)
    planeSources[1].SetYResolution(5)
    planeSources[2].SetXResolution(5)
    planeSources[2].SetYResolution(5)
    
    self.Properties.append(IntProperty("plane resolution",
                   self.SetResolution, self.GetResolution))
    
    appendPolyData = vtk.vtkAppendPolyData()
    for appendIdx in range(planeCnt):
      appendPolyData.AddInput(planeSources[appendIdx].GetOutput())

    self.tubeFilter = []
    collectTubes = vtk.vtkAppendPolyData()
    for tubeIdx in range(planeCnt):
      edgeFilter = vtk.vtkExtractEdges()
      edgeFilter.SetInput(planeSources[tubeIdx].GetOutput())
      tubeFilter = vtk.vtkTubeFilter()
      tubeFilter.SetInput(edgeFilter.GetOutput())
      tubeFilter.SetRadius(0.05)
      tubeFilter.SetNumberOfSides(12)
      self.tubeFilter.append(tubeFilter)
      collectTubes.AddInput(tubeFilter.GetOutput())
    self.Properties.append(FloatProperty("grid thickness",
                           self.SetTubeThickness, self.GetTubeThickness))
    
    tubeMap = vtk.vtkPolyDataMapper()
    tubeMap.SetInput(collectTubes.GetOutput())
    tubeActor = vtk.vtkActor()
    tubeActor.SetMapper(tubeMap)
    tubeActor.GetProperty().SetColor(0.1,0.1, 0.1)
    self.Properties.append(ColorProperty("grid color",
                    tubeActor.GetProperty().SetColor, tubeActor.GetProperty().GetColor))
    self.Properties.append(FloatProperty("grid opacity",
                    tubeActor.GetProperty().SetOpacity, tubeActor.GetProperty().GetOpacity))
    self.Properties.append(ChoiceProperty("grid visible",
                    tubeActor.SetVisibility, tubeActor.GetVisibility))

    map = vtk.vtkPolyDataMapper()
    map.SetInput(appendPolyData.GetOutput())
    
    planeActor = vtk.vtkActor()
    planeActor.SetMapper(map)
    planeActor.GetProperty().SetColor(.2, .2, .2)
    self.Properties.append(ColorProperty("plane color",
                    planeActor.GetProperty().SetColor, planeActor.GetProperty().GetColor))
    self.Properties.append(FloatProperty("plane opacity",
                    planeActor.GetProperty().SetOpacity, planeActor.GetProperty().GetOpacity))
    self.Properties.append(ChoiceProperty("plane visible",
                    planeActor.SetVisibility, planeActor.GetVisibility))
    return [planeActor, tubeActor]
