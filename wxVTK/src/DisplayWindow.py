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




class DisplayWindow:
  def __init__(self):
    self.backgroundColor = (.2,.2,.2) #(.3, .3, .5)
    # These affect writing the file. If it isn't JPEG, it's TIFF.
    # It makes a non-compressed TIFF, so you might want to open it in Photoshop and resave.
    self.bJPEGFile = 0
    # Turns on anti-aliasing. Use a number like 4, 8, or 16. Only works when magnification is off.
    self.imageAAFrames = 1
    # This multiplies the window size.
    self.imageMagnification = 1

    self.ren = vtk.vtkRenderer()
    self.renWin = vtk.vtkRenderWindow()
    self.renWin.AddRenderer(self.ren)
    self.iren = vtk.vtkRenderWindowInteractor()
    self.iren.SetRenderWindow(self.renWin)
  
    # Associate the actors with the
    # renderer.
    self.ren.SetBackground(self.backgroundColor)

    style = vtk.vtkInteractorStyleTrackballCamera()
    self.iren.SetInteractorStyle(style)
    style.AddObserver("KeyReleaseEvent", self.PrintCallback)

    # Zoom in a little bit.
    #self.ren.GetActiveCamera().Zoom(1.5)
    self.renWin.SetSize(700,700)
  
    light0 = vtk.vtkLight()
    light0.SetLightTypeToCameraLight()
    light0.PositionalOff()
    light0.SetPosition(-400, 100, 500)
    light0.SetFocalPoint(0,0,0)
    self.ren.AddLight(light0)
    light1 = vtk.vtkLight()
    light1.SetLightTypeToCameraLight()
    light1.PositionalOff()
    light1.SetPosition(+400, 50, 500)
    light1.SetSpecularColor(1,.8,.5)
    light1.SetDiffuseColor(.2,.2,.2)
    light1.SetFocalPoint(0,0,0)
    self.ren.AddLight(light1)
    
    # Initialize and start the event loop.
    self.iren.Initialize()
    self.renWin.Render()
    
    
    
  def Start(self):
    self.iren.Start()
    
    
    
    
  def PrintCallback(self, irenStyle, event):
    iren = irenStyle.GetInteractor()
    if 't' is iren.GetKeySym():
      renWin = iren.GetRenderWindow()
      windowToImage = vtk.vtkWindowToImageFilter()
      windowToImage.SetInput(renWin)
      windowToImage.SetMagnification(self.imageMagnification)
      if self.bJPEGFile:
        filename = "planes.jpg"
        writer = vtk.vtkJPEGWriter()
      else:
        writer = vtk.vtkTIFFWriter()
        filename = "planes.tif"
      writer.SetFileName(filename)
      writer.SetInput(windowToImage.GetOutput())
      #writer.SetCompressionToLZW()ple
      aaFrames = renWin.GetAAFrames()
      renWin.SetAAFrames(self.imageAAFrames)
      writer.Write()
      renWin.SetAAFrames(aaFrames)
      print "wrote", filename
      renWin.Render()      
		
    
    
  def AddActor(self, actor):
    self.ren.AddActor(actor)
    
    
    
  def RemoveActor(self, actor):
    self.ren.RemoveActor(actor)
		

# HERE is MAIN()		
if __name__ == "__main__":
  pass
	