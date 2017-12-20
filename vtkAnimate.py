#!/usr/bin/env python
"""
This simple example shows how to do basic animation
using pyVTK
"""

import sys
import vtk

class CueAnimator:
    
    def __init__(self):
        self.SphereSource = 0
        self.Mapper = 0
        self.Actor = 0
    
    def StartCue(self, ren=vtk.vtkRenderer()):
        print "*** IN StartCue "
        self.SphereSource = vtk.vtkSphereSource()
        self.SphereSource.SetRadius(0.5)
        
        self.Mapper = vtk.vtkPolyDataMapper()
        self.Mapper.SetInput(self.SphereSource.GetOutput())
        
        self.Actor = vtk.vtkActor()
        self.Actor.SetMapper(self.Mapper)
        
        ren.AddActor(self.Actor)
        ren.ResetCamera()
        ren.Render()
    
    def Tick(self, info=vtk.vtkAnimationCue(), ren=vtk.vtkRenderer()):
        newradius = 0.1 + float(info.CurrentTime - info.StartTime)/float(info.EndTime - info.StartTime) * 1.0
        self.SphereSource.SetRadius(newradius)
        self.SphereSource.Update()
        ren.Render()
    
    def EndCue(self, ren=vtk.vtkRenderer()):
        ren.RemoveActor(self.Actor)


class vtkAnimationCueObserver(vtk.vtkAnimationCueObserver):
    
    def __init__(self):
        vtk.vtkAnimationCueObserver.__init__()
        self.Renderer = vtk.vtkRenderer()
        self.Animator = CueAnimator()
        self.RenWin = vtk.vtkRenderWindow()
    
    def Execute(self, event, calldata):
        if (self.Animator and self.Renderer):
            if(event==vtk.vtkCommand.StartAnimationCueEvent):
                self.Animator.StartCue(calldata, self.Renderer)
            if(event==vtk.vtkCommand.EndAnimationCueEvent):
                self.Animator.EndCue(calldata, self.Renderer)
            if(event==vtk.vtkCommand.AnimationCueTickEvent):
                self.Animator.Tick(calldata, self.Renderer)
        if (self.RenWin): self.RenWin.Render()


if __name__ == '__main__':
    
    # Create animation Scene
    scene = vtk.vtkAnimationScene()
    if (len(sys.argv) >= 2 and sys.argv[1]=="real"):
        scene.SetModeToRealTime()
    else:
        scene.SetModeToSequence()
    
    scene.SetLoop(0)
    scene.SetFrameRate(5)
    scene.SetStartTime(3)
    scene.SetEndTime(20)
    
    # Create an Animation Cue.
    cue1 = vtk.vtkAnimationCue()
    cue1.SetStartTime(5)
    cue1.SetEndTime(13)
    scene.AddCue(cue1)
    
    # Create cue animator
    animator = vtk.CueAnimator()
    
    # Create Cue observer
    observer = vtkAnimationCueObserver()
    cue1.AddObserver(vtk.vtkCommand.StartAnimationCueEvent(), observer);
    cue1.AddObserver(vtk.vtkCommand.EndAnimationCueEvent(), observer);
    cue1.AddObserver(vtk.vtkCommand.AnimationCueTickEvent(), observer);
    
    scene.Play()
    scene.Stop()
